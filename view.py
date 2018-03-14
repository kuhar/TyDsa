#!/usr/bin/env python

import csv
import graphviz
from subprocess import Popen


def display(g):
    path = g.save("view.mem.dot", "./")
    Popen(["xdg-open " + path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


def main():
    type_idx = 0
    type_to_idx = {}

    regs = set()

    reg_to_heap = []
    heap_to_heap = []
    heap_to_types = {}
    opaqueEdges = set()

    with open("./out/RegPtsTo.csv") as reg_pts:
        reader = csv.reader(reg_pts, delimiter='\t')
        for row in reader:
            reg = row[0]
            regs.add(reg)

            heap_name = row[1]

            ty_name = row[2]
            if ty_name not in type_to_idx:
                type_to_idx[ty_name] = type_idx
                type_idx += 1

            reg_to_heap.append((reg, heap_name, ty_name))

    with open("./out/FldPtsTo.csv") as reg_pts:
        reader = csv.reader(reg_pts, delimiter='\t')
        for row in reader:
            h1, ty1, h2, ty2 = row[0], row[1], row[2], row[3]

            for ty_name in (ty1, ty2):
                if ty_name not in type_to_idx:
                    type_to_idx[ty_name] = type_idx
                    type_idx += 1

            heap_to_heap.append((h1, ty1, h2, ty2))

    with open("./out/opaqueEdge.csv") as reg_pts:
        reader = csv.reader(reg_pts, delimiter='\t')
        for row in reader:
            r, h = row[0], row[1]
            opaqueEdges.add((r, h))

    for _, heap, ty in reg_to_heap:
        if heap not in heap_to_types:
            heap_to_types[heap] = set()

        heap_to_types[heap].add(ty)

    for h1, ty1, h2, ty2 in heap_to_heap:
        for h in (h1, h2):
            if h not in heap_to_types:
                heap_to_types[h] = set()

        heap_to_types[h1].add(ty1)
        heap_to_types[h2].add(ty2)

    s = graphviz.Digraph('TyDsa', filename='mem.gv')

    s.attr('node', shape='box')
    for reg in regs:
        s.node(reg, reg)

    s.attr('node', shape='Mrecord')
    for heap, types in heap_to_types.iteritems():
        content = '<obj> ' + heap + ' | '
        for i, ty in enumerate(types):
            content += '<f' + str(type_to_idx[ty]) + '> ' + ty + " "
            if i + 1 < len(types):
                content += '| '

        s.node(heap, content)

    reg_to_heap = sorted(reg_to_heap, key=lambda x: x[0])

    for reg, heap, ty in reg_to_heap:
        color = 'turquoise' if (reg, heap) in opaqueEdges else 'black'
        s.edge(reg,
               heap + ':f' + str(type_to_idx[ty]),
               color=color)

    heap_to_heap = sorted(heap_to_heap, key=lambda x: (x[0], x[2]))

    for h1, ty1, h2, ty2 in heap_to_heap:
        s.edge(h1 + ':f' + str(type_to_idx[ty1]),
               h2 + ':f' + str(type_to_idx[ty2]),
               color='black')

    display(s)


if __name__ == "__main__":
    main()
