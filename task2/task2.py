import sys

sys.setrecursionlimit(3000)

import timeit
from functools import lru_cache

import matplotlib.pyplot as plt


class SplayTreeNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = SplayTreeNode(key, value, current_node)
        elif key > current_node.key:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = SplayTreeNode(key, value, current_node)
        else:
            current_node.value = value

    def search(self, key):
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n < 2:
        return n
    result = tree.search(n)
    if result is not None:
        return result
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val


def main():
    test_values = list(range(0, 1001, 50))
    repetitions = 5
    lru_times = []
    splay_times = []

    for val in test_values:
        lru_time = timeit.timeit(lambda: fibonacci_lru(val), number=repetitions)
        lru_avg = lru_time / repetitions
        lru_times.append(lru_avg)

        def splay_call():
            t = SplayTree()
            return fibonacci_splay(val, t)

        splay_time = timeit.timeit(splay_call, number=repetitions)
        splay_avg = splay_time / repetitions
        splay_times.append(splay_avg)

    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
    print("-" * 60)
    for n, lt, st in zip(test_values, lru_times, splay_times):
        print(f"{n:<10}{lt:<25.8f}{st:<25.8f}")

    plt.figure(figsize=(8, 5))
    plt.plot(test_values, lru_times, marker='o', label='LRU Cache')
    plt.plot(test_values, splay_times, marker='o', label='Splay Tree')
    plt.yscale('log')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.title('Fibonacci Computation Performance Comparison')
    plt.legend()
    plt.savefig('fib_comparison.png')
    plt.show()

    if lru_times[-1] < splay_times[-1]:
        print("\nLRU Cache is faster for larger n in this experiment.")
    else:
        print("\nSplay Tree is faster for larger n in this experiment.")


if __name__ == "__main__":
    main()