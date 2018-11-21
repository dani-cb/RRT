import os
import csv
import sys
import math
import matplotlib
import collections
import numpy as np
import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt

###########################################################################################################
#generating a random tree
def random_tree (size):

	#0) Defina n, o número de vértices na árvore
	#size = int(input('size of the subtree: '))
	#print()
	global G
	global nodes
	#1) Inicialize um grafo com um vértice, com rótulo 1.
	G = nx.Graph()
	G.add_node(0)

	#2) Para i=1 até n-1 faça
	for i in range(0,size-1):
		#3)   Escolha um vértice v ao acaso, de forma uniforme entre [1, k]
		node = math.trunc(np.random.uniform(0,i+1))
		#print(node)
		#4)   Crie um novo vértice com rótulo k+1 e conecte no vértice v escolhido, aumentando o grafo
		G.add_node(i+1)
		G.add_edge(node,i+1)

	#generating a list of nodes
	nodes = nx.nodes(G)

	return G
	return nodes

###########################################################################################################
#finding the root
def find_root(G):
	global root

	#1) Escolha um vértice qualquer da árvore e chame de raiz.
	root = math.trunc(np.random.uniform(0,len(nodes)))
	#print('the initial root is: ', root)

	#2) Execute uma BFS a partir deste vértice para definir uma orientação (quem é pai de quem).
	#BFS
	bfs_result = list(nx.bfs_edges(G,root))

	#3) Inicie o processo de contagem do tamanho das subarvores, conforme o algoritmo que você já implementou (começando com as folhas e subindo).
	#parent's list
	parent = [0]*len(nodes)
	parent[root] = -1
	for i in bfs_result:
		parent[i[1]] = i[0]
			
	#child list
	child = [0]*len(nodes)

	for i in parent:
		if i >= 0: 
			child[i] = child[i] + 1 

	#leaf list
	leaf = [i for i, x in enumerate(child) if x == 0]

	#4) Pare o algoritmo de contagem ao encontrar um vértice cujo tamanho da subarvore enraizada nele (em relação ao vértice raiz escolhido no passo 1) 
	#seja maior ou igual a n/2, onde n é o número de vértices da árvore.

	#calculating the size of the subtree
	size = [0]*len(nodes)
	size[root] +=1

	while leaf != []:
		new_leaf = []
		for i in leaf:
			size[i] += 1
			size[parent[i]] = size[parent[i]] + size[i]
			child[parent[i]] -= 1
			half = math.trunc(len(nodes)/2)
			max_size = np.amax(size)
			if max_size >= half: 
				root = parent[i] 
				new_leaf = []
			if child[parent[i]] == 0:
				new_leaf.append(parent[i])
			if parent[i] == root:
				new_leaf = []

			leaf = new_leaf

	#5) Retorne o vértice acima, como sendo a raiz da epidemia.
	#print('the root that has as the size of the tree the half of the vertices is', root)

	return root
###########################################################################################################
def only_unique(all_roots):
    l = []
    for i in all_roots:
        if i not in l:
            l.append(i)
    l.sort()
    return l

###########################################################################################################
if __name__=='__main__':
	np.random.seed(int(sys.argv[1]))
	#size = 10 #demora 3' 15"
	size = 1000 #demora 2h
	all_roots = [-1]*n #root of every iteration  
	repeat = [0]*size #how many time the same root apears in the simulation
	frequency = [0]*size #repeat / n
	log_frequency = [0]*size
	freq = [0]*size

	G = random_tree(size)
	root = find_root(G)
	freq[root] += 1 		
	all_roots[i] = root
	uniques = only_unique(all_roots)
	color_map = []
	for node in G:
	    if node == root:
		color_map.append('firebrick')
	    else: color_map.append('darksalmon')      
	nx.draw(G,node_color = color_map,with_labels = True)
	#create new directory
	#output_dir = "C:/Users/dani_/OneDrive/Área de Trabalho/tese/script_python/teste_100"
	#output_dir = "C:/Users/dani_/OneDrive/Área de Trabalho/tese/script_python/teste_1000"
	output_dir = "C:/Users/dani_/OneDrive/Área de Trabalho/tese/script_python"
	plt.savefig(output_dir+'/fig'+str(i)+'.png')
	plt.close()


	for j in range(0,size):
		frequency[j] = freq[j]/n


	for k in range(0,size):
		if frequency[k] == 0:
			log_frequency[k] = 0
		else:	
			log_frequency[k] = math.log10(frequency[k])

	#plots
	plt.plot(frequency)
	plt.xlabel('nodes')
	plt.ylabel('frequency')
	#output_dir = "C:/Users/dani_/OneDrive/Área de Trabalho/tese/script_python/teste_100"
	#output_dir = "C:/Users/dani_/OneDrive/Área de Trabalho/tese/script_python/teste_1000"
	plt.savefig(output_dir+'/frequency'+'.png')
	plt.close()

	plt.plot(log_frequency)
	plt.xlabel('nodes')
	plt.ylabel('log-frequency')
	plt.savefig(output_dir+'/log_frequency'+'.png')
	
