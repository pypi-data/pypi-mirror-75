from rocon_client_sdk_py.utils.util import *


class DListNode:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DListDataQueue(metaclass=SingletonMetaClass):
    def __init__(self):
        self._head = None
        self._tail = None

    def append(self, msg_data, remove_same_name_prev_msg=False):
        if remove_same_name_prev_msg is True:
            name = msg_data['name']
            self.remove_all(name=name)

        if not self._head:
            self._head = DListNode(data=msg_data)
            self._tail = self._head
            return

        if self._tail:
            new_tail = DListNode(data=msg_data, prev=self._tail)
            self._tail.next = new_tail
            self._tail = new_tail

    def find(self, name):
        curr = self._head
        while curr:
            if 'name' in curr and curr['name'] == name:
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

        return data

    def peek(self):
        if self._head is None:
            return None

        return self._head.data

    def remove_all(self, name=None):
        curr = self._head

        if name is not None:
            while curr:
                if 'name' in curr and curr['name'] == name:
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

