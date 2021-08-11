from MinHeap import MinHeap
from typing import Any

class PriorityQueue:
    """Priority Queue"""
    def __init__(self, capacity: int =50) -> None:
        """Binary minimum heap implementation. Default capacity is 50"""
        self.q = MinHeap(capacity)

    def enqueue(self, item: Any, priority: int) -> None:
        """Inserts an item and its priority into the queue. If item already in
        the queue, updates priority"""
        if item in self.q.map:
            self.decreasekey(item, priority)
        else:
            self.q.insert(item,priority)

    def peek(self) -> Any:
        """returns the item at the front of the queue without removing"""
        return self.q.findmin()
    
    def dequeue(self) -> Any:
        """Removes and returns the item at the front of the queue """
        return self.q.extractmin()

    def decreasekey(self,item: Any, new_prio: int) -> None:
        """Takes the item and its priority to be changed to. Restores order based on priority"""
        self.q.decreasekey(item,new_prio)

    def is_empty(self) -> bool:
        """Returns a boolean whether the queue is empty or not"""
        return self.q.is_empty()

