from click.testing import CliRunner
import importlib
import os
import tempfile
import unittest
from unittest.mock import patch
import shutil
import sys

from zipline.repo import GROUP_BY_FOLDER_NAME, JOIN_FOLDER_NAME
from zipline.repo.materialize import extract_and_convert
import zipline.schema.thrift.ttypes as ttypes

TEAM_NAME = 'zipline_test'


def write_group_by(
        group_by_version,
        output_file_path,
        online,
        production,
        startPartition):
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    with open(os.path.join(os.path.dirname(__file__), 'GROUP_BY_TEMPLATE')) as f, \
         open(output_file_path, mode='w') as output_file:
        template = f.read()
        output_file.write(template.format(group_by_version=group_by_version,
                                          startPartition=startPartition,
                                          online=online,
                                          production=production))


def write_join(
        join_version,
        output_file_path,
        group_by_name,
        online,
        production,
        startPartition):
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    with open(os.path.join(os.path.dirname(__file__), 'JOIN_TEMPLATE')) as f, \
         open(output_file_path, mode='w') as output_file:
        template = f.read()
        output_file.write(template.format(group_by_name=group_by_name,
                                          join_version=join_version,
                                          online=online,
                                          startPartition=startPartition,
                                          production=production))


def get_name(filename, version):
    return '.'.join([TEAM_NAME, filename.split('.')[0], version])


# Base group by name and join name.
BASE_GROUP_BY_FILENAME = 'test_group_by.py'
BASE_JOIN_FILENAME = 'test_join.py'
BASE_GROUP_BY_VERSION = 'v1'
BASE_JOIN_VERSION = 'test'
BASE_GROUP_BY_NAME = get_name(
    BASE_GROUP_BY_FILENAME, BASE_GROUP_BY_VERSION)
BASE_JOIN_NAME = get_name(
    BASE_JOIN_FILENAME, BASE_JOIN_VERSION)

GROUP_BY_CLASS_NAME = ttypes.GroupBy.__name__
JOIN_CLASS_NAME = ttypes.LeftOuterJoin.__name__


class TestMaterialize(unittest.TestCase):

    def setUp(self):
        self.input_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..', 'resources')
        if not os.path.exists(self.input_directory):
            os.makedirs(self.input_directory)
            sys.path.append(self.input_directory)
        self.output_directory = tempfile.mkdtemp()
        self.group_by_output_path = os.path.join(
            self.output_directory, GROUP_BY_FOLDER_NAME, TEAM_NAME)
        self.join_output_path = os.path.join(
            self.output_directory, JOIN_FOLDER_NAME, TEAM_NAME)
        self.group_by_input_path = os.path.join(
            self.input_directory, GROUP_BY_FOLDER_NAME, TEAM_NAME)
        self.join_input_path = os.path.join(
            self.input_directory, JOIN_FOLDER_NAME, TEAM_NAME)

        if not os.path.exists(self.group_by_input_path):
            os.makedirs(self.group_by_input_path)
        if not os.path.exists(self.join_input_path):
            os.makedirs(self.join_input_path)
        self.runner = CliRunner()

    def setup_group_by_and_join(
            self,
            group_by_filename=BASE_GROUP_BY_FILENAME,
            join_filename=BASE_JOIN_FILENAME,
            group_by_name=BASE_GROUP_BY_NAME,
            group_by_version=BASE_GROUP_BY_VERSION,
            join_version=BASE_JOIN_VERSION,
            group_by_online=None,
            group_by_production=None,
            join_online=False,
            join_production=False,
            startPartition="2019-11-01"):
        group_by_file_path = os.path.join(self.group_by_input_path, group_by_filename)
        join_file_path = os.path.join(self.join_input_path, join_filename)
        write_group_by(
            group_by_version, group_by_file_path, online=group_by_online, production=group_by_production, startPartition=startPartition)
        write_join(
            join_version, join_file_path, group_by_name, online=join_online, production=join_production, startPartition=startPartition)

    def tearDown(self):
        shutil.rmtree(self.group_by_input_path)
        shutil.rmtree(self.join_input_path)
        shutil.rmtree(self.output_directory)
        self._unload_objs()

    def _unload_objs(self):
        """Unload loaded group by and join files.
        """
        loaded_modules = [
            module for module in sys.modules
            if module.startswith(f'{GROUP_BY_FOLDER_NAME}') or
            module.startswith(f'{JOIN_FOLDER_NAME}')]
        for module in loaded_modules:
            mod = importlib.import_module(module)
            if hasattr(mod, '__cached__') and os.path.exists(mod.__cached__):
                os.remove(mod.__cached__)
            del mod
            del sys.modules[module]

    def _invoke_cli(
            self,
            input_path,
            zipline_root=None,
            output_directory=None):

        if not zipline_root:
            zipline_root = self.input_directory
        if not output_directory:
            output_directory = self.output_directory
        return self.runner.invoke(
            extract_and_convert, [
                '--zipline_root',
                zipline_root,
                '--input_path',
                input_path,
                '--output_root',
                output_directory,
                '--debug'
            ],
            env=os.environ.copy(),
            catch_exceptions=False,
        )

    ###
    # Test materializing single entities.
    ###

    def test_materialize_same_config(self):
        """Materializing the same config skips the config.
        """
        self.setup_group_by_and_join(
            group_by_online=None,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        # First materialize join.
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        self._unload_objs()
        # Materializing the same join results in nothing materialized.
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        assert f"Skipping {JOIN_CLASS_NAME} {BASE_JOIN_NAME}" in result.output

    def test_does_not_materialize_offline_groupby(self):
        self.setup_group_by_and_join(
            group_by_online=False, group_by_production=None)
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no online False group bys are materialized.
        assert not os.path.exists(self.group_by_output_path)
        self.setup_group_by_and_join(
            group_by_online=None, group_by_production=None)
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no offline group bys are materialized.
        assert not os.path.exists(self.group_by_output_path)

    def test_materialize_online_groupby_in_offline_join(self):
        """Materializing online groupby succeeds.
        """
        self.setup_group_by_and_join(
            group_by_online=True, group_by_production=None, join_online=False)
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        # Materializes online group bys.
        assert len(os.listdir(self.group_by_output_path)) == 1

    def test_materialize_offline_join(self):
        """Materializing offline join with group by with no explicit status succeeds.
        """
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=False,
            join_production=False
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        assert len(os.listdir(self.join_output_path)) == 1
        # Assert no offline group bys are materialized.
        assert not os.path.exists(self.group_by_output_path)

    def test_materialize_online_join(self):
        """Materializing online join creates both join and the underlying group by.
        """
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=False
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        assert len(os.listdir(self.join_output_path)) == 1
        # Assert online group bys are created.
        assert len(os.listdir(self.group_by_output_path)) == 1

    def test_materialize_online_join_with_offline_group_by(self):
        """Materializing online join with offline group by fails.
        """
        self.setup_group_by_and_join(
            group_by_online=False,
            group_by_production=None,
            join_online=True,
            join_production=False
        )

        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no joins are created.
        assert not os.path.exists(self.join_output_path)
        # Assert no group bys are created.
        assert not os.path.exists(self.group_by_output_path)

    ###
    # Test validation Rules against other existing entities.
    ###

    def test_materialize_offline_group_by_in_online_join(self):
        """Materializing offline group by included in online join fails.
        """
        self.setup_group_by_and_join(
            group_by_online=False,
            group_by_production=None,
            join_online=True,
            join_production=False
        )
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no group bys are created.
        assert not os.path.exists(self.group_by_output_path)

    def test_materialize_non_production_group_by_in_production_join_fails(self):
        """Materializing non production group by included in production join fails.
        """
        # First materialize production offline join.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=False,
            join_production=True
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        # Change group by to non-production, join stays production.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=False,
            join_online=False,
            join_production=True
        )
        self._unload_objs()
        # Materializing non production group by in production join fails.
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        assert f"Could not write {GROUP_BY_CLASS_NAME} {BASE_GROUP_BY_NAME}" in result.output
        # Change start partition to trigger re-materialization.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=False,
            join_online=False,
            join_production=True,
            startPartition="2018-01-01"
        )
        # Materializing the production offline join succeeds
        # since the non production group by was not materialized.
        self._unload_objs()
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        assert f"Successfully wrote 1 {JOIN_CLASS_NAME} object" in result.output

    def test_materialize_online_production_join_with_non_production_group_by_fails(self):
        """Materializing online production join including non production group by fails.
        """
        # First materialize production online join.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        # Change group by to non-production, join stays production.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=False,
            join_online=True,
            join_production=True
        )
        # Materializing the production online join fails
        # since the non production group by included can't be materialized.
        self._unload_objs()
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no joins are created.
        assert f"Could not write {JOIN_CLASS_NAME} {BASE_JOIN_NAME}" in result.output

    def test_materialize_online_non_production_join_with_production_group_by_works(self):
        """Materializing online non production join including production group by works.
        """
        # First materialize production group by.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=True,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        # Change group by to non-production, join stays production.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=False,
            join_online=True,
            join_production=True
        )
        # Materializing the production online join fails
        # since the non production group by included can't be materialized.
        self._unload_objs()
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert no joins are created.
        assert f"Could not write {JOIN_CLASS_NAME} {BASE_JOIN_NAME}" in result.output

    ###
    # Test overwriting protected entities.
    ###
    @patch('zipline.repo.validator.get_input', return_value='y')
    def test_confirm_join_overwrite_succeeds(self, input):
        """
        Changing online join prompts user to confirm and writes if user confirms.
        """
        # First materialize online join.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        # Change start partition to trigger re-materialization.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True,
            startPartition="2018-01-01"
        )
        self._unload_objs()
        # Materializing the online join triggers user input to confirm.
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert joins are re-created.
        assert f"Successfully wrote 1 {JOIN_CLASS_NAME} objects" in result.output

    @patch('zipline.repo.validator.get_input', return_value='n')
    def test_confirm_join_overwrite_fails(self, input):
        """
        Changing online join prompts user to confirm and does not write if user does not confirms.
        """
        # First materialize online join.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        # Change start partition to trigger re-materialization.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True,
            startPartition="2011-01-01"
        )
        # Materializing the online join fails if the user declines.
        self._unload_objs()
        result = self._invoke_cli(JOIN_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert joins are not re-created.
        assert f"user declined to overwrite {JOIN_CLASS_NAME} {BASE_JOIN_NAME}" in result.output

    @patch('zipline.repo.validator.get_input', return_value='y')
    def test_confirm_group_by_overwrite_succeeds(self, input):
        """
        Changing online group by prompts user to confirm and writes if user confirms.
        """
        # First materialize online group_by.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        # Change startPartition to trigger re-materialization.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True,
            startPartition='2012-01-01'
        )
        self._unload_objs()
        # Materializing the online group by triggers user input to confirm.
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        assert result.exit_code == 0
        # Assert group bys are re-created.
        assert f"Successfully wrote 1 {GROUP_BY_CLASS_NAME} objects" in result.output

    @patch('zipline.repo.validator.get_input', return_value='n')
    def test_confirm_group_by_overwrite_fails(self, input):
        """
        Changing online group by prompts user to confirm and fails if user declines.
        """
        # First materialize online group_by.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True
        )
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)
        # Change startPartition to trigger re-materialization.
        self.setup_group_by_and_join(
            group_by_online=True,
            group_by_production=None,
            join_online=True,
            join_production=True,
            startPartition='2012-01-01'
        )
        self._unload_objs()
        # Materializing the online group by triggers user input to confirm.
        result = self._invoke_cli(GROUP_BY_FOLDER_NAME)

        assert result.exit_code == 0
        # Assert group by are not re-created.
        assert f"user declined to overwrite {GROUP_BY_CLASS_NAME} {BASE_GROUP_BY_NAME}" in result.output
