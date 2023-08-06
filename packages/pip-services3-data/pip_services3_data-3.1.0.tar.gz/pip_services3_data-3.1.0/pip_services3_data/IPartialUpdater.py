# -*- coding: utf-8 -*-
"""
    pip_services3_data.IPartialUpdater
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for partial data updaters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IPartialUpdater:
    """
    Interface for data processing components to update data items partially.
    """
    def update_partially(self, correlation_id, id, data):
        """
        Updates only few selected fields in a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be updated.

        :param data: a map with fields to be updated.

        :return: updated item
        """
        raise NotImplementedError('Method from interface definition')
