from .node import Node
from .element import Element


class Block(Node):

    def get_base_class(self):
        return self.get_name()

    def create_element(self, name):
        return Element(name, self)

    def e(self, name):
        return self.create_element(name)
