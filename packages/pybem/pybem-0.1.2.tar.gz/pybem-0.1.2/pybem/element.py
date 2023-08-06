from .node import Node


class Element(Node):
    def __init__(self, name, block):
        self.__block = block
        super(Element, self).__init__(name)

    def get_block(self):
        return self.__block

    def set_block(self, block):
        self.__block = block

    def get_base_class(self):
        return '{}__{}'.format(self.get_block().get_name(), self.get_name())


