# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import threading

from pip_services3_commons.config import IConfigurable, IReconfigurable, ConfigParams
from pip_services3_commons.refer import IReferenceable, IReferences
from pip_services3_commons.data import PagingParams, DataPage
from pip_services3_commons.run import IOpenable, IClosable, ICleanable
from pip_services3_components.log import CompositeLogger
from pip_services3_commons.data import PagingParams, DataPage, IdGenerator

# This function will be overriden in the code
filtered = filter

class MemoryPersistence(IConfigurable, IReferenceable, IOpenable, ICleanable):
    """
    Abstract persistence component that stores data in memory.

    This is the most basic persistence component that is only
    able to store data items of any type. Specific CRUD operations
    over the data items must be implemented in child classes by
    accessing <code>this._items</code> property and calling
    [[save]] method.

    The component supports loading and saving items from another
    data source. That allows to use it as a base class for file
    and other types of persistence components that cache all data
    in memory.

    ### References ###
        - *:logger:*:*:1.0   (optional) ILogger components to pass log messages

    Example:
        class MyMemoryPersistence(MemoryPersistence):

            def get_by_name(self, correlationId, name):
                item = self.find(name)
                ...
                return item

        persistence = MyMemoryPersistence()

        persistence.set("123", MyData("ABC"))
        print str(persistence.get_by_name("123", "ABC")))
    """
    _logger = None
    _items = None
    _loader = None
    _saver = None
    _lock = None
    _opened = False

    def __init__(self, loader = None, saver = None):
        """
        Creates a new instance of the persistence.

        :param loader: (optional) a loader to load items from external datasource.

        :param saver: (optional) a saver to save items to external datasource.
        """
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._items = []
        self._loader = loader
        self._saver = saver

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._max_page_size = config.get_as_integer_with_default("options.max_page_size", self._max_page_size)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)

    def is_opened(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, correlation_id: str):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.load(correlation_id)
        self._opened = True

    def close(self, correlation_id: str):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.save(correlation_id)
        self._opened = False

    # TODO: not exists into nodejs
    def _convert_to_public(self, value):
        return value

    # TODO: not exists into nodejs
    def _convert_from_public(self, value):
        return value

    def load(self, correlation_id: str):
        if self._loader == None: return

        self._lock.acquire()
        try:
            items = self._loader.load(correlation_id)
            self._items = []
            for item in items:
                item = self._convert_to_public(item)
                self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Loaded " + str(len(self._items)) + " items")

    def save(self, correlation_id: str):
        """
        Saves items to external data source using configured saver component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self._saver == None: return

        self._lock.acquire()
        try:
            items = []
            for item in self._items:
                item = self._convert_from_public(item)
                items.append(item)
            self._saver.save(correlation_id, items)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Saved " + str(len(self._items)) + " items")

    def clear(self, correlation_id: str):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._lock.acquire()
        
        try:
            del self._items[:]
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Cleared items")

        # Outside of lock to avoid reentry
        self.save(correlation_id)


    def create(self, correlation_id: str, item):
        """
        Creates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param item: an item to be created.

        :return: a created item
        """
        self._lock.acquire()
        try:
            self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Created " + str(item))

        # Avoid reentry
        self.save(correlation_id)
        return item


    def get_page_by_filter(self, correlation_id: str, filter, paging: PagingParams, sort = None, select = None) -> DataPage:
        """
        Gets a page of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public getPageByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param paging: (optional) paging parameters

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data page of result by filter.
        """
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()
            
        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))
        if not (sort is None):
            items = list(items.sort(key=sort))
            # items = sorted(items, sort)

        # Prepare paging parameters
        paging = paging if not (paging is None) else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        
        # Get a page
        data = items
        if skip > 0:
            data = data[skip:]
        if take > 0:
            data = data[:take+1]
                
        # Convert values
        if not (select is None):
            data = map(select, data)
                
        self._logger.trace(correlation_id, "Retrieved " + str(len(data)) + " items")

        # Return a page
        return DataPage(data, len(items))


    def get_list_by_filter(self, correlation_id: str, filter, sort = None, select = None) -> list:
        """
        Gets a list of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public getListByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data list of results by filter.
        """
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()

        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))
        if not (sort is None):
            items = list(sorted(items, key=sort))
                        
        # Convert values      
        if not (select is None):
            items = map(select, items)
                
        # Return a list
        return list(items)

    def get_count_by_filter(self, correlation_id: str, filter) -> int:
 
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()

        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))
 
        self._logger.trace(correlation_id, f"Retrieved {len(items)} items")
                
        # Return a list
        return len(items)


    def get_one_random(self, correlation_id: str):
        """
        Gets a random item from items that match to a given filter.

        This method shall be called by a public getOneRandom method from child class
        that receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a random item.
        """
        self._lock.acquire()
        try:
            if len(self._items) == 0:
                return None

            index = random.randint(0, len(self._items))
            item = self._items[index]
        finally:
            self._lock.release()
            
        if not (item is None):
            self._logger.trace(correlation_id, "Retrieved a random item")
        else:
            self._logger.trace(correlation_id, "Nothing to return as random item")
                        
        return item


    def delete_by_filter(self, correlation_id: str, filter):
        """
        Deletes data items that match to a given filter.

        This method shall be called by a public deleteByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items.
        """
        def negative_filter(item):
            return not filter(item)

        old_length = len(list(self._items))

        self._lock.acquire()
        try:
            self._items = list(filtered(negative_filter, self._items))
        finally:
            self._lock.release()
        deleted = old_length - len(list(self._items))
        self._logger.trace(correlation_id, "Deleted " + str(deleted) + " items")

        if (deleted > 0):
            self.save(correlation_id)
