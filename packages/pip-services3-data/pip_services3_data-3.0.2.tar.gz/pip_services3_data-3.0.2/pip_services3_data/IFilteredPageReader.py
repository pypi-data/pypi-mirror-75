# -*- coding: utf-8 -*-
"""
    pip_services3_data.IFilteredPageReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for filtered paging data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IFilteredPageReader:
    """
    Interface for data processing components that can retrieve a page of data items by a filter.
    """
    def get_page_by_filter(self, correlation_id, filter, paging, sort = None):
        """
        Gets a page of data items using filter parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) filter parameters

        :param paging: (optional) paging parameters

        :param sort: (optional) sort parameters

        :return: list of items
        """
        raise NotImplementedError('Method from interface definition')
