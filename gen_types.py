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
        print('ptrOf(\"' + self.name + '\", \"' + self.name + '*\").')
        print('ptrOf(\"' + self.name + '*\", \"' + self.name + '**\").')

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
    names = [t.name for t in x]
    return '{' + ' '.join(names) + '}'


i8 = Type("i8", 1)
Ty1 = Type("Ty1", 4)
Ty2 = Type("Ty2", 2)
Ty3 = Type("Ty3", 12)

Foo = Struct("Foo", [Ty1, Ty2, Ty1.add_ptr()])
Bar = Struct("Bar", [Ty1.add_ptr(), Ty2.add_ptr(), Ty3.add_ptr()])
Baz = Struct("Baz", [Ty1.add_ptr(), Ty1, Ty1.add_ptr()])
Bam = Struct("Bam", [Foo, Ty3.add_ptr(), Ty1])

primitive_types = [i8, Ty1, Ty2, Ty3]
types = [i8, Ty1, Ty2, Ty3, Foo, Bar, Baz, Bam]

for t in types:
    t.dump()
    print()


# all_types = []
# for t in primitive_types:
#     all_types.append(t)
#     all_types.append(t.add_ptr())
#
# ps = set(powerset(all_types))
# for p in ps:
#     for t in all_types:
#         sorter = lambda ty: ty.name
#         tys = sorted(p, key=sorter)
#         if t not in p:
#             with_t = sorted(p + (t, ), key=sorter)
#             print('append_type(\"' + to_ty_list(tys) + '\", \"' + t.name + '\", \"' + to_ty_list(with_t) + '\").')
#         else:
#             print('has_type(\"' + to_ty_list(tys) + '\", \"' + t.name + '\").')


