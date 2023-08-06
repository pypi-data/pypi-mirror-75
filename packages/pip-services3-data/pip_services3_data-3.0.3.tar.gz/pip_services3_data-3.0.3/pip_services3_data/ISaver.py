# -*- coding: utf-8 -*-
"""
    pip_services3_data.ISaver
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data saver.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ISaver:
    """
    Interface for data processing components that save data items.
    """
    def save(self, correlation_id, items):
        """
        Saves given data items.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param items: a list of items to save.
        """
        raise NotImplementedError('Method from interface definition')
