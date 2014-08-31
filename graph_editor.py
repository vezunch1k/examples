# -*- coding: utf-8 -*-
import sys
import re
import argparse


class Vertex(object):
    def __init__(self, vertex_name):
        if re.search('[^a-zA-Z_0-9]', vertex_name):
            raise AttributeError('You can use only letters, digits and _')
        self.vertex_name = vertex_name
        self.options = {}

    def set_option(self, key, value):
        self.options[key] = value

    def remove_option(self, key):
        if key not in self.options:
            raise AttributeError('No option with key %s' % key)
        del self.options[key]


class Graph(object):
    def __init__(self):
        self.vertex_list = {}
        self.edge_list = {}

    def has_edge(self, name1, name2):
        if ''.join((name1, ':', name2)) in self.edge_list:
            return True
        return False

    def has_vertex(self, name):
        return True if name in self.vertex_list else False

    def add_vertex(self, vertex):
        self.vertex_list[vertex.vertex_name] = vertex

    def remove_vertex(self, name):
        if not self.has_vertex(name):
            raise AttributeError('No vertex in graph with name %s' % name)
        del self.vertex_list[name]

    def add_edge(self, name1, name2):
        if not self.has_vertex(name1):
            raise AttributeError('No vertex with name %s' % name1)
        elif not self.has_vertex(name2):
            raise AttributeError('No vertex with name %s' % name2)
        elif self.has_edge(name2, name1) or self.has_edge(name1, name2):
            raise AttributeError('Graph already has such edge')
        else:
            self.edge_list[''.join((name1, ':', name2))] = True

    def remove_edge(self, name1, name2):
        if not self.has_edge(name1, name2) and not self.has_edge(name2, name1):
            raise AttributeError('No edge between %s and %s' % (name1, name2))
        else:
            if self.has_edge(name1, name2):
                edge = ''.join((name1, ':', name2))
            else:
                edge = ''.join((name2, ':', name1))
            del self.edge_list[edge]

    def get_vertex(self, name):
        if not self.has_vertex(name):
            raise AttributeError('No vertex in graph with name %s' % name)
        return self.vertex_list[name]


class Activity(object):
    def __init__(self, do, undo, params):
        self.do = do
        self.undo = undo
        self.params = params


class History(object):
    def __init__(self):
        self.undo = []
        self.redo = []

    def do_undo(self):
        if not self.undo:
            raise IndexError('Nothing to undo')
        act = self.undo.pop()
        act.undo(act.params)
        self.redo.append(act)

    def do_redo(self):
        if not self.redo:
            raise IndexError('Nothing to redo')
        act = self.redo.pop()
        act.do(act.params)
        self.undo.append(act)

    def add(self, act):
        self.undo.append(act)
        del self.redo[:]


class Document(object):
    def help(self, *args):
        print help

    def exit(self, *args):
        print 'Nooooooooo\n'
        sys.exit(0)

    def add_vertex(self, obj):
        mygraph.add_vertex(Vertex(obj.name))

    def remove_vertex(self, obj):
        mygraph.remove_vertex(obj.name)

    def set_vertex_attribute(self, obj):
        vertex = mygraph.get_vertex(obj.name)
        vertex.set_option(obj.key, obj.value)
        mygraph.add_vertex(vertex)

    def remove_vertex_attribute(self, obj):
        vertex = mygraph.get_vertex(obj.name)
        vertex.remove_option(obj.key)
        mygraph.add_vertex(vertex)

    def print_graph(self, *args):
        buffer = ['graph mygraph {\n']
        for k, v in mygraph.vertex_list.iteritems():
            options_str = ''
            if v.options:
                options_buffer = []
                for o, m in v.options.iteritems():
                    options_buffer.extend([''.join([o, '=', m])])
                options_buffer = ' '.join(options_buffer)
                options_str = ''.join([' [', options_buffer, ']'])
            buffer.extend([k, options_str, ';\n'])
        for k, v in mygraph.edge_list.iteritems():
            (name1, name2) = k.split(':')
            buffer.extend([name1, ' -- ', name2, ';\n'])
        buffer.append('}\n')
        sys.stdout.write(''.join(buffer))

    def add_edge(self, obj):
        mygraph.add_edge(obj.name1, obj.name2)

    def remove_edge(self, obj):
        mygraph.remove_edge(obj.name1, obj.name2)

    def undo(self, *args):
        myhistory.do_undo()

    def redo(self, *args):
        myhistory.do_redo()


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Commands", metavar="<command>")

    p_va = subparsers.add_parser('add_vertex', help='vertex adding')
    p_va.add_argument('name')
    p_va.set_defaults(func=mydoc.add_vertex, antifunc=mydoc.remove_vertex)

    p_rv = subparsers.add_parser('remove_vertex', help='vertex deleting')
    p_rv.add_argument('name')
    p_rv.set_defaults(func=mydoc.remove_vertex, antifunc=mydoc.add_vertex)

    p_sv = subparsers.add_parser('set_vertex_attribute', help='set attribute')
    p_sv.add_argument('name')
    p_sv.add_argument('key')
    p_sv.add_argument('value')
    p_sv.set_defaults(
        func=mydoc.set_vertex_attribute,
        antifunc=mydoc.remove_vertex_attribute
    )

    p_ae = subparsers.add_parser('add_edge', help='edge adding')
    p_ae.add_argument('name1')
    p_ae.add_argument('name2')
    p_ae.set_defaults(func=mydoc.add_edge, antifunc=mydoc.remove_edge)

    p_re = subparsers.add_parser('remove_edge', help='edge deleting')
    p_re.add_argument('name1')
    p_re.add_argument('name2')
    p_re.set_defaults(func=mydoc.remove_edge, antifunc=mydoc.add_edge)

    p_pg = subparsers.add_parser('print', help='graph printing')
    p_pg.set_defaults(func=mydoc.print_graph, antifunc=None)

    p_exit = subparsers.add_parser('exit', help='exits the editor')
    p_exit.set_defaults(func=mydoc.exit, antifunc=None)

    p_undo = subparsers.add_parser('undo', help='undo the last action')
    p_undo.set_defaults(func=mydoc.undo, antifunc=None)

    p_redo = subparsers.add_parser('redo', help='redo the last action')
    p_redo.set_defaults(func=mydoc.redo, antifunc=None)
    return parser

if __name__ == '__main__':
    mygraph = Graph()
    myhistory = History()
    mydoc = Document()
    parser = get_parser()
    while True:
        try:
            args = parser.parse_args(raw_input('\n>>> Enter action: ').split())
            args.func(args)
            if args.antifunc:
                myhistory.add(Activity(args.func, args.antifunc, args))
        except Exception, e:
            print e
