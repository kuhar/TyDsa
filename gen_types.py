#!/usr/bin/env python

from __future__ import print_function
from itertools import chain, combinations


class Type:
    def __init__(self, name, size, is_ptr=False):
        self.name = name
        self.is_ptr = is_ptr
        self.size = size

    def add_ptr(self):
        new_ty = Type(self.name + '*', 8, True)
        return new_ty

    def dump(self):
        print('sizeOf(\"' + self.name + '\", ' + str(self.size) + ').')
        print('ptrOf(\"' + self.name + '\", ' + self.name + '*\").')
        print('ptrOf(\"' + self.name + '*\", ' + self.name + '**\").')

    def is_primitive(self):
        return True


class Struct(Type):
    def __init__(self, name, fields):
        self.fields = fields
        total_size = 0
        for f in self.fields:
            total_size += f.size

        Type.__init__(self, name, total_size)

    def dump(self):
        Type.dump(self)
        print('class(\"' + self.name + '\", ' + str(len(self.fields)) + ').')
        for i, fld in enumerate(self.fields):
            print('field(\"' + self.name + '\", \"' + fld.name + '\", ' + str(i) + ').')

    def is_primitive(self):
        return False


def powerset(xs):
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs)))

def to_ty_list(x):
    res = "{"
    for t in x:
        res += t.name + ' '
    res += "}"
    return res


i8 = Type("i8", 1)
i16 = Type("short", 2)
i32 = Type("int", 4)
f32 = Type("float", 4)

Foo = Struct("Foo", [i16, i32, i16.add_ptr()])
Bar = Struct("Bar", [i16.add_ptr(), i32.add_ptr(), f32.add_ptr()])
Baz = Struct("Baz", [i16.add_ptr(), i16, i16.add_ptr()])
Bam = Struct("Bam", [f32.add_ptr(), Foo, i16])

primitive_types = [i8, i16, i32, f32]
types = [i8, i16, i32, f32, Foo, Bar, Baz, Bam]

for t in types:
    t.dump()
    print()


all_types = []
for t in primitive_types:
    all_types.append(t)
    all_types.append(t.add_ptr())
    all_types.append(t.add_ptr().add_ptr())

ps = set(powerset(all_types))
for p in ps:
    for t in primitive_types:
        if t not in p:
            print('append_type(\"' + to_ty_list(p) + '\", \"' + t.name + '\", \"' + to_ty_list(p + (t, )) + '\").')



