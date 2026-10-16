import os
import tempfile
import unittest
from unittest import mock

from src import cli, util

# TODO: Revamped by Github Copilot. Needs review and testing. 
#       The original outdated tests were removed, and new tests were added for the CLI module.
#       Some were moved to test_basic.py, and some were removed because they were not relevant to the CLI module.

class TestConfigLoading(unittest.TestCase):
    def test_parse_jsonc_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "config.jsonc")
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write('{"paths": {"work": "/tmp/work"}}')

            config = cli.parse_config_file(config_path)

        self.assertIsInstance(config, util.NameSpace)
        self.assertEqual(config.paths.work, "/tmp/work")

    def test_parse_yaml_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "config.yml")
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write("paths:\n  work: /tmp/work\n")

            config = cli.parse_config_file(config_path)

        self.assertIsInstance(config, util.NameSpace)
        self.assertEqual(config.paths.work, "/tmp/work")

    def test_parse_config_rejects_unsupported_extension(self):
        with self.assertRaises(util.UnsupportedFileTypeError):
            cli.parse_config_file("config.txt")


class TestConfigPathValidation(unittest.TestCase):
    def test_read_config_file_returns_parsed_contents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            os.mkdir(config_dir)
            config_path = os.path.join(config_dir, "logging.jsonc")
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write('{"enabled": true}')

            result = cli.read_config_file(temp_dir, "config", "logging.jsonc")

        self.assertEqual(result, {"enabled": True})

    def test_verify_dirpath_creates_missing_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "work")

            result = cli.verify_dirpath(new_dir, temp_dir)

            self.assertEqual(result, new_dir)
            self.assertTrue(os.path.isdir(new_dir))

    def test_verify_dirpath_resolves_parent_relative_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            code_root = os.path.join(temp_dir, "code")
            os.mkdir(code_root)
            expected_path = os.path.join(temp_dir, "work")

            result = cli.verify_dirpath("../work", code_root)

            self.assertEqual(result, expected_path)
            self.assertTrue(os.path.isdir(expected_path))


class TestDateValidation(unittest.TestCase):
    def test_check_date_format_accepts_supported_formats(self):
        for date_string in ("2001", "200101", "2001-01", "20010131", "2001-01-31"):
            with self.subTest(date_string=date_string):
                self.assertIsNotNone(cli.check_date_format(date_string))

    def test_check_date_format_rejects_invalid_date(self):
        with self.assertRaises(util.MDTFBaseException):
            cli.check_date_format("not-a-date")


class TestCondaEnvironmentValidation(unittest.TestCase):
    def test_verify_conda_envs_rejects_missing_conda_and_micromamba(self):
        config = util.NameSpace.fromDict({
            "micromamba_exe": "/missing/micromamba",
            "conda_root": "/missing/conda",
            "conda_env_root": "/missing/envs",
        })

        with mock.patch.object(cli.os.path, "exists", return_value=False):
            with self.assertRaises(util.MDTFBaseException):
                cli.verify_conda_envs(config, "runtime_config.jsonc")

    def test_verify_conda_envs_uses_conda_envs_directory(self):
        config = util.NameSpace.fromDict({
            "micromamba_exe": "/missing/micromamba",
            "conda_root": "/opt/conda",
            "conda_env_root": "/missing/envs",
        })

        def path_exists(path):
            return path in {"/opt/conda", "/opt/conda/envs"}

        with mock.patch.object(cli.os.path, "exists", side_effect=path_exists):
            result = cli.verify_conda_envs(config, "runtime_config.jsonc")

        self.assertIs(result, config)
        self.assertEqual(config.conda_env_root, "/opt/conda/envs")


if __name__ == "__main__":
    unittest.main()
