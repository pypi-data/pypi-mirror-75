import os
import argparse
import json
from shapely.geometry import Polygon
from anytree import Node, RenderTree, PreOrderIter
from anytree.search import findall, findall_by_attr
from anytree.exporter import DictExporter
from pprint import pprint
import yaml
import numpy as np

class DocTree():

    def __init__(self, config):
        config = yaml.safe_load(open(config['dtree']['config']))

        self.duplicatable_fields = config['duplicatable_fields']
        self.text_field = config['text_field']
        self.min_overlap = config['min_overlap']
        self.doc_type = 'loai_vb'

    def build_response(self, nodes, doc_type):
        # create empty tree to fill
        value = {}
        confidence={}
        
        # fill in tree starting with roots (those with no parent)
        self.__export(value, None, nodes, istext=True)
        self.__export(confidence, None, nodes, istext=False)
        
        rs = {'value': {
                    **value['root'], 
                    'loai_vb': doc_type
                }, 
              'confidence': {
                    **confidence['root'],
                    'loai_vb': 0.99
                    }
            }

        return rs

    def __export(self, tree, parent, nodes, istext=True):
        """
        Args:
            tree: dict or list, current container
            parent: node
            nodes: all nodes
        """
        # find children
        children  = [(n, n.y) for n in nodes if n.parent == parent]
        children = sorted(children, key=lambda child: child[1])
        children = [n for n, _ in children]

        # build a subtree for each child
        for child in children:
            key = child.name
            # start new subtree
            if child.is_leaf:
                value = child.text if istext else float(child.prob)
                tree[key] = value
            else:
                next_tree = {}
                # container is list
                if key in self.duplicatable_fields:
                    tree[key] = tree.get(key, [])
                    tree[key].append(next_tree)
                # container is dict
                else:
                    tree[key] = next_tree

                # call recursively to build a subtree for current node
                self.__export(next_tree, child, nodes, istext)
    
    def merge_node(self, root):
        nodes = findall_by_attr(root, self.text_field)
        parents = set(node.parent for node in nodes)
        for parent in parents:
            children = findall_by_attr(parent, self.text_field, maxlevel=2)
            children = sorted(children, key=lambda child: child.y)

            texts = []
            probs = []
            for child in children:
                child.parent = None
                texts.append(child.text if child.is_leaf else '')
                probs.append(child.prob)

            texts = ' '.join(texts)
            parent.text = texts
    
        return root

    def create_node(self, bd):
        x1, y1, x2, y2 = bd['x'], bd['y'], bd['x'] + bd['w'], bd['y'] + bd['h']
        points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

        return Polygon(points)

    def score(self, a, b):
        bda = self.create_node(a)
        bdb = self.create_node(b)
        
        score = bda.intersection(bdb).area/bda.area
    
        return score

    def get_leaves(self, bds):
        bds = [{**bd, 'index':i} for i, bd in enumerate(bds)]
        root = self.build_tree(bds)
        leaves = root.leaves
        leaves_idx = [leaf.index for leaf in leaves]

        return leaves_idx

    def build_tree(self, bds):
        bds = sorted(bds, key=lambda x:x['w']*x['h'])

        root = Node(**{'x': 0, 'y': 0, 'w': 10**6, 'h':10**6, 'name': 'root', 'prob': 0.99})
                
        nodes = [Node(**bd, parent=root) for bd in bds]

        for i in range(len(bds)):
            recta = bds[i]

            for j in range(i+1, len(bds)):
                rectb = bds[j]
                
                score = self.score(recta, rectb)

                if score > self.min_overlap:
                    nodes[i].parent = nodes[j]
                    break

        return root

    def build_layout(self, bds, doc_type):
        """
        bds: array, {x, y, w, h, prob, name, text}
        """
        root = self.build_tree(bds)
        root = self.merge_node(root)

        print(RenderTree(root))
        
        rs = self.build_response([root, *root.descendants], doc_type)

        return rs
