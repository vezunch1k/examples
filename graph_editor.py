# -*- coding: utf-8 -*-
import sys
import re
import argparse


class Item(object):
    def __init__():
        self.options = {}

    def set_option(self, key, value):
        if re.search('[^a-zA-Z_0-9]', key):
            raise AttributeError('You can use only letters, digits and _')
        self.options[key] = value

    def remove_option(self, key):
        if key not in self.options:
            raise AttributeError('No option with key %s' % key)
        del self.options[key]

# generalized function for getting Item options to be printed
    def get_printable_options(self):
        options_str = ''
        if self.options:
            options_buffer = []
            for k, v in self.options.iteritems():
                options_buffer.extend([''.join([k, '=', v])])
            options_buffer = ' '.join(options_buffer)
            options_str = ''.join([' [', options_buffer, ']'])
        return options_str


class Vertex(Item):
    def __init__(self, vertex_name):
        if re.search('[^a-zA-Z_0-9]', vertex_name):
            raise AttributeError('You can use only letters, digits and _')
        self.vertex_name = vertex_name
        self.options = {}


class Edge(Item):
    def __init__(self, name1, name2):
        if re.search('[^a-zA-Z_0-9]', name1):
            raise AttributeError('You can use only letters, digits and _')
        if re.search('[^a-zA-Z_0-9]', name2):
            raise AttributeError('You can use only letters, digits and _')
        self.name1 = name1
        self.name2 = name2
        self.options = {}

# hide logics for naming inside class
    @staticmethod
    def get_edge_name(name1, name2):
        (name1, name2) = sorted([name1, name2])
        return ''.join((name1, ':', name2))


class Graph(object):
    def __init__(self, name):
        self.name = name
        self.vertex_list = {}
        self.edge_list = {}

    def has_vertex(self, name):
        return True if name in self.vertex_list else False

    def add_vertex(self, name):
        if self.has_vertex(name):
            raise AttributeError('Graph has vertex with name %s' % name)
        self.vertex_list[name] = Vertex(name)

    def remove_vertex(self, name):
        if not self.has_vertex(name):
            raise AttributeError('No vertex in graph with name %s' % name)
        del self.vertex_list[name]

    def set_vertex_attribute(self, name, key, value):
        vertex = self.get_vertex(name)
        vertex.set_option(key, value)

    def remove_vertex_attribute(self, name, key):
        vertex = self.get_vertex(name)
        vertex.remove_option(key)

    def has_edge(self, name1, name2):
        if Edge.get_edge_name(name1, name2) in self.edge_list:
            return True
        return False

    def add_edge(self, name1, name2):
        if not self.has_vertex(name1):
            raise AttributeError('No vertex with name %s' % name1)
        if not self.has_vertex(name2):
            raise AttributeError('No vertex with name %s' % name2)
        if self.has_edge(name1, name2):
            raise AttributeError('Graph has edge %s -- %s' % (name1, name2))
        self.edge_list[Edge.get_edge_name(name1, name2)] = Edge(name1, name2)

    def remove_edge(self, name1, name2):
        if not self.has_edge(name1, name2):
            raise AttributeError('No edge between %s and %s' % (name1, name2))
        del self.edge_list[Edge.get_edge_name(name1, name2)]

    def get_vertex(self, name):
        if not self.has_vertex(name):
            raise AttributeError('No vertex in graph with name %s' % name)
        return self.vertex_list[name]

    def get_edge(self, name1, name2):
        if not self.has_edge(name1, name2):
            raise AttributeError('No edge between %s and %s' % (name1, name2))
        return self.edge_list[Edge.get_edge_name(name1, name2)]

    def set_edge_attribute(self, name1, name2, key, value):
        edge = self.get_edge(name1, name2)
        edge.set_option(key, value)

    def remove_edge_attribute(self, name1, name2, key):
        edge = self.get_edge(name1, name2)
        edge.remove_option(key)

    def get_dot_graph(self):
        buffer = ['graph ', self.name, ' {\n']
        for k, v in self.vertex_list.iteritems():
            options = v.get_printable_options()
            buffer.extend([k, options, ';\n'])
        for k, v in self.edge_list.iteritems():
            options = v.get_printable_options()
            buffer.extend([v.name1, ' -- ', v.name2, options, ';\n'])
        buffer.append('}\n')
        return ''.join(buffer)


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
# flush redo stack, if action called from command line
        del self.redo[:]


class Document(object):
    def __init__(self):
        self.graph = Graph('mygraph')
        self.history = History()

    def help(self, *args):
        print help

    def exit(self, *args):
        print 'Nooooooooo\n'
        sys.exit(0)

    def add_vertex(self, obj):
        self.graph.add_vertex(obj.name)

    def remove_vertex(self, obj):
        self.graph.remove_vertex(obj.name)

    def set_vertex_attribute(self, obj):
        self.graph.set_vertex_attribute(obj.name, obj.key, obj.value)

    def remove_vertex_attribute(self, obj):
        self.graph.remove_vertex_attribute(obj.name, obj.key)

    def print_graph(self, *args):
        printable_graph = self.graph.get_dot_graph()
        sys.stdout.write(printable_graph)

    def add_edge(self, obj):
        self.graph.add_edge(obj.name1, obj.name2)

    def remove_edge(self, obj):
        self.graph.remove_edge(obj.name1, obj.name2)

    def set_edge_attribute(self, obj):
        self.graph.set_edge_attribute(obj.name1, obj.name2, obj.key, obj.value)

    def remove_edge_attribute(self, obj):
        self.graph.remove_edge_attribute(obj.name1, obj.name2, obj.key)

    def undo(self, *args):
        self.history.do_undo()

    def redo(self, *args):
        self.history.do_redo()


def get_parser(doc):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Commands", metavar="<command>")

    p_va = subparsers.add_parser('add_vertex', help='vertex adding')
    p_va.add_argument('name')
    p_va.set_defaults(func=doc.add_vertex, antifunc=doc.remove_vertex)

    p_rv = subparsers.add_parser('remove_vertex', help='vertex deleting')
    p_rv.add_argument('name')
    p_rv.set_defaults(func=doc.remove_vertex, antifunc=doc.add_vertex)

    p_sva = subparsers.add_parser(
        'set_vertex_attribute', help='setting vertex attribute')
    p_sva.add_argument('name')
    p_sva.add_argument('key')
    p_sva.add_argument('value')
    p_sva.set_defaults(
        func=doc.set_vertex_attribute,
        antifunc=doc.remove_vertex_attribute
    )

    p_ae = subparsers.add_parser('add_edge', help='edge adding')
    p_ae.add_argument('name1')
    p_ae.add_argument('name2')
    p_ae.set_defaults(func=doc.add_edge, antifunc=doc.remove_edge)

    p_re = subparsers.add_parser('remove_edge', help='edge deleting')
    p_re.add_argument('name1')
    p_re.add_argument('name2')
    p_re.set_defaults(func=doc.remove_edge, antifunc=doc.add_edge)

    p_sea = subparsers.add_parser(
        'set_edge_attribute', help='setting edge attribute')
    p_sea.add_argument('name1')
    p_sea.add_argument('name2')
    p_sea.add_argument('key')
    p_sea.add_argument('value')
    p_sea.set_defaults(
        func=doc.set_edge_attribute,
        antifunc=doc.remove_edge_attribute
    )

    p_undo = subparsers.add_parser('undo', help='undo the last action')
    p_undo.set_defaults(func=doc.undo, antifunc=None)

    p_redo = subparsers.add_parser('redo', help='redo the last action')
    p_redo.set_defaults(func=doc.redo, antifunc=None)

    p_pg = subparsers.add_parser('print', help='graph printing')
    p_pg.set_defaults(func=doc.print_graph, antifunc=None)

    p_exit = subparsers.add_parser('exit', help='exits the editor')
    p_exit.set_defaults(func=doc.exit, antifunc=None)
    return parser

if __name__ == '__main__':
    mydoc = Document()
    parser = get_parser(mydoc)
    while True:
        try:
            args = parser.parse_args(raw_input('\n>>> Enter action: ').split())
            args.func(args)
            if args.antifunc:
                mydoc.history.add(Activity(args.func, args.antifunc, args))
        except Exception, e:
            print e
