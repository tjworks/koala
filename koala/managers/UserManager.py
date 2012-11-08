"""This is UserManager
"""
from koala.managers.BaseManager import BaseManager
class UserManager(BaseManager):
    """Manager class for item related functions
    
    """
    def add(self, item):        
        """Add a new user

        Should not be called directly by application developers - see
        :meth:`~koala.managers.ItemManager.ItemManager.update` instead.

        .. mongodoc:: cursors        
        """
        pass
    
    def update(self, item):
        """Update user 
        
        
        What else?
        .. versionchanged:: 1.0
           ``full_name`` is now a property rather than a method.
        """
        pass