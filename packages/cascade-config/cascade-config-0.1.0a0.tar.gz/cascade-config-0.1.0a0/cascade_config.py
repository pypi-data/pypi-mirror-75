"""Cascading configuration from the CLI and config files."""

__version__ = "0.1.0-a0"

import json
import os
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict

import jsonschema


class CascadeConfig:
    """Cascading configuration."""

    def __init__(self, validation_schema=None):
        """
        Cascading configuration.

        Parameters
        ----------
        validation_schema: str, path-like, dict, or cascade_config.ValidationSchema, optional
            JSON Schema to validate fully cascaded configuration

        Examples
        --------
        >>> cascade_conf = CascadeConfig(validation_schema="config_schema.json")
        >>> cascade_conf.add_json("config_default.json")
        >>> cascade_conf.add_json("config_user.json")
        >>> config = cascade_conf.parse()

        """
        self.validation_schema = validation_schema
        self.sources = []

    @property
    def validation_schema(self):
        """JSON Schema to validate fully cascaded configuration."""
        return self._validation_schema

    @validation_schema.setter
    def validation_schema(self, value):
        """Set validation schema."""
        if value:
            self._validation_schema = ValidationSchema.from_object(value)
        else:
            self._validation_schema = None

    def _update_dict_recursively(self, original: Dict, updater: Dict) -> Dict:
        """Update dictionary recursively."""
        for k, v in updater.items():
            if isinstance(v, dict):
                original[k] = self._update_dict_recursively(original.get(k, {}), v)
            else:
                original[k] = v
        return original

    def add_dict(self, *args, **kwargs):
        """
        Add dictionary configuration source to source list.
        *args and **kwargs are passed to :class:`cascade_config.DictConfigSource()`.

        """
        source = DictConfigSource(*args, **kwargs)
        self.sources.append(source)

    def add_argumentparser(self, *args, **kwargs):
        """
        Add argumentparser configuration source to source list.
        *args and **kwargs are passed to :class:`cascade_config.ArgumentParserConfigSource()`.

        """
        source = ArgumentParserConfigSource(*args, **kwargs)
        self.sources.append(source)

    def add_namespace(self, *args, **kwargs):
        """
        Add argparse Namespace configuration source to source list.
        *args and **kwargs are passed to :class:`cascade_config.NamespaceConfigSource()`.
        """
        source = NamespaceConfigSource(*args, **kwargs)
        self.sources.append(source)

    def add_json(self, *args, **kwargs):
        """
        Add JSON configuration source to source list.
        *args and **kwargs are passed to :class:`cascade_config.JSONConfigSource()`.
        """
        source = JSONConfigSource(*args, **kwargs)
        self.sources.append(source)

    def parse(self) -> Dict:
        """Parse all sources, cascade, validate, and return cascaded configuration."""
        config = dict()
        for source in self.sources:
            config = self._update_dict_recursively(config, source.load())

        if self.validation_schema:
            jsonschema.validate(config, self.validation_schema.load())

        return config


class _ConfigSource(ABC):
    """Abstract base class for configuration source."""

    def __init__(self, source, validation_schema=None, subkey=None) -> None:
        """
        Initialize a single configuration source.

        Parameters
        ----------
        source : str, path-like, dict, argparse.ArgumentParser
            source for the configuration, either a dictionary, path to a file, or
            argument parser.
        validation_schema: str, path-like, dict, or cascade_config.ValidationSchema, optional
            JSON Schema to validate single configuration
        subkey : str
            adds the configuration to a subkey of the final cascased configuration;
            e.g. specifying a subkey `"user"` for a configuration source, would add it
            under the key `"user"` in the cascaded configuration, instead of updating
            the root of the existing configuration

        Methods
        -------
        load()
            load the configuration from the source and return it as a dictionary

        """
        self.source = source
        self.validation_schema = validation_schema
        self.subkey = subkey

    @property
    def validation_schema(self):
        """Get validation_schema."""
        return self._validation_schema

    @validation_schema.setter
    def validation_schema(self, value):
        """Set validation schema."""
        if value:
            self._validation_schema = ValidationSchema.from_object(value)
        else:
            self._validation_schema = None

    @abstractmethod
    def _read(self):
        """Read source into dict."""
        pass

    def load(self) -> Dict:
        """Read, validate, and place in subkey if required."""
        if self.subkey:
            config = dict()
            config[self.subkey] = self._read()
        else:
            config = self._read()
        if self.validation_schema:
            jsonschema.validate(config, self.validation_schema.load())
        return config


class DictConfigSource(_ConfigSource):
    """Dictionary configuration source."""

    def _read(self) -> Dict:
        if not isinstance(self.source, dict):
            raise TypeError("DictConfigSource `source` must be a dict")
        return self.source


class JSONConfigSource(_ConfigSource):
    """JSON configuration source."""

    def _read(self) -> Dict:
        if not isinstance(self.source, (str, os.PathLike)):
            raise TypeError(
                "JSONConfigSource `source` must be a string or path-like object"
            )
        with open(self.source, "rt") as json_file:
            config = json.load(json_file)
        return config


class ArgumentParserConfigSource(_ConfigSource):
    """ArgumentParser configuration source."""

    def _read(self) -> Dict:
        if not isinstance(self.source, ArgumentParser):
            raise TypeError(
                "ArgumentParserSource `source` must be an argparse.ArgumentParser object"
            )
        config = vars(self.source.parse_args())
        return config


class NamespaceConfigSource(_ConfigSource):
    """Argparse Namespace configuration source."""

    def _read(self) -> Dict:
        if not isinstance(self.source, Namespace):
            raise TypeError(
                "NamespaceConfigSource `source` must be an argparse.Namespace object"
            )
        config = vars(self.source)
        return config


class ValidationSchema:
    """ValidationSchema."""

    def __init__(self, source):
        """ValidationSchema."""
        self.source = source

    @classmethod
    def from_object(cls, obj):
        """Return ValidationSchema from str, path-like, dict, or ValidationSchema."""
        if isinstance(obj, (str, os.PathLike, Dict)):
            return cls(obj)
        elif isinstance(obj, cls):
            return obj
        else:
            raise TypeError(
                f"Cannot create ValidationSchema from type {type(obj)}. Must be a "
                "string, path-like, dict, or cascade_config.ValidationSchema object"
            )

    def load(self) -> Dict:
        """Load validation schema."""
        if isinstance(self.source, (str, os.PathLike)):
            with open(self.source, "rt") as json_file:
                schema = json.load(json_file)
        elif isinstance(self.source, Dict):
            schema = self.source
        else:
            raise TypeError(
                "ValidationSchema `source` must be of type string, path-like, or dict"
            )
        return schema
