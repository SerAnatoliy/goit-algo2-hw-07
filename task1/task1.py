class DoublyLinkedListNode:
    def __init__(self, key, value):
        self.data = (key, value)
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = DoublyLinkedListNode(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        return new_node

    def remove_last(self):
        if not self.tail:
            return None
        node = self.tail
        if self.tail.prev:
            self.tail.prev.next = None
        self.tail = self.tail.prev
        if not self.tail:
            self.head = None
        return node

    def move_to_front(self, node):
        if node is self.head:
            return
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node


def range_sum_no_cache(array: list, L: int, R: int):
    return sum(array[L:R + 1])


def update_no_cache(array: list, index: int, value: int):
    array[index] = value


def range_sum_with_cache(array: list, L: int, R: int):
    cache_key = (L, R)
    cached_value = lru_cache.get(cache_key)
    if cached_value != -1:
        return cached_value
    result = sum(array[L:R + 1])
    lru_cache.put(cache_key, result)
    return result


def update_with_cache(array: list, index: int, value: int):
    array[index] = value
    invalid_keys = [key for key in lru_cache.cache if key[0] <= index <= key[1]]
    for key in invalid_keys:
        del lru_cache.cache[key]
    lru_cache.list = DoublyLinkedList()


lru_cache = LRUCache(1000)