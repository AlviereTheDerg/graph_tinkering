
from operator import lt

class IPQ:
    """
    Indexed Priority Queue in the form of a map
    Can store hashable key values with integer priority values as a minimum priority queue
    A given key can only hold a single priority value
    """

    def __init__(self):
        self._heap = []
        self._indexes = {}
        self._priorities = {}
        self._compare = lt
    
    #helper methods
    def _swap(self, first_index, second_index):
        first_key = self._heap[first_index]
        second_key = self._heap[second_index]
        
        self._heap[first_index], self._heap[second_index] = self._heap[second_index], self._heap[first_index]
        self._indexes[first_key], self._indexes[second_key] = self._indexes[second_key], self._indexes[first_key]
    
    def _siftup(self, index):
        while index > 0:
            parent = index // 2
            if self._compare(self._priorities[self._heap[index]], self._priorities[self._heap[parent]]):
                self._swap(parent, index)
                index = parent
            else:
                break
    
    def _siftdown(self, index):
        pass
    
    # internal put vs update_key
    def _put(self, key, value):
        self._indexes[key] = len(self._heap)
        self._heap.append(key)
        self._priorities[key] = value
        self._siftup(self._indexes[key])
    
    def _update_key(self, key, new_value):
        pass
    
    #PQ methods
    def peek(self):
        return self._heap[0]

    def pop(self):
        pass

    def put(self, key, value):
        if key not in self._indexes:
            self._put(key, value)

    #IPQ method
    def update_key(self, key, new_value):
        pass