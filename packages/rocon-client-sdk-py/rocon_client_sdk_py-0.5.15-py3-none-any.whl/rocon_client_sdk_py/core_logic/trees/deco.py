import py_trees
from .constants import *
from py_trees.decorators import Decorator
from py_trees import behaviour
from py_trees import blackboard
from py_trees import common
from rocon_client_sdk_py.core_logic.context import Context


class CustomDecoBase(Decorator):

    def __init__(self, child: behaviour.Behaviour, name=common.Name.AUTO_GENERATED):
        super().__init__(child, name)

        self._blabkboard = None
        self._context = None

    @property
    def context(self) -> Context:

        if self._blabkboard is None:
            self._blabkboard = py_trees.blackboard.Client(name=MASTER_BLACKBOARD_NAME)
            self._blabkboard.register_key(key=KEY_CONTEXT, access=py_trees.common.Access.READ, required=True)
            self._context = self._blabkboard.get(KEY_CONTEXT)

        return self._context

