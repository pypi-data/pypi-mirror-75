from rocon_client_sdk_py.utils.util import *

class DKeyLinkedListNode:
    def __init__(self, key, data=None, prev=None, next=None, waiter=None):
        self.key = key
        self.waiter = waiter
        self.data = data
        self.prev = prev
        self.next = next

        self.resp_data = None


class DKeyLinkedList(metaclass=SingletonMetaClass):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, key, msg_data, remove_same_name_prev_msg=False, waiter=None):
        if remove_same_name_prev_msg is True:
            self.remove_all(name=key)

        self._size += 1

        if not self._head:
            self._head = DKeyLinkedListNode(key, data=msg_data, waiter=waiter)
            self._tail = self._head
            return

        if self._tail:
            new_tail = DKeyLinkedListNode(key, data=msg_data, prev=self._tail, waiter=waiter)
            self._tail.next = new_tail
            self._tail = new_tail



    def find(self, key):
        curr = self._head
        #TODO 검색속도 향상 필요
        while curr:
            if curr.key == key:
                return curr

            curr = curr.next

        return None

    def pop_key(self, key):
        if self._head is None:
            return None

        curr = self._head
        while curr:
            if curr.key == key:
                self._remove(curr)
                return curr

            curr = curr.next

        return None

    def pop(self):

        if self._head is None:
            return None

        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None

        self._size -= 1
        if self._size < 0: self._size = 0

        return data

    def peek(self):
        if self._head is None:
            return None

        return self._head.data

    def remove_all(self, key=None):
        curr = self._head
        self._size = 0

        if key is not None:
            while curr:
                if curr.key == key:
                    next = curr.next
                    self._remove(curr)
                    curr = next
                else:
                    curr = curr.next
        else:
            self._head = None
            self._tail = None

    def _remove(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self._head:
            self._head = node.next

        node.prev = None
        node.next = None

        self._size -= 1
        if self._size < 0: self._size = 0



    def size(self):
        return self._size