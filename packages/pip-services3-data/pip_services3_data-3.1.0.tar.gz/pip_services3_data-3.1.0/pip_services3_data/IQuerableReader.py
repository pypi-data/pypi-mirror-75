# -*- coding: utf-8 -*-
"""
    pip_services3_data.IQuerableReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for querable data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IQuerableReader:
    """
    Interface for data processing components that can query a list of data items.
    """
    def get_list_by_query(self, correlation_id, query, sort = None):
        """
        Gets a list of data items using a query string.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param query: (optional) a query string

        :param sort: (optional) sort parameters

        :return: list of items
        """
        raise NotImplementedError('Method from interface definition')
