from bisect import insort
from collections import deque

## to store codes for huffman coding
class CodeHeap():
    def __init__(self):
        self._container = deque([])

    def push(self, item):
        insort(self._container, item)  # in by sort

    def pop(self):
        return self._container.popleft()  # FIFO

    def __getitem__(self, item):
        return self._container[item]

    def __len__(self):
        return len(self._container)

    def __repr__(self):
        return repr(self._container)
