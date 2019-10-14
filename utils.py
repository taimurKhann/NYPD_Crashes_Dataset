import numpy as np

def get_collision_list_by_borough(borough,db):
	'''Return all collisions in given borough'''
	return db.Crashes_Collection.find({"borough":{"$eq":borough}})

def closest_node(node, nodes):
	'''Return index of point closed to given point'''
	nodes = np.asarray(nodes)
	deltas = nodes - node
	dist_2 = np.einsum('ij,ij->i', deltas, deltas)
	return np.argmin(dist_2)
