### NEATLY PRIMARY FUNCTIONS ###

import toml
from .helpers import sig, softmax
from .classes import Node

config = toml.load('./config.toml')

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

    # Return the activated output layer
    # If stochastic, softmax the layer as well
    # If deterministic, do nothing else
    out = [sig(network[node].value) for node in range(i_count, i_count + o_count)]
    return (softmax([out]) if config['decision_method'] == 0 else out)
