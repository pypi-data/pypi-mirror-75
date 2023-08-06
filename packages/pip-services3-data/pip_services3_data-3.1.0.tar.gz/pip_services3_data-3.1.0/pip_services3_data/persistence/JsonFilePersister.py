# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.JsonFilePersister
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    JSON file persister implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json
import os

from pip_services3_commons.config import IConfigurable
from pip_services3_commons.errors import ConfigException, FileException

from ..ILoader import ILoader
from ..ISaver import ISaver


class JsonFilePersister(ILoader, ISaver, IConfigurable):
    """
    Persistence component that loads and saves data from/to flat file.

    It is used by [[FilePersistence]], but can be useful on its own.

    ### Configuration parameters ###

        - path:          path to the file where data is stored

    Example:
        persister = JsonFilePersister(MyData.class, "./data/data.json")

        persister.save("123", ["A", "B", "C"])
        ...

        persister.load("123", items)
        print items
    """
    path = None

    def __init__(self, path=None):
        """
        Creates a new instance of the persistence.

        :param path: (optional) a path to the file where data is stored.
        """
        self.path = path

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        try:
            if config is not None or config.contains_key("path"):
                self.path = config.get_as_string("path")

        except AttributeError:
            raise ConfigException(None, "NO_PATH", "Data file path is not set")

    def load(self, correlation_id):
        """
        Loads data items from external JSON file.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: loaded items
        """
        # If doesn't exist then consider empty data
        if not os.path.isfile(self.path):
            return []

        try:
            with open(self.path, 'r') as file:
                return json.load(file)
        except Exception as ex:
            raise FileException(correlation_id, "READ_FAILED", "Failed to read data file: " + str(ex)) \
                .with_cause(ex)

    def save(self, correlation_id, entities):
        """
        Saves given data items to external JSON file.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param entities: list if data items to save
        """
        try:
            with open(self.path, 'w') as file:
                json.dump(entities, file)
        except Exception as ex:
            raise FileException(correlation_id, "WRITE_FAILED", "Failed to write data file: " + str(ex)) \
                .with_cause(ex)
