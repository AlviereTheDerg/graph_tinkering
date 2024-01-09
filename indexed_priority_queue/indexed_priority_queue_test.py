
import unittest
if __name__ == '__main__':
    from indexed_priority_queue import IPQ
else:
    from indexed_priority_queue.indexed_priority_queue import IPQ

class IPQ_initialization_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["IMPORTANT","things","others","stuff","dishes"]
        self.priorities_data = {"others":4,"IMPORTANT":1,"dishes":float('inf'),"stuff":3,"things":2}
    
    def test_no_params(self):
        ipq = IPQ()
        self.assertEqual(0, len(ipq._heap))
        self.assertEqual(0, len(ipq._indexes))
        self.assertEqual(0, len(ipq._priorities))

    def test_import_single_priority(self):
        ipq = IPQ({self.heap_data[0]:self.priorities_data[self.heap_data[0]]})

        # check the lengths
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check the contents
        self.assertEqual(self.heap_data[0], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[self.heap_data[0]])
        self.assertEqual(self.priorities_data[self.heap_data[0]], ipq._priorities[self.heap_data[0]])

    def test_import_two_priority(self):
        ipq = IPQ({item:self.priorities_data[item] for item in self.heap_data[0:2]})

        # check the lengths
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check the contents
        for index,item in enumerate(self.heap_data[0:2]): 
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_import_three_priority(self):
        ipq = IPQ({item:self.priorities_data[item] for item in self.heap_data[0:3]})

        # check the lengths
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check the contents
        for index,item in enumerate(self.heap_data[0:3]): 
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_import_five_priority(self):
        ipq = IPQ(self.priorities_data)

        # check the lengths
        self.assertEqual(5, len(ipq._heap))
        self.assertEqual(5, len(ipq._indexes))
        self.assertEqual(5, len(ipq._priorities))

        # check the heaps have the same/correct contents
        self.assertEqual(set(self.heap_data), set(ipq._heap))
        self.assertEqual(self.priorities_data, ipq._priorities)
        self.assertEqual(self.priorities_data.keys(), ipq._indexes.keys())
        self.assertEqual([ipq._indexes[item] for item in ipq._heap], list(range(5)))

        # check the contents are in order
        self.assertEqual(self.heap_data[0], ipq._heap[0]) # minimum priority item
        for index,item in enumerate(ipq._heap[1:], start=1):
            self.assertTrue(self.priorities_data[ipq._heap[(index-1)//2]] <= self.priorities_data[item])
    
    def test_import_disconnect_input_dict(self):
        ipq = IPQ(self.priorities_data)
        old_priorities = self.priorities_data.copy()
        self.priorities_data = {item:0 for item in self.priorities_data}

        # check the lengths
        self.assertEqual(5, len(ipq._heap))
        self.assertEqual(5, len(ipq._indexes))
        self.assertEqual(5, len(ipq._priorities))

        # check the heaps have the same/correct contents
        self.assertEqual(set(self.heap_data), set(ipq._heap))
        self.assertEqual(old_priorities, ipq._priorities)
        self.assertEqual(self.priorities_data.keys(), ipq._indexes.keys())
        self.assertEqual([ipq._indexes[item] for item in ipq._heap], list(range(5)))

        # check the contents are in order
        self.assertEqual(self.heap_data[0], ipq._heap[0]) # minimum priority item
        for index,item in enumerate(ipq._heap[1:], start=1):
            self.assertTrue(old_priorities[ipq._heap[(index-1)//2]] <= old_priorities[item])


class IPQ_swap_function_tests(unittest.TestCase):
    def setUp(self):
        self.basic_ipq = IPQ()
        self.basic_ipq._heap = ["stuff","things","others","IMPORTANT"]
        self.basic_ipq._indexes = {item:index for index,item in enumerate(self.basic_ipq._heap)}
    
    def test_swap_once(self):
        start_heap = self.basic_ipq._heap.copy()

        self.basic_ipq._swap(1,3)
        # those that shouldn't be touched
        self.assertEqual(start_heap[0], self.basic_ipq._heap[0])
        self.assertEqual(start_heap[2], self.basic_ipq._heap[2])
        self.assertEqual(0, self.basic_ipq._indexes[start_heap[0]])
        self.assertEqual(2, self.basic_ipq._indexes[start_heap[2]])

        # those that SHOULD be touched
        self.assertEqual(start_heap[1], self.basic_ipq._heap[3])
        self.assertEqual(start_heap[3], self.basic_ipq._heap[1])
        self.assertEqual(1, self.basic_ipq._indexes[start_heap[3]])
        self.assertEqual(3, self.basic_ipq._indexes[start_heap[1]])
    
    def test_swap_with_itself(self):
        start_heap = self.basic_ipq._heap.copy()

        self.basic_ipq._swap(1,1)
        # those that shouldn't be touched
        for index in range(4):
            self.assertEqual(start_heap[index], self.basic_ipq._heap[index])
            self.assertEqual(index, self.basic_ipq._indexes[start_heap[index]])
    
    def test_two_disparate_swaps(self):
        start_heap = self.basic_ipq._heap.copy()

        self.basic_ipq._swap(1,3)
        self.basic_ipq._swap(0,2)
        self.assertEqual(start_heap[0], self.basic_ipq._heap[2])
        self.assertEqual(start_heap[1], self.basic_ipq._heap[3])
        self.assertEqual(start_heap[2], self.basic_ipq._heap[0])
        self.assertEqual(start_heap[3], self.basic_ipq._heap[1])
        self.assertEqual(0, self.basic_ipq._indexes[start_heap[2]])
        self.assertEqual(1, self.basic_ipq._indexes[start_heap[3]])
        self.assertEqual(2, self.basic_ipq._indexes[start_heap[0]])
        self.assertEqual(3, self.basic_ipq._indexes[start_heap[1]])
    
    def test_two_overlapping_swaps(self):
        start_heap = self.basic_ipq._heap.copy()

        self.basic_ipq._swap(1,3)
        self.basic_ipq._swap(1,2)
        self.assertEqual(start_heap[0], self.basic_ipq._heap[0])
        self.assertEqual(start_heap[1], self.basic_ipq._heap[3])
        self.assertEqual(start_heap[2], self.basic_ipq._heap[1])
        self.assertEqual(start_heap[3], self.basic_ipq._heap[2])
        self.assertEqual(0, self.basic_ipq._indexes[start_heap[0]])
        self.assertEqual(1, self.basic_ipq._indexes[start_heap[2]])
        self.assertEqual(2, self.basic_ipq._indexes[start_heap[3]])
        self.assertEqual(3, self.basic_ipq._indexes[start_heap[1]])

class IPQ_siftup_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["stuff","things","others","IMPORTANT"]
        self.priorities_data = {"stuff":3,"things":2,"others":4,"IMPORTANT":1}
    
    def test_siftup_single_item(self):
        ipq = IPQ()
        ipq._heap.append(self.heap_data[0])
        ipq._indexes[self.heap_data[0]] = 0
        ipq._priorities[self.heap_data[0]] = self.priorities_data[self.heap_data[0]]

        ipq._siftup(0) # no crash
        # check that the lengths are untouched
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that the item info stays
        self.assertEqual(self.heap_data[0], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[ipq._heap[0]])
        self.assertEqual(self.priorities_data[self.heap_data[0]], ipq._priorities[self.heap_data[0]])

    def test_siftup_root(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[1::-1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(0) # no crash
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info stays
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftup_two_preorder(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[1::-1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(1)
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info stays
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftup_two_out_of_order_leaf(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(1)
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info stays
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftup_four_out_of_order_branch(self):
        ipq = IPQ()
        ipq._heap = self.heap_data.copy()
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(1)
        # check that the lengths are untouched
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that the item info stays
        for ipq_index,index in enumerate([1,0,2,3]):
            item = self.heap_data[index]
            self.assertEqual(item, ipq._heap[ipq_index], index)
            self.assertEqual(ipq_index, ipq._indexes[item], index)
            self.assertEqual(self.priorities_data[item], ipq._priorities[item], index)
    
    def test_siftup_four_out_of_order_leaf(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [1,0,2,3]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(3)
        # check that the lengths are untouched
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that the item info stays
        for ipq_index,index in enumerate([3,1,2,0]):
            item = self.heap_data[index]
            self.assertEqual(item, ipq._heap[ipq_index], index)
            self.assertEqual(ipq_index, ipq._indexes[item], index)
            self.assertEqual(self.priorities_data[item], ipq._priorities[item], index)
    
    def test_siftup_four_stop_at_branch(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [3,0,2,1]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftup(3)
        # check that the lengths are untouched
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that the item info stays
        for ipq_index,index in enumerate([3,1,2,0]):
            item = self.heap_data[index]
            self.assertEqual(item, ipq._heap[ipq_index], index)
            self.assertEqual(ipq_index, ipq._indexes[item], index)
            self.assertEqual(self.priorities_data[item], ipq._priorities[item], index)

    def test_siftup_no_difference(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:1 for item in ipq._heap}

        ipq._siftdown(1)
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate(self.heap_data[0:2]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(1, ipq._priorities[item])

class IPQ_siftdown_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["stuff","things","others","IMPORTANT"]
        self.priorities_data = {"stuff":3,"things":2,"others":4,"IMPORTANT":1}
    
    def test_siftdown_single_item(self):
        ipq = IPQ()
        ipq._heap.append(self.heap_data[0])
        ipq._indexes[self.heap_data[0]] = 0
        ipq._priorities[self.heap_data[0]] = self.priorities_data[self.heap_data[0]]

        ipq._siftdown(0) # no crash
        # check that the lengths are untouched
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that the item info stays
        self.assertEqual(self.heap_data[0], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[ipq._heap[0]])
        self.assertEqual(self.priorities_data[self.heap_data[0]], ipq._priorities[self.heap_data[0]])
    
    def test_siftdown_leaf(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(1) # no crash
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info stays the same
        for index,item in enumerate(self.heap_data[0:2]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_partial_full_root_preorder(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[1::-1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_partial_full_root_out_of_order(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_full_root_preorder(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [1,0,2]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info stays the same
        for index,item in enumerate([1,0,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_full_root_left_swap(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,0,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_full_root_right_swap(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [0,2,1]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,2,0]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_full_worst_root_left_child_better(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [2,1,0]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,2,0]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_siftdown_full_worst_root_right_child_better(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [2,0,1]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,0,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

    def test_siftdown_move_down_partially_full_branch(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [0,1,2,3]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,3,2,0]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

    def test_siftdown_move_down_to_upper_leaf(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [0,2,1,3]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate([1,2,0,3]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

    def test_siftdown_no_difference(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:1 for item in ipq._heap}

        ipq._siftdown(0)
        # check that the lengths are untouched
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that the item info is correct
        for index,item in enumerate(self.heap_data[0:3]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(1, ipq._priorities[item])


class IPQ_internal_put_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["stuff","things","others","IMPORTANT"]
        self.priorities_data = {"stuff":3,"things":2,"others":4,"IMPORTANT":1}
    
    def test_put_one_item(self):
        ipq = IPQ()
        ipq._put(self.heap_data[0], self.priorities_data[self.heap_data[0]])

        # check that the lengths were incremented
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that the items were added correctly
        self.assertEqual(self.heap_data[0], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[ipq._heap[0]])
        self.assertEqual(self.priorities_data[self.heap_data[0]], ipq._priorities[self.heap_data[0]])
    
    def test_put_two_items_preordered(self):
        ipq = IPQ()
        ipq._put(self.heap_data[1], self.priorities_data[self.heap_data[1]])
        ipq._put(self.heap_data[0], self.priorities_data[self.heap_data[0]])

        # check that the lengths were incremented
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that both items were added with their correct priorities, disregarding order
        for item in self.heap_data[0:2]:
            self.assertIn(item, ipq._heap)
            self.assertIn(item, ipq._indexes)
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

        # check that the items are ordered correctly
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
    
    def test_put_two_items_out_of_order(self):
        ipq = IPQ()
        ipq._put(self.heap_data[0], self.priorities_data[self.heap_data[0]])
        ipq._put(self.heap_data[1], self.priorities_data[self.heap_data[1]])

        # check that the lengths were incremented
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that both items were added with their correct priorities, disregarding order
        for item in self.heap_data[0:2]:
            self.assertIn(item, ipq._heap)
            self.assertIn(item, ipq._indexes)
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

        # check that the items are ordered correctly
        for index,item in enumerate(self.heap_data[1::-1]):
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])

class IPQ_internal_update_key_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["IMPORTANT","things","others","stuff"]
        self.priorities_data = {"stuff":3,"things":2,"others":4,"IMPORTANT":1}

        self.ipq = IPQ()
        self.ipq._priorities = self.priorities_data.copy()
        self.ipq._heap = self.heap_data.copy()
        self.ipq._indexes = {item:index for index,item in enumerate(self.ipq._heap)}
    
    def test_update_key_decrease_root(self):
        previous_indexes = self.ipq._indexes.copy()
        self.ipq._update_key(self.ipq._heap[0], self.priorities_data[self.ipq._heap[0]]-1)

        self.assertEqual(self.heap_data, self.ipq._heap)
        self.assertEqual(previous_indexes, self.ipq._indexes)
        self.assertEqual(self.priorities_data[self.ipq._heap[0]]-1, self.ipq._priorities[self.ipq._heap[0]])
        for key in self.priorities_data.keys() - {self.ipq._heap[0]}:
            self.assertEqual(self.priorities_data[key], self.ipq._priorities[key], key)
    
    def test_update_key_increase_root_but_not_order_changing(self):
        previous_indexes = self.ipq._indexes.copy()
        self.ipq._update_key(self.ipq._heap[0], self.priorities_data[self.ipq._heap[0]]+1)

        self.assertEqual(self.heap_data, self.ipq._heap)
        self.assertEqual(previous_indexes, self.ipq._indexes)
        self.assertEqual(self.priorities_data[self.ipq._heap[0]]+1, self.ipq._priorities[self.ipq._heap[0]])
        for key in self.priorities_data.keys() - {self.ipq._heap[0]}:
            self.assertEqual(self.priorities_data[key], self.ipq._priorities[key], key)
    
    def test_update_key_decrease_leaf_but_not_order_changing(self):
        previous_indexes = self.ipq._indexes.copy()
        self.ipq._update_key(self.ipq._heap[2], self.priorities_data[self.ipq._heap[2]]-1)

        self.assertEqual(self.heap_data, self.ipq._heap)
        self.assertEqual(previous_indexes, self.ipq._indexes)
        self.assertEqual(self.priorities_data[self.ipq._heap[2]]-1, self.ipq._priorities[self.ipq._heap[2]])
        for key in self.priorities_data.keys() - {self.ipq._heap[2]}:
            self.assertEqual(self.priorities_data[key], self.ipq._priorities[key], key)
    
    def test_update_key_increase_leaf(self):
        previous_indexes = self.ipq._indexes.copy()
        self.ipq._update_key(self.ipq._heap[2], self.priorities_data[self.ipq._heap[2]]+1)

        self.assertEqual(self.heap_data, self.ipq._heap)
        self.assertEqual(previous_indexes, self.ipq._indexes)
        self.assertEqual(self.priorities_data[self.ipq._heap[2]]+1, self.ipq._priorities[self.ipq._heap[2]])
        for key in self.priorities_data.keys() - {self.ipq._heap[2]}:
            self.assertEqual(self.priorities_data[key], self.ipq._priorities[key], key)

class IPQ_pop_tests(unittest.TestCase):
    def setUp(self):
        self.heap_data = ["IMPORTANT","things","others","stuff","dishes"]
        self.priorities_data = {"IMPORTANT":1,"things":2,"others":4,"stuff":3,"dishes":float('inf')}

    def test_pop_empty(self):
        ipq = IPQ()
        self.assertRaises(IndexError, ipq.pop)
    
    def test_pop_one_from_one_entry(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop()
        # check that the lengths were affected
        self.assertEqual(0, len(ipq._heap))
        self.assertEqual(0, len(ipq._indexes))
        self.assertEqual(0, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)
    
    def test_pop_one_from_two_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop()
        # check that the lengths were affected
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        self.assertEqual(self.heap_data[1], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[self.heap_data[1]])
        self.assertEqual(self.priorities_data[self.heap_data[1]], ipq._priorities[self.heap_data[1]])
    
    def test_pop_one_from_three_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop()
        # check that the lengths were affected
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        for index,item in enumerate([1,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_one_from_four_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:4]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop()
        # check that the lengths were affected
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        for index,item in enumerate([1,3,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_non_present(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        self.assertRaises(KeyError, ipq.pop, key=self.heap_data[1])
    
    def test_pop_key_one_from_one_entry(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:1]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[0])
        # check that the lengths were affected
        self.assertEqual(0, len(ipq._heap))
        self.assertEqual(0, len(ipq._indexes))
        self.assertEqual(0, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)
    
    def test_pop_key_root_from_two_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[0])
        # check that the lengths were affected
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        self.assertEqual(self.heap_data[1], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[self.heap_data[1]])
        self.assertEqual(self.priorities_data[self.heap_data[1]], ipq._priorities[self.heap_data[1]])
    
    def test_pop_key_leaf_from_two_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:2]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[1])
        # check that the lengths were affected
        self.assertEqual(1, len(ipq._heap))
        self.assertEqual(1, len(ipq._indexes))
        self.assertEqual(1, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[1], value)

        # check the remaining values
        self.assertEqual(self.heap_data[0], ipq._heap[0])
        self.assertEqual(0, ipq._indexes[self.heap_data[0]])
        self.assertEqual(self.priorities_data[self.heap_data[0]], ipq._priorities[self.heap_data[0]])
    
    def test_pop_key_root_from_three_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[0])
        # check that the lengths were affected
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        for index,item in enumerate([1,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_left_leaf_from_three_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[1])
        # check that the lengths were affected
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[1], value)

        # check the remaining values
        for index,item in enumerate([0,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_right_leaf_from_three_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:3]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[2])
        # check that the lengths were affected
        self.assertEqual(2, len(ipq._heap))
        self.assertEqual(2, len(ipq._indexes))
        self.assertEqual(2, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[2], value)

        # check the remaining values
        for index,item in enumerate([0,1]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_root_from_four_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:4]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[0])
        # check that the lengths were affected
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[0], value)

        # check the remaining values
        for index,item in enumerate([1,3,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_high_leaf_from_four_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:4]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[2])
        # check that the lengths were affected
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[2], value)

        # check the remaining values
        for index,item in enumerate([0,1,3]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_low_leaf_from_four_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:4]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[3])
        # check that the lengths were affected
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[3], value)

        # check the remaining values
        for index,item in enumerate([0,1,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_branch_from_four_entries(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:4]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[1])
        # check that the lengths were affected
        self.assertEqual(3, len(ipq._heap))
        self.assertEqual(3, len(ipq._indexes))
        self.assertEqual(3, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[1], value)

        # check the remaining values
        for index,item in enumerate([0,3,2]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_branch_from_five_entries_first_order(self):
        ipq = IPQ()
        ipq._heap = self.heap_data[0:5]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[1])
        # check that the lengths were affected
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[1], value)

        # check the remaining values
        for index,item in enumerate([0,3,2,4]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])
    
    def test_pop_key_branch_from_five_entries_second_order(self):
        ipq = IPQ()
        ipq._heap = [self.heap_data[index] for index in [0,1,2,4,3]]
        ipq._indexes = {item:index for index,item in enumerate(ipq._heap)}
        ipq._priorities = {item:self.priorities_data[item] for item in ipq._heap}

        value = ipq.pop(self.heap_data[1])
        # check that the lengths were affected
        self.assertEqual(4, len(ipq._heap))
        self.assertEqual(4, len(ipq._indexes))
        self.assertEqual(4, len(ipq._priorities))

        # check that pop result was correct
        self.assertEqual(self.heap_data[1], value)

        # check the remaining values
        for index,item in enumerate([0,3,2,4]):
            item = self.heap_data[item]
            self.assertEqual(item, ipq._heap[index])
            self.assertEqual(index, ipq._indexes[item])
            self.assertEqual(self.priorities_data[item], ipq._priorities[item])

if __name__ == '__main__':
    unittest.main()