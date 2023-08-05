import toml
from .helpers import *

config = toml.load('./config.toml')


### CLASSES ###
class Species:
    def __init__(self):
        self.topFitness = 0
        self.staleness = 0
        self.genomes = []
        self.avg_fitness = 0

class Genome:
    def __init__(self, i_count = config['i_count'], o_count = config['o_count']):
        self.genes = []
        self.fitness = 0
        self.adj_fitness = 0
        self.global_rank = 0

        # Add input-output genes
        inno = 0
        for i in range(i_count):
            for j in range(i_count, i_count + o_count):
                self.genes.append(Gene(i, j, xav(i_count + 1), True, inno))
                inno += 1
        # Add bias genes
        for i in range(i_count, i_count + o_count):
            self.genes.append(Gene(i_count + o_count, i, xav(i_count + 1), True, inno))

'''
    # Turns genome into a standard genome
    def standard_initialization(self, i_count = config['i_count'], o_count = config['o_count']):
        # Add input-output genes
        inno = 0
        for i in range(i_count):
            for j in range(i_count, i_count + o_count):
                self.genes.append(Gene(i, j, xav(i_count + 1), True, inno))
                inno += 1
        # Add bias genes
        for i in range(i_count, i_count + o_count):
            self.genes.append(Gene(i_count + o_count, i, xav(i_count + 1), True, inno))
'''

class Gene:
    def __init__(self, origin = 0, destination = 0, weight = 0.0, enabled = True, innovation = 0):
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

class Node:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.value = 0

    def add_input(self, inp):
        self.inputs.append(inp)
    
    def add_output(self, out, weight):
        self.outputs.append((out, weight))

    def remove_input(self, inp):
        try:
            self.inputs.remove(inp)
        except:
            print('This error should never occur. If it does, idek what to do.')

### FUNCTIONS ###
# Fires a genome with a given input
def eval(gen, inp, i_count = config['i_count'], o_count = config['o_count']):
    
    # Determine which genes are active in a given genome
    # Makes a list of the enabled genes in a genome
    genes = [gene for gene in gen.genes if gene.enabled]

    # Determine which nodes have to be made
    # Creates a dictionary that ties each node id to a node object
    network = dict.fromkeys(set([n.origin for n in genes] + [n.destination for n in genes]))
    for i in network:
        network[i] = Node()

    # Build a network of nodes based on genetic information
    for gene in genes:
        # initialize non-input and non-bias nodes
        # pre-fire input and bias nodes
        if not (gene.origin in range(i_count) or gene.origin == (i_count + o_count)):
            network[gene.destination].add_input(gene.origin)
            network[gene.origin].add_output(gene.destination, gene.weight)
        elif gene.origin in range(i_count):
            network[gene.destination].value += inp[gene.origin] * gene.weight
        else:
            network[gene.destination].value += gene.weight

    # Fire off the network
    fired = False
    while not fired:
        fired = True
        # For each node
        for node in network:
            # If all inputs have been given
            if network[node].inputs == []:
                # Update the values of destination nodes
                # by adding the product of the activated
                # input node value and the edge's weight
                # Also remove input from destination
                for out in network[node].outputs:
                    network[out[0]].value += sig(network[node].value) * out[1]
                    network[out[0]].remove_input(node)

                # Set node's inputs to None to stop multiple
                # firings of the same node
                network[node].inputs = None

                fired = False

    # Return the softmaxed activated output layer
    return softmax([
        sig(network[node].value) for node in range(i_count, i_count + o_count)
    ])
