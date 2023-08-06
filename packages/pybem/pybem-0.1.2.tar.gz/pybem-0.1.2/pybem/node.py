from abc import ABC, abstractmethod
from collections import OrderedDict


class Node(ABC):
    def __init__(self, name: str):
        self.__name = name
        self.__classes = OrderedDict()
        self.__modifiers = OrderedDict()
        self.__mixes = []

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
        return self

    def get_modifiers(self):
        return self.__modifiers

    def set_modifiers(self, modifiers: dict):
        self.__modifiers.clear()

        for m in modifiers:
            self.add_modifier(m, modifiers[m])

        return self

    def get_modifier(self, name, default=None):
        return self.__modifiers[name] if self.has_modifier(name) else default

    def add_modifier(self, name, value=True):
        self.__modifiers[name] = value
        return self

    def has_modifier(self, name):
        return name in self.__modifiers

    def remove_modifier(self, name):
        self.__modifiers.pop(name, None)
        return self

    def get_mixes(self):
        return self.__mixes

    def add_mix(self, node):
        self.__mixes.append(node)
        return self

    def remove_mix(self, node):
        if self.has_mix(node):
            self.__mixes.remove(node)
        return self

    def has_mix(self, node):
        return node in self.__mixes

    def get_classes(self):
        return list(self.__classes.keys())

    def set_classes(self, classes: list):
        self.__classes.clear()

        for c in classes:
            self.add_class(c)
        return self

    def add_class(self, name):
        self.__classes[name] = True
        return self

    def remove_class(self, name):
        self.__classes.pop(name, None)
        return self

    def has_class(self, name):
        return name in self.__classes

    def build_classes(self):
        return " ".join(self.generate_classes())

    def generate_modifier_classes(self):
        for modifier in self.__modifiers:
            if type(self.__modifiers[modifier]) is bool and self.__modifiers[modifier]:
                yield '{}--{}'.format(self.get_base_class(), modifier)
            elif type(self.__modifiers[modifier]) in [str, int]:
                yield '{}--{}_{}'.format(self.get_base_class(), modifier, self.__modifiers[modifier])
            elif type(self.__modifiers[modifier]) is list:
                base_class = self.get_base_class()
                for v in self.__modifiers[modifier]:
                    yield '{}--{}_{}'.format(base_class, modifier, str(v))

    def generate_mixes_classes(self):
        for mix in self.__mixes:
            yield from mix.generate_classes()

    def generate_classes(self):
        yield self.get_base_class()

        yield from self.generate_modifier_classes()

        for c in self.__classes.keys():
            yield c

        yield from self.generate_mixes_classes()

    def m(self, name, value=True):
        return self.add_modifier(name, value)

    def mix(self, node):
        return self.add_mix(node)

    @abstractmethod
    def get_base_class(self):
        pass

    def __str__(self):
        return self.build_classes()
