# -*- coding: utf-8 -*-
"""
    pip_services3_data.IGetter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data getters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IGetter:
    """
    Interface for data processing components that can get data items.
    """
    def get_one_by_id(self, correlation_id, id):
        """
        Gets a data items by its unique id.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param id: an id of item to be retrieved.

        :return: an item by its id.
        """
        raise NotImplementedError('Method from interface definition')
