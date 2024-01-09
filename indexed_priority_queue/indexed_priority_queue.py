
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
        while True:
            l,r = index*2+1, index*2+2
            match   l < len(self._heap) and self._compare(self._priorities[self._heap[l]], self._priorities[self._heap[index]]), \
                    r < len(self._heap) and self._compare(self._priorities[self._heap[r]], self._priorities[self._heap[index]]):
                case False, False:
                    break
                case False, True:
                    switch_with = r
                case True, False:
                    switch_with = l
                case True, True:
                    switch_with = l if self._compare(self._priorities[self._heap[l]], self._priorities[self._heap[r]]) else r
            self._swap(index, switch_with)
            index = switch_with
    
    # internal put vs update_key
    def _put(self, key, value):
        self._indexes[key] = len(self._heap)
        self._heap.append(key)
        self._priorities[key] = value
        self._siftup(self._indexes[key])
    
    def _update_key(self, key, new_value):
        old_value = self._priorities[key]
        self._priorities[key] = new_value
        if self._compare(old_value, new_value): # if new value is worse
            self._siftdown(self._indexes[key])
        else:
            self._siftup(self._indexes[key])

    # route between _put and _update_key
    def _route_KV(self, key, value):
        if key not in self._indexes:
            self._put(key, value)
        else:
            self._update_key(key, value)
    
    #PQ methods
    def peek(self):
        return self._heap[0]

    def pop(self):
        self._swap(0,-1)
        result = self._heap.pop()
        del self._priorities[result]
        del self._indexes[result]
        self._siftdown(0)
        return result

    def put(self, key, value):
        self._route_KV(key, value)

    #IPQ method
    def update_key(self, key, new_value):
        self._route_KV(key, new_value)