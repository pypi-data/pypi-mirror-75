# -*- coding: utf-8 -*-
"""
    pip_services3_data.IFilteredReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for filtered data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IFilteredReader:
    """
    Interface for data processing components that can retrieve a list of data items by filter.
    """
    def get_list_by_filter(self, correlation_id, filter, sort = None):
        """
        Gets a list of data items using filter parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) filter parameters

        :param paging: (optional) paging parameters

        :return: list of items
        """
        raise NotImplementedError('Method from interface definition')
