#!/usr/bin/python3
"""LFU caching.
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class.
    """
    
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.queue = []
        self.count = {}
    
    def put(self, key, item):
        """Put method.
        """
        pass
                
        
    def get(self, key):
        """Get method.
        """
        if key in self.cache_data:
            self.mru = key
            return self.cache_data[key]
        return None
