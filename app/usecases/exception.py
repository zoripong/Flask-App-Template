import typing as t


class EntityNotFound(Exception):
    def __init__(self, class_: t.Type):
        self.message = 'Cannot found entity.'
        self.class_ = class_

    def __str__(self):
        return self.message
