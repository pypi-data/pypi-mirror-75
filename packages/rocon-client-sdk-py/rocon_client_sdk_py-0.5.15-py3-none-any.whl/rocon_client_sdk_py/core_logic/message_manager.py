import ast
import os
import importlib.util
import glob, pathlib, sys
from rocon_client_sdk_py.utils.util import *

class MessageManager():
    def __init__(self, context, logger=None):
        self._context = context

        self._queue = ReceivedMessageDataQueue()

        msg_path = context.worker.msg_def_paths
        self._msg_path = msg_path
        self._msg_instances = self._dynamic_load_messages(msg_path)
        self._msg_defines = {}

    def _dynamic_load_messages(self, msg_path):
        """
            주어진 절대경로 msg_path로 부터 message 클래스 인스턴스를 동적 생성한다.
            경로내의 message 정의 파일은 'message_xxx.py'의 규칙을 가져야한다.

        """
        self._context.rocon_logger.debug('load message class files at {}'.format(msg_path))
        msg_instances = {}

        sys.path.append(msg_path)
        py_files = glob.glob(os.path.join(msg_path, 'message_*.py'))
        for py_file in py_files:
            module_name = pathlib.Path(py_file).stem
            module = importlib.import_module(module_name)

            # path_name으로 부터 선언된 클래스 찾기 (내부 유일 클래스로 가정)
            msg_class = None
            # path_name = msg_path + '/' + filename
            with open(py_file, "rb") as src_stream:
                p = ast.parse(src_stream.read())
                classnames = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
                msg_class = classnames[0]

            class_instance = getattr(module, msg_class)
            msg = class_instance()
            msg.context = self._context
            msg_instances[msg.name] = msg

            self._context.rocon_logger.debug('created instance of message "{}"'.format(msg.name))

        return msg_instances

    def find_message(self, msg_name):
        """
        msg_name (string)으로 message instance 찾아 리턴
        :return:
        """
        for msg_key in self._msg_instances:
            if self._msg_instances[msg_key].name == msg_name:
                return self._msg_instances[msg_key]

        return None

    async def execute(self, msg):
        msg_inst = self.find_message(msg['name'])
        # TODO validate message body schema using jsonschema

        if msg_inst:
            result = await msg_inst.on_handle(msg)
            return result
        else:
            self._context.rocon_logger.error('malformed message handler: {}, {}'.format(msg['name'], {'message': msg}))
            return False

    def push_new_message_data(self, msg_data, remove_same_name_prev_msg=False):
        self._queue.append(msg_data, remove_same_name_prev_msg=remove_same_name_prev_msg)

    def pop_message_data(self):
        return self._queue.pop()


class DListNode:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class ReceivedMessageDataQueue(metaclass=SingletonMetaClass):
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
            self._tail = DListNode(data=msg_data, prev=self._tail)

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


class ReceivedMessageData():
    def __init__(self, name, body):
        self.name = name
        self.body = body

