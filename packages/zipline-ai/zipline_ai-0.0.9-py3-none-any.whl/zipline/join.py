import copy
import importlib
import json
import zipline.group_by as gb
import zipline.schema.thrift.ttypes as ttypes
import zipline.utils as utils
from typing import List, Dict, Union, Optional, Iterable
from zipline.metadata_helper import get_dependencies


def _expand_selectors(group_by: ttypes.GroupBy,
                      selectors: Optional[List[Union[ttypes.AggregationSelector, str]]]):
    if selectors is None:
        if group_by.aggregations:
            for aggregation in group_by.aggregations:
                if aggregation.windows:
                    yield ttypes.AggregationSelector(
                        name=aggregation.name,
                        windows=aggregation.windows
                    )
                else:
                    yield ttypes.AggregationSelector(
                        name=aggregation.name
                    )
        else:
            for column in gb.get_columns(group_by.sources[0]):
                yield ttypes.AggregationSelector(name=column)
    else:
        valid_names: Optional[Iterable[str]] = None
        aggregation_map: Dict[str, ttypes.Aggregation]
        if group_by.aggregations:
            aggregation_map = {
                aggregation.name: aggregation
                for aggregation in group_by.aggregations
            }
            valid_names = aggregation_map.keys()
        else:  # pre-aggregated
            valid_names = set([column for column in gb.get_columns(group_by.sources[0])])
        for selector in selectors:
            if isinstance(selector, ttypes.AggregationSelector):
                utils.check_contains(selector.name,
                                     valid_names,
                                     "aggregation",
                                     group_by.name)
                if selector.windows:
                    assert group_by.aggregations, f"""
group_by:{group_by.name} doesn't have windows, and is pre-aggregated.
You requested: {selector}
"""
                    utils.check_contains(selector.windows,
                                         aggregation_map[selector.name].windows,
                                         "window",
                                         f"{group_by.name}:{selector.name}",
                                         gb.window_to_str_pretty)
                yield selector
            else:
                # selector is a string name
                utils.check_contains(selector, valid_names, "aggregation", group_by.name)
                yield ttypes.AggregationSelector(
                    name=selector
                )


def JoinPart(group_by_name: str,  # the python qualifier
             keyMapping: Dict[str, str] = None,  # mapping of key columns from the join
             selectors: Optional[List[Union[ttypes.AggregationSelector, str]]] = None,
             prefix: str = None  # all aggregations will be prefixed with that name
             ) -> ttypes.JoinPart:
    name_fields = group_by_name.split('.')
    variable_name = name_fields[-1]
    module_path = f"group_bys.{'.'.join(name_fields[:-1])}"
    module = importlib.import_module(module_path)
    group_by = module.__dict__[variable_name]
    group_by.name = group_by_name
    if keyMapping:
        utils.check_contains(keyMapping.values(),
                             group_by.keyColumns,
                             "key",
                             group_by_name)

    return ttypes.JoinPart(
        groupBy=group_by,
        keyMapping=keyMapping,
        selectors=list(_expand_selectors(group_by, selectors)),
        prefix=prefix
    )


def LeftOuterJoin(left: ttypes.Source,
                  rightParts: List[ttypes.JoinPart],
                  check_consistency: bool = False,
                  additional_args: List[str] = None,
                  additional_env: List[str] = None,
                  online: bool = False,
                  production: bool = False) -> ttypes.LeftOuterJoin:
    # create a deep copy for case: multiple LeftOuterJoin use the same left,
    # validation will fail after the first iteration
    updated_left = copy.deepcopy(left)
    if left.events:
        assert "ts" not in left.events.query.select.keys(), "'ts' is a reserved key word for Zipline," \
                                                          " please specify the expression in timeColumn"
        # mapping ts to query.timeColumn to events only
        updated_left.events.query.select.update({"ts": updated_left.events.query.timeColumn})
    # name is set externally, cannot be set here.
    root_base_source = updated_left.entities if updated_left.entities else updated_left.events
    root_keys = set(root_base_source.query.select.keys())
    for joinPart in rightParts:
        mapping = joinPart.keyMapping if joinPart.keyMapping else {}
        utils.check_contains(mapping.keys(), root_keys, "root key", "")
        uncovered_keys = set(joinPart.groupBy.keyColumns) - set(mapping.values()) - root_keys
        assert not uncovered_keys, f"""
Not all keys columns needed to join with GroupBy:{joinPart.groupBy.name} are present.
Missing keys are: {uncovered_keys},
Missing keys should be either mapped or selected in root.
KeyMapping only mapped: {mapping.values()}
Root only selected: {root_keys}
        """

    dependencies = get_dependencies(updated_left)

    right_sources = [joinPart.groupBy.sources for joinPart in rightParts]
    # flattening
    right_sources = [source for source_list in right_sources for source in source_list]
    right_dependencies = [dep for source in right_sources for dep in get_dependencies(source)]

    dependencies.extend(right_dependencies)
    metadata_map = {
        "check_consistency": check_consistency,
        "dependencies": json.dumps(list({frozenset(item.items()): item for item in dependencies}.values()))
    }

    if additional_args:
        metadata_map["additional_args"] = additional_args

    if additional_env:
        metadata_map["additional_env"] = additional_env

    metadata = json.dumps(metadata_map)

    return ttypes.LeftOuterJoin(
        left=updated_left,
        rightParts=rightParts,
        metadata=metadata,
        online=online,
        production=production
    )
