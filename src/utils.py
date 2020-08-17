import networkx as nx
import matplotlib.pyplot as plt
from random import choice

########################################
# A support class for build dispute tree
########################################
class ArgumentTreeNode:
    def __init__(self, root=' '):
        self.value = root
        self.child = []

########################################
# Argument Framework 
########################################
class ArgumentFramework:

    def __init__(self, edges=[]):
        self.frame = nx.DiGraph()
        # self.frame.clear()
        self.tree=[]

    #############################
    # basic utility functions  
    #############################
    def add_node(self,node):
        self.frame.add_node(node)
    def add_edges(self,node1,node2):
        self.frame.add_edge(node1,node2)
    def remove_edges(self,edge):
        self.frame.remove_edges_from(edge)
    def get_nodes(self):
        return self.frame.nodes
    def get_edges(self):
        return self.frame.edges()
    def get_tree(self):
        return self.tree    
    def reverse_frame(self):
        return self.frame.reverse()
    # dfs on edges(which will find all edges apart from nodes)    
    def dfs(self,node):
        rframe = self.reverse_frame()
        path = list(nx.edge_dfs(rframe,node)) 
        for edge in path:
            if edge[0] == edge[1]:
                path.remove(edge) 
        return path     

    ############################
    # figure generators
    ############################
    def show_gram(self,showflag=1):
        plt.figure()
        nx.draw(self.frame,pos=nx.spring_layout(self.frame,seed=500),
        node_color='black',node_size=1600,
        with_labels=True,font_color='w',font_size=30,
        arrowsize=25,arrowstyle='->',edge_color='black',width=2)
        if showflag == 1:
            plt.show()
        else:
            plt.savefig('framework.png')
            plt.close()
    
    ############################
    # functional utility functions
    ############################                          
    # build argument tree for every node
    def build_argument_tree_without_duplicate(self,root):
        # path is like [('e','b'),('e','d')]
        path = self.dfs(root)
        nodes = list(self.get_nodes())
        self.build_argument_tree(root,path,nodes)
        # self.tree is a instance of ArgumentTreeNode
        return self.tree
    def build_argument_tree(self,root,path,nodes):   
        if root in nodes:
            nodes.remove(root)
            node = ArgumentTreeNode()
            node.value = root
            for edge in path:
                if edge[0] == root:
                    node.child.append(edge[1])
            self.tree.append(node)        
            for child in node.child:
                self.build_argument_tree(child,path,nodes)              
        return 
    def get_childen_by_node(self,tree):
        children_dict = {}
        for node in tree:
            children_dict[node.value] = node.child
        # children_dict is like {'e':['a','f']}
        return children_dict

    def random_dispute_tree(self,node,semantics='grounded'):
        path = self.dfs(node)
        tree = self.get_tree()
        # children_dict is like {'e':['a','f']}
        children_dict = self.get_childen_by_node(tree)
        strategy = [node]
        self.random_add_node(node,children_dict,strategy,semantics)
        strategy = self.remove_dupilicate(strategy,semantics)
        return strategy
    def random_add_node(self,node,children_dict,strategy,semantics):
        if not children_dict[node]:
            return
        while True:
            child = choice(children_dict[node])
            if semantics == 'preferred':
                if (len(strategy)%2) and (child in strategy[1::2]):
                    if all(c in strategy[1::2] for c in children_dict[node]):
                        return
                    else:
                        continue    
                else:
                    strategy.append(child)
                    self.random_add_node(child,children_dict,strategy,semantics)
                    return    
            elif semantics == 'grounded':
                # odd and P is going to repeat
                if (not len(strategy)%2) and (child in strategy[::2]): 
                    if all(c in strategy[::2] for c in children_dict[node]):
                        return
                    else:
                        continue 
                else:
                    strategy.append(child)    
                    self.random_add_node(child,children_dict,strategy,semantics)
                    return     

    def build_dispute_tree(self, node, trial, semantics='grounded'):
        dispute_tree = []
        for i in range(trial):
            s = self.random_dispute_tree(node,semantics)                
            if s not in dispute_tree:
                dispute_tree.append(s)        
        return dispute_tree
    def remove_dupilicate(self, strategy, semantics):
        if semantics == 'grounded':
            dupmoves = strategy[1::2]
        elif semantics == 'preferred':
            dupmoves = strategy[::2]    
        for node in dupmoves:
            if strategy.count(node) >= 2:
                index_list = [x for x in range(len(strategy)) if strategy[x] == node]
                strategy = strategy[0:index_list[1]+1]
        return strategy    

####### Using Example #######
# if __name__ == '__main__':
#     # add nodes like click button
#     af = ArgumentFramework()
#     af.add_node('a')
#     af.add_node('b')
#     af.add_node('c')
#     af.add_node('d')
#     af.add_node('e')
#     af.add_node('f')
#     af.add_edges('a','b')
#     #af.add_edges('b','c')
#     af.add_edges('c','b')
#     af.add_edges('c','d')
#     af.add_edges('b','d')
#     af.add_edges('d','e')
#     af.add_edges('e','f')
#     af.add_edges('f','e')

#     # build argument tree
#     tree = af.build_argument_tree_without_duplicate('e')

#     dispute_tree = af.build_dispute_tree('e',semantics='grounded',trial=50)
#     print(dispute_tree)
#     print('The number of strategy: %d'%len(dispute_tree))
#     af.show_gram(showflag=0)
    