# -*- coding: utf-8 -*-
"""
    pip_services3_data.IQuerablePageReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for querable paging data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IQuerablePageReader:
    """
    Interface for data processing components that can query a page of data items.
    """
    def get_page_by_query(self, correlation_id, query, paging, sort = None):
        """
        Gets a page of data items using a query string.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param query: (optional) a query string

        :param paging: (optional) paging parameters

        :param sort: (optional) sort parameters

        :return: list of items
        """
        raise NotImplementedError('Method from interface definition')
