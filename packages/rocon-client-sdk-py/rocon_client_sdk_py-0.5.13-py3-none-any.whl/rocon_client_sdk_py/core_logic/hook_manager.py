import ast
import os
import importlib.util
import glob, pathlib, sys


class HookManager():
    def __init__(self, context, logger=None):
        self._context = context
        self._hook_path = context.worker._hooks_def_path
        self._hook_instances = self._dynamic_load_hooks(self._hook_path)

    def _dynamic_load_hooks(self, hook_path):
        """
            주어진 절대경로 hook_path로 부터 hook 클래스 인스턴스를 동적 생성한다.
            경로내의 hook 정의 파일은 'hook_xxx.py'의 규칙을 가져야한다.

        """
        self._context.rocon_logger.debug('load hook class files at {}'.format(hook_path))

        hook_instances = {}

        sys.path.append(hook_path)
        py_files = glob.glob(os.path.join(hook_path, 'hook_*.py'))
        for py_file in py_files:
            module_name = pathlib.Path(py_file).stem
            module = importlib.import_module(module_name)

            # path_name으로 부터 선언된 클래스 찾기 (내부 유일 클래스로 가정)
            hook_class = None
            with open(py_file, "rb") as src_stream:
                p = ast.parse(src_stream.read())
                classnames = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
                hook_class = classnames[0]

            class_instance = getattr(module, hook_class)
            hook = class_instance()
            hook.context = self._context
            hook_instances[hook.name] = hook

            self._context.rocon_logger.debug('created instance of hook "{}"'.format(hook.name))

        return hook_instances

    def find_hook(self, hook_name):
        """
        hook_name (string)으로 hook instance 찾아 리턴
        :return:
        """

        for hook_key in self._hook_instances:
            if self._hook_instances[hook_key].name == hook_name:
                return self._hook_instances[hook_key]

        return None

    async def execute(self, hook):
        hook_inst = self.find_hook(hook['name'])
        # TODO validate message body schema using jsonschema

        if hook_inst:
            result = await hook_inst.on_handle(hook)
            return result
        else:
            self._context.rocon_logger.error('malformed message handler: {}, {}'.format(hook['name'], {'message': hook}))
            return False
