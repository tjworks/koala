"""This is ItemManager
"""
from koala.managers.BaseManager import BaseManager
class ItemManager(BaseManager):
    """Manager class for item related functions
    
    """
    def add(self, item):        
        """Add a new item

        Should not be called directly by application developers - see
        :meth:`~koala.managers.ItemManager.ItemManager.update` instead.

        .. mongodoc:: cursors        
        """
        pass
    
    def update(self, item):
        """Update item 
        
        
        What else?
        .. versionchanged:: 1.0
           ``full_name`` is now a property rather than a method.
        """
        pass