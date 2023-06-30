import sys

# Reads the file and returns an array of lines found in the file
def readFile(filename):
    with open(filename, "r") as fileObj: # opens the file in read mode
        inputlines = fileObj.read().splitlines()  # puts the file into an array
        fileObj.close()
        return inputlines

# Class describing a node of the ising tree
class Node(object):
    def __init__(self, val, children, nodeweight, parent_node_edgeweight):
        self.val =val
        self.children = children
        self.nodeweight = nodeweight
        self.parent_node_edgeweight = parent_node_edgeweight

# Class describing an edge of the ising tree
class Edge(object):
    def __init__(self, parentnode_value, node_value, edgeweight):
        self.parentnode_value = parentnode_value
        self.node_value = node_value
        self.edgeweight = edgeweight

# A method to read the array returned by readfile method and builds the tree
def parse_Input(inputlines):
    nodedict = {}
    nodelist = []
    edgelist = []
    nodelist_values = []
    edgelist_values = []
    number_of_nodes = 0

# Here we are looping through the strings in the array and parse the necessary inputs used to build the tree
    for line in inputlines:
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            number_of_nodes = int(line.split(' ')[2])
            number_of_weights = int(line.split(' ')[3])
        else:
            parentnode_value = int(line.split(' ')[0])
            childnode_value = int(line.split(' ')[1])
            if parentnode_value == childnode_value:
                nodeweight = int(line.split(' ')[2])
                node = Node(parentnode_value, [], nodeweight, 0)
                nodelist.append(node)
                nodelist_values.append(node.val)
                nodedict[node.val] = node
            else:
                edgeweight = int(line.split(' ')[2])
                edge = Edge(parentnode_value, childnode_value, edgeweight)
                edgelist_values.append([edge.parentnode_value, edge.node_value])
                edgelist.append(edge)

# Creating nodes that do not show up in the file
    if len(nodelist) != number_of_nodes:
        all_nodes = set(range(number_of_nodes))
        missing_node_values = all_nodes - set(nodelist_values)
        for missing_node_value in missing_node_values:
            missing_node = Node(missing_node_value, [], 0, 0)
            nodelist.append(missing_node)
            nodelist_values.append(missing_node_value)
            nodedict[missing_node_value] = missing_node

    for edge in edgelist:
        parentnode = nodedict[edge.parentnode_value]
        node = nodedict[edge.node_value]
        node.parent_node_edgeweight = edge.edgeweight
        parentnode.children.append(node)
    return nodedict

# Class used to encapsulate the results of the calculate_min_energy_dynamic function
class MinEnergyConfiguration(object):
    def __init__(self, min_energy, spin_configuration):
        self.min_energy = min_energy
        self.spin_configuration = spin_configuration

# Recursive/dynamic programming algorithm to calculate the minimum energy and its corresponding spin configuration for the tree
def calculate_min_energy_dynamic(node, parent_spin):
# checks to see if the values of energies corresponding to the nodes are already calculated
    if (node.val, parent_spin) in energydict:
       return energydict[(node.val, parent_spin)]

    min_energy = sys.maxsize                # start of function
    min_spin_configuration = {}
    spin_list = [0, 1, 2, 3]

    for node_spin in spin_list:
        energy = 0
        spin_configuration = {}

        if node.children == []:  # checks if node is a leafnode
            energy = node.nodeweight * node_spin + node.parent_node_edgeweight * parent_spin * node_spin
            spin_configuration[node.val] = node_spin
        else:
            energy = node.nodeweight * node_spin + node.parent_node_edgeweight * parent_spin * node_spin
            spin_configuration[node.val] = node_spin
            for child in node.children:
                Min_Energy_Configuration_of_subtree_rooted_at_child = calculate_min_energy_dynamic(child, node_spin)
                energy_of_subtree_rooted_at_child = Min_Energy_Configuration_of_subtree_rooted_at_child.min_energy
                spin_configuration_of_subtree_rooted_at_child = Min_Energy_Configuration_of_subtree_rooted_at_child.spin_configuration
                energy = energy_of_subtree_rooted_at_child + energy
                spin_configuration.update(spin_configuration_of_subtree_rooted_at_child)

        if energy < min_energy:
            min_energy = energy
            min_spin_configuration = spin_configuration
        #print(node.val, parent_spin, min_energy)

    optimal_solution = MinEnergyConfiguration(min_energy, min_spin_configuration)
    energydict[(node.val, parent_spin)] = optimal_solution
    #storing the calculated value for future use in the recursion

    return optimal_solution



def print_spins(spin_configuration):
    result = ''
    for node_val in range(len(spin_configuration)):
        if spin_configuration[node_val] == 0:
            result = result + ')'
        elif spin_configuration[node_val] == 1:
            result = result + '!'
        elif spin_configuration[node_val] == 2:
            result = result + '@'
        else:
            result = result + '#'
    print(result)
    return result

if __name__ == "__main__":
    energydict = {}
    treedict = parse_Input(readFile('inp3.txt'))
    parent_spin_of_root = 0
    result = calculate_min_energy_dynamic(treedict[0], parent_spin_of_root)
    print(result.min_energy)
    print_spins(result.spin_configuration)
