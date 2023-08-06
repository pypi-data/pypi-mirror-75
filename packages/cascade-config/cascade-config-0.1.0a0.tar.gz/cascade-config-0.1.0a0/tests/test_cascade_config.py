"""Test cascade_config."""

import argparse
import json
from os import stat
import tempfile
from typing import Type

import pytest
import jsonschema

import cascade_config
from cascade_config import ValidationSchema

TEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Test schema",
    "type": "object",
    "properties": {
        "config_example": {
            "type": "object",
            "properties": {
                "num_cpu": {
                    "type": "number",
                    "minimum": -1,
                },
                "log_level": {
                    "type": "string",
                    "enum": ["debug", "info", "warning", "error", "critical"]
                }
            }
        }
    }
}

TEST_SAMPLE = {
    "config_example": {"num_cpu": 1, "log_level": "info"}
}
TEST_SAMPLE_2 = {
    "config_example": {"log_level": "debug"}, "test": True
}
TEST_SAMPLE_CASC = {
    "config_example": {"num_cpu": 1, "log_level": "debug"}, "test": True
}

TEST_SAMPLE_INVALID = {
    "config_example": {"num_cpu": "not_a_number", "log_level": "info"}
}

def get_sample_namespace(test_sample):
    flatten = lambda l: [item for sublist in l for item in sublist]
    test_args = flatten([[f"--{i[0]}", f"{i[1]}"] for i in test_sample.items()])
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_cpu", type=int)
    parser.add_argument("--log_level")
    return parser.parse_args(test_args)


class TestCascadeConfig:
    """Test CascadeConfig."""

    @staticmethod
    def get_json_file(test_sample):
        with tempfile.NamedTemporaryFile(mode='wt', delete=False) as json_file:
            json.dump(test_sample, json_file)
            json_file.seek(0)
            json_file_name = json_file.name
        return json_file_name

    @staticmethod
    def get_sample_namespace(test_sample):
        flatten = lambda l: [item for sublist in l for item in sublist]
        test_args = flatten([[f"--{i[0]}", f"{i[1]}"] for i in test_sample.items()])
        parser = argparse.ArgumentParser()
        parser.add_argument("--num_cpu", type=int)
        parser.add_argument("--log_level")
        return parser.parse_args(test_args)

    def test_single_config(self):
        cc = cascade_config.CascadeConfig()
        cc.add_dict(TEST_SAMPLE)
        assert cc.parse() == TEST_SAMPLE

    def test_single_config_validation(self):
        """Test single valid dict source, with JSON Schema validation"."""
        cc = cascade_config.CascadeConfig(validation_schema=TEST_SCHEMA)
        cc.add_dict(TEST_SAMPLE)
        assert cc.parse() == TEST_SAMPLE

    def test_single_config_validation_invalid(self):
        """Test single invalid dict source, with JSON Schema validation"."""
        cc = cascade_config.CascadeConfig(validation_schema=TEST_SCHEMA)
        cc.add_dict(TEST_SAMPLE_INVALID)
        with pytest.raises(jsonschema.exceptions.ValidationError):
            cc.parse()

    def test_single_config_json(self):
        """Test JSON config."""
        cc = cascade_config.CascadeConfig()
        cc.add_json(self.get_json_file(TEST_SAMPLE), validation_schema=TEST_SCHEMA)
        assert cc.parse() == TEST_SAMPLE

    def test_single_config_namespace(self):
        """Test Namespace config."""
        subkey = "config_example"
        cc = cascade_config.CascadeConfig()
        cc.add_namespace(
            get_sample_namespace(TEST_SAMPLE[subkey]),
            subkey=subkey,
            validation_schema=TEST_SCHEMA
        )
        assert cc.parse() == TEST_SAMPLE

    def test_single_config_dict_typeerror(self):
        """Test Namespace config type error."""
        cc = cascade_config.CascadeConfig()
        cc.add_dict(42)
        with pytest.raises(TypeError):
            cc.parse()

    def test_single_config_json_typeerror(self):
        """Test Namespace config type error."""
        cc = cascade_config.CascadeConfig()
        cc.add_json(42)
        with pytest.raises(TypeError):
            cc.parse()

    def test_single_config_namespace_typeerror(self):
        """Test Namespace config type error."""
        cc = cascade_config.CascadeConfig()
        cc.add_namespace("not_a_namespace")
        with pytest.raises(TypeError):
            cc.parse()

    def test_multiple_configs(self):
        """Test multiple config sources."""
        subkey = "config_example"
        cc = cascade_config.CascadeConfig(validation_schema=TEST_SCHEMA)
        cc.add_namespace(
            get_sample_namespace(TEST_SAMPLE[subkey]),
            subkey=subkey,
        )
        cc.add_json(self.get_json_file(TEST_SAMPLE_2))
        assert cc.parse() == TEST_SAMPLE_CASC

    def test_validation_schema_from_object(self):
        with pytest.raises(TypeError):
            cascade_config.ValidationSchema.from_object(42)

    def test_validation_schema_from_json(self):
        vs = cascade_config.ValidationSchema(self.get_json_file(TEST_SCHEMA))
        assert vs.load() == TEST_SCHEMA
