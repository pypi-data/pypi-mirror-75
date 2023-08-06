#!/usr/bin/env python
# -*- coding: utf-8 -*-


def token(cls):
    class Class(cls):
        __name__ = cls.__name__
        __qualname__ = cls.__qualname__

        @property
        def is_token(self):
            return True

    return Class


def is_token(t):
    return hasattr(t, 'is_token') and t.is_token


class binary_operator:

    _operator_rules = {
        '+': 'add',
        '-': 'sub',
        '*': 'mul',
        '/': 'div',
        '//': 'truediv',
        '@': 'matmul',
        '**': 'pow',
    }

    class BinaryDispatcher:
        def __init__(self, f, t_other, next=None):
            self.f = f
            self.t_other = t_other
            self.next = next

        def __call__(self, other):

            if issubclass(type(other), self.t_other):
                self.f(self, other)
            elif self.next:
                self.next(other)
            else:
                raise TypeError(
                    f'Unsupported operands {self} and {other}.'
                )

    class ReverseBinaryDispatcher:
        def __init__(self, f, t_other, next=None):
            self.f = f
            self.t_other = t_other
            self.next = next

        def __call__(self, other):

            if issubclass(type(other), self.t_other):
                self.f(other, self)
            elif self.next:
                self.next(other)
            else:
                raise TypeError(
                    f'Unsupported operands {other} and {self}.'
                )

    def __init__(self, t1, op, t2):
        if op not in self._operator_rules:
            raise ValueError(f'Unknown binary operator {op}')
        if is_token(t1):
            rule = f'__{self._operator_rules[op]}__'
            self.dispatcher = self.BinaryDispatcher(
                None,
                t2,
                next=getattr(t1, rule) if hasattr(t1, rule) else None
            )
            setattr(t1, rule, self.dispatcher)
        elif is_token(t2):
            rule = f'__r{self._operator_rules[op]}__'
            self.dispatcher = self.ReverseBinaryDispatcher(
                None,
                t1,
                next=getattr(t2, rule) if hasattr(t2, rule) else None
            )
            setattr(t2, rule, self.dispatcher)
        else:
            raise ValueError(
                f'At least one operand must be a token, got {t1} and {t2}.'
            )

    def __call__(self, action):
        self.dispatcher.f = action
        return action
