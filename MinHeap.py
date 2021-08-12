from typing import Any, List

class MinHeap:

    def __init__(self, capacity: int = 50):
        """Constructor creating an empty heap with default capacity = 50 but allows heaps of other capacities to be created."""
        self.values: List = [None]*(capacity+1)
        self.keys: List = [0]*(capacity+1)
        self.map = {}   #stores the index of every value
        self.num_items = 0                     

    def insert(self, item: Any, priority: int) -> None:
        """inserts item and priority into the heap
        Raises IndexError if there is no room in the heap"""
        if self.is_full():
            raise IndexError

        self.num_items += 1
        self.values[self.num_items] = item
        self.keys[self.num_items] = priority
        self.map[item] = self.num_items
        self._perc_up(self.num_items)

    def findmin(self) -> Any:
        """returns root of heap (highest priority) without changing the heap
        Raises IndexError if the heap is empty"""
        if self.is_empty():
            raise IndexError

        return self.values[1]

    def extractmin(self) -> Any:
        """returns item at root (highest priority) - removes it from the heap and restores the heap property
           Raises IndexError if the heap is empty"""
        if self.is_empty():
            raise IndexError
        
        root = self.values[1]
        self.values[1] = self.values[self.num_items]
        self.keys[1] = self.keys[self.num_items]
        self.map.pop(root)
        self.map[self.values[1]] = 1
        self.num_items -= 1
        self._perc_down(1)
        return root

    def decreasekey(self, item: Any, new_key: int) -> None:
        """Takes the item whose priority needs to change and the new priority and updates 
        the priority. Restores heap
        Raises ValueError if item not in heap
        O(logn) time"""
        if item not in self.map:
            raise ValueError

        i = self.map[item]
        self.keys[i] = new_key
        self._perc_up(i)

    def is_empty(self) -> bool:
        """returns True if the heap is empty, false otherwise"""
        return self.num_items == 0

    def is_full(self) -> bool:
        """returns True if the heap is full, false otherwise"""
        return self.num_items == self.capacity()

    def capacity(self) -> int:
        """This is the maximum number of a entries the heap can hold, which is
        1 less than the number of entries that the array allocated to hold the heap can hold"""
        return len(self.values) - 1
    
    def size(self) -> int:
        """the actual number of elements in the heap, not the capacity"""
        return self.num_items

    def _perc_down(self,i: int) -> None:
        """where the parameter i is an index in the heap and perc_down moves the element stored
        at that location to its proper place in the heap rearranging elements as it goes."""
        while (i * 2) <= self.size():
            mc_idx = self._min_child(i)

            if self.keys[i] > self.keys[mc_idx]:
                self.values[i], self.values[mc_idx] = self.values[mc_idx], self.values[i]
                self.keys[i], self.keys[mc_idx] = self.keys[mc_idx], self.keys[i]
                self.map[self.values[i]] = i
                self.map[self.values[mc_idx]] = mc_idx

            i = mc_idx

    def _min_child(self, idx: int) -> int:
        """Parameter idx is index of parent node of interest. Returns the index of the minimum child"""
        if idx * 2 + 1 > self.size():
            return idx * 2
        else:
            if self.keys[idx * 2] < self.keys[idx * 2 + 1]:
                return idx * 2
            else: 
                return idx * 2 + 1

    def _perc_up(self,i: int) -> None:
        """where the parameter i is an index in the heap and perc_up moves the element stored
        at that location to its proper place in the heap rearranging elements as it goes."""
        while i // 2 > 0:
            if self.keys[i] < self.keys[i // 2]:
                self.values[i // 2], self.values[i] = self.values[i], self.values[i//2]
                self.keys[i // 2], self.keys[i] = self.keys[i], self.keys[i//2]
                self.map[self.values[i]] = i
                self.map[self.values[i//2]] = i//2
            i = i // 2

