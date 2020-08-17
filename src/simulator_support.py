#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.2
#  in conjunction with Tcl version 8.6
#    Jul 12, 2020 10:20:25 AM BST  platform: Windows NT
#    Jul 12, 2020 11:34:49 AM BST  platform: Windows NT
#    Jul 15, 2020 09:04:38 AM BST  platform: Windows NT
#    Jul 15, 2020 11:40:18 AM BST  platform: Windows NT
#    Jul 15, 2020 11:46:57 AM BST  platform: Windows NT
#    Aug 06, 2020 08:56:30 AM BST  platform: Windows NT
#    Aug 10, 2020 11:50:39 AM BST  platform: Windows NT
#    Aug 10, 2020 11:55:00 AM BST  platform: Windows NT
#    Aug 11, 2020 06:45:53 AM BST  platform: Windows NT

import sys
from utils import ArgumentFramework
from PIL import Image, ImageTk
from random import choice

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global message
    message = tk.StringVar()

    global selectedButton
    selectedButton = tk.IntVar()
    global spinbox
    spinbox = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    global attackers, defenders, nodes
    global gpath, ppath
    w = gui
    top_level = top
    root = top
    nodes = []
    attackers, defenders = [], []
    gpath, ppath = [], []

def addEdges(p1):
    a = w.entry_attacker.get().split(',')
    d = w.entry_defender.get().split(',')
    for i in range(min(len(a),len(d))):
        attackers.append(a[i])
        defenders.append(d[i])
    print('Number of edges: ', len(attackers))
    sys.stdout.flush()

def addNodes(p1):
    global nodes
    nodes = w.entry_addNode.get().split(',')
    print('Number of nodes: ', len(nodes))
    sys.stdout.flush()

def assignRoot(p1):
    for widget in w.Labelframe_groundedGameLogs.winfo_children():
        widget.destroy()
    for widget in w.Labelframe_preferredGameLogs.winfo_children():
        widget.destroy()
    w.Scrolledtext_.delete(1.0,'end')
    global root_node, gpath, ppath
    gpath, ppath = [], []
    root_node = w.entry_assignRoot.get()
    print('Let us play argument game at node %s'%root_node)
    sys.stdout.flush()

def autoGenerate(p1):
    resume(p1)
    global nodes, attackers, defenders
    nodes_list = ['a','b','c','d','e','f','g']
    num = int(w.Spinbox_autoNodesNum.get())
    nodes = nodes_list[0:num]
    attackers, defenders = [], []
    edges_num = choice(range(num-1,2*num-1))
    for i in range(0,edges_num):
        rdm_range = range(0,num)
        rdm_node = choice(rdm_range)
        attackers.append(nodes[rdm_node])
        rdm_range.remove(rdm_node)
        rdm_node_ = choice(rdm_range)
        defenders.append(nodes[rdm_node_])
    #showArgumentationFramework(p1) 
    print('Argumentation framework has generated. The number of nodes is %d'%num)  
    sys.stdout.flush()

def pack_label(oneGame, path, mode):
    if mode == 'grounded':
        if oneGame not in gpath:
            gpath.append(oneGame) 
            print('a possible path for %s games is tracked'%mode)
            tempLabel = tk.Label(w.Labelframe_groundedGameLogs, text=' '.join(oneGame))
            tempLabel.configure(font="-family {Microsoft YaHei UI Light} -size 12")
            tempLabel.configure(background="#d9d9d9")    
            tempLabel.pack(expand=True,fill=None)
    elif mode == 'preferred':
        if oneGame not in ppath:
            ppath.append(oneGame) 
            print('a possible path for %s games is tracked'%mode)
            tempLabel = tk.Label(w.Labelframe_preferredGameLogs, text=' '.join(oneGame))
            tempLabel.configure(font="-family {Microsoft YaHei UI Light} -size 12")
            tempLabel.configure(background="#d9d9d9")    
            tempLabel.pack(expand=True,fill=None)
                       
def playOneTime(p1):
    id2game = {0:'grounded',1:'preferred'}
    af.build_argument_tree_without_duplicate(root_node)
    oneGame = af.random_dispute_tree(root_node,semantics=id2game[selectedButton.get()])
    if not selectedButton.get():
        pack_label(oneGame, gpath, 'grounded')
    elif selectedButton.get():        
        pack_label(oneGame, ppath, 'preferred')
    # print('[%s game]: '%id2game[selectedButton.get()], oneGame)
    w.Scrolledtext_.insert('insert', '[%s game]: '%id2game[selectedButton.get()]+' '.join(oneGame)+'\n')
    sys.stdout.flush()

def playThreeTimes(p1):
    id2game = {0:'grounded',1:'preferred'}
    af.build_argument_tree_without_duplicate(root_node)
    for i in range(3):
        oneGame = af.random_dispute_tree(root_node,semantics=id2game[selectedButton.get()])
        if not selectedButton.get():
            pack_label(oneGame, gpath, 'grounded')
        elif selectedButton.get():        
            pack_label(oneGame, ppath, 'preferred')
        # print('[%s game]: '%id2game[selectedButton.get()], oneGame)
        w.Scrolledtext_.insert('insert', '[%s game]: '%id2game[selectedButton.get()]+' '.join(oneGame)+'\n')
    sys.stdout.flush()     
            
def showArgumentationFramework(p1):
    global nodes, attackers, defenders, af
    af = ArgumentFramework()
    for node in nodes:
        af.add_node(node)
    for i in range(len(attackers)):
        af.add_edges(attackers[i],defenders[i])
    af.show_gram(showflag=0)    
    im = Image.open('framework.png')
    im = im.resize((w.Canvas1.winfo_width(), w.Canvas1.winfo_height()), Image.ANTIALIAS)
    im.save('framework.png', "png")
    img = ImageTk.PhotoImage(file='framework.png')
    w.Canvas1.create_image(0, 0, anchor='nw', image=img)
    w.Canvas1.image = img
    print(af.get_edges())
    sys.stdout.flush()

def cleanCanvas(p1):
    resume(p1)
    global nodes, defenders, attackers
    w.Canvas1.delete('all')
    w.entry_addNode.delete(0,'end')
    w.entry_attacker.delete(0,'end')
    w.entry_defender.delete(0,'end')
    nodes = []
    attackers = []
    defenders = []
    sys.stdout.flush()

def clearFrame(lf):
    for widget in lf.winfo_children():
        widget.destroy()
def resume(p1):
    w.Scrolledtext_.delete(1.0,'end')
    w.entry_assignRoot.delete(0,'end')
    clearFrame(w.Labelframe_groundedGameLogs)
    clearFrame(w.Labelframe_preferredGameLogs)
    clearFrame(w.Frame_hiddenWS)
    global gpath, ppath
    gpath, ppath = [], []
    root_node = []
    message.set(' ')
    print('Argument games have been re-started.')
    sys.stdout.flush()

def showCanvas(p1):
    resume(p1)
    showArgumentationFramework(p1)
    sys.stdout.flush()
  
def findStrategy(path):
    ## first prunning from bottom
    # even path
    dpath = [p for p in path if not len(p)%2] 
    duppath = path[:]
    # remove even path
    for dp in dpath:
        for rp in path:
            if dp[-2] in rp[::2]:
                try:
                    duppath.remove(rp)
                except ValueError:
                    pass
    ## then check from top
    # get all P's move
    P = []
    for e in duppath:
        for ee in e[::2]:
            P.append(ee)
    P = list(set(P))        
    children = af.get_childen_by_node(af.get_tree()) 
    dduppath = duppath[:]
    for pm in P:
        if not all([any([child in e[1::2] for e in duppath]) for child in children[pm]]):
            for wpm in dduppath:
                if pm in wpm[::2]: 
                    duppath.remove(wpm)       
    return duppath  
def conflictFreeCheck(strategies):
    children = af.get_childen_by_node(af.get_tree()) 
    strg = strategies[:]
    for s in strategies:
        if any([pm in children[rpm] for rpm in s[::2] for pm in s[::2]]):
            strg.remove(s)
    return strg        
def checkWinningStrategy(p1):
    clearFrame(w.Frame_hiddenWS)
    if not selectedButton.get():
        path = gpath
        mode = 'GROUNDED'
    elif selectedButton.get():   
        path = ppath    
        mode = 'PREFERRED' 
    ws = findStrategy(path)
    ws_cf = conflictFreeCheck(ws)
    if ws_cf:
        m = '[%s GAME] CONGRALATIONS! YOU FIND WINNING STRATEGRIES FOR NODE %s.'%(mode, root_node)
        message.set(m)
        for s in ws:
            tempLabel = tk.Label(w.Frame_hiddenWS, text='-'.join(s))
            tempLabel.configure(background="#d9d9d9")    
            tempLabel.configure(font="-family {Microsoft YaHei UI Light} -size 16")
            tempLabel.pack(expand=True,fill=None,ipadx=3,ipady=2)
    elif (not ws_cf) and ws:
        m = '[%s GAME] CONGRALATIONS! YOU FIND WINNING STRATEGRIES FOR NODE %s.\n(BUT CONFILTS HAPPEND)'%(mode, root_node) 
        message.set(m)   
        for s in ws:
            tempLabel = tk.Label(w.Frame_hiddenWS, text='-'.join(s))
            tempLabel.configure(background="#d9d9d9")    
            tempLabel.configure(font="-family {Microsoft YaHei UI Light} -size 16")
            tempLabel.pack(expand=True,fill=None,ipadx=3,ipady=2) 
    elif not ws:
        m = '[%s GAME] THERE IS NO WINNING STRATEGY FOR NODE %s.'%(mode, root_node)
        message.set(m)
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None  

if __name__ == '__main__':
    import simulator
    simulator.vp_start_gui()