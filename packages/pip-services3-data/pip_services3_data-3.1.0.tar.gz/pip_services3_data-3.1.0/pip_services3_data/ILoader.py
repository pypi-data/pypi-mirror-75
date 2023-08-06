# -*- coding: utf-8 -*-
"""
    pip_services3_data.ILoader
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data loaders.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ILoader:
    """
    Interface for data processing components that load data items.
    """
    def load(self, correlation_id):
        """
        Loads data items.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a list of data items
        """
        raise NotImplementedError('Method from interface definition')
