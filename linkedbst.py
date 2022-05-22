"""
File: linkedbst.py
Author: Ken Lambert
"""
import random

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
#from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while node:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

        return node

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def insert_item(node):
            # New item is less, go left until spot is found
            while True:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            insert_item(self._root)
        self._size += 1
        # if self._size % 10000 == 0:
        #    print(self._size)

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(top):
                return 0
            else:
                return 1 + max(self._height2(child) for child in self.children(top))
        if self.isEmpty():
            return None
        else:
            return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height < 2 * log(len(self) + 1, 2) - 1 else False

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        pos_list = []
        check_list = [self._root]
        while check_list:
            current_node = check_list.pop()
            if current_node.data < low and current_node.right:
                check_list.append(current_node.right)
            elif low <= current_node.data <= high:
                pos_list.append(current_node.data)
                if current_node.right:
                    check_list.append(current_node.right)
                if current_node.left:
                    check_list.append(current_node.left)
            elif current_node.data > high and current_node.left:
                check_list.append(current_node.left)
        return pos_list

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        el_list = []
        for el in self:
            el_list.append(el)
        el_list.sort()
        lists_list = [el_list]
        self.clear()
        while lists_list:
            sub_list = lists_list.pop(0)
            if sub_list:
                self.add(sub_list[len(sub_list) // 2])
                lists_list.append(sub_list[:len(sub_list) // 2])
                lists_list.append(sub_list[len(sub_list) // 2 + 1:])

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # if not self.find(item):
        #    return None
        current = self._root
        potential_successor = None
        if current.data == item and not current.right:
            return potential_successor
        while True:
            if not current:
                return potential_successor.data if potential_successor else potential_successor
            if item < current.data:
                potential_successor = current
                current = current.left
            elif item > current.data:
                current = current.right
            elif item == current.data:
                if current.right:
                    potential_successor = current.right
                    while potential_successor.left:
                        potential_successor = potential_successor.left
                return potential_successor.data if potential_successor else potential_successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # if not self.find(item):
        #    return None
        current = self._root
        potential_predecessor = None
        if current.data == item and not current.left:
            return potential_predecessor
        while True:
            if not current:
                return potential_predecessor.data if potential_predecessor else potential_predecessor
            if item > current.data:
                potential_predecessor = current
                current = current.right
            elif item < current.data:
                current = current.left
            elif item == current.data:
                if current.left:
                    potential_predecessor = current.left
                    while potential_predecessor.right:
                        potential_predecessor = potential_predecessor.right
                return potential_predecessor.data if potential_predecessor else potential_predecessor

    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def random_words_generator(words):
            """Generates a list of the needed length with random words"""
            random_words = []
            for i in range(words):
                random_words.append(random.choice(ordered_list))
            return random_words

        def _reader(path, restriction=None):
            results = []
            with open(path, mode="r") as file:
                if restriction >= 0:
                    i = 0
                    while i < restriction:
                        i+=1
                        results.append(file.readline().strip())
                else:
                    for line in file:
                        results.append(line.strip())
            return results

        def words_mixing(ordered):
            random_list = []
            ordered_list_copy = ordered.copy()
            while ordered_list_copy:
                el = ordered_list_copy.pop(random.randint(0, len(ordered_list_copy) - 1))
                random_list.append(el)
            return random_list

        def time_measurement(to_find, structure):
            types_funcs = {list: list.index, LinkedBST: LinkedBST.find}
            start = time.time()
            func = types_funcs[type(structure)]
            for word in to_find:
                func(structure, word)
            stop = time.time()
            operation_time = stop - start
            return operation_time
        print("This is a demo function to show the efficiency of binary search trees. Starting generation...")
        ordered_list = _reader(path, 50000)
        unordered_list = words_mixing(ordered_list)
        to_find_list = random_words_generator(10000)
        print("Lists generation completed!")
        print("Creating an ordered tree. It may take a while...")
        ordered_tree = LinkedBST(ordered_list)
        print("First tree generation completed!")
        print("Creating a random ordered tree. It may take a while...")
        random_ordered_tree = LinkedBST(unordered_list)
        print("Second tree generation completed!")

        print("Generation completed, starting time measurement...")

        print("Search time in an ordered list (by alphabet): " + str(time_measurement(to_find_list, ordered_list)))
        print("Search time in an unordered list: " + str(time_measurement(to_find_list, unordered_list)))
        print("Search time in an ordered tree (by alphabet): " + str(time_measurement(to_find_list, ordered_tree)))
        print("Search time in an unordered tree: " + str(time_measurement(to_find_list, random_ordered_tree)))
        ordered_tree.rebalance()
        print("Search time in a balanced tree (previously ordered tree): " + str(time_measurement(to_find_list, ordered_tree)))
