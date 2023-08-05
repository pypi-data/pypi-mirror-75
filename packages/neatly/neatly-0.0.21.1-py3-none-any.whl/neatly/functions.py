### NEATLY PRIMARY FUNCTIONS ###

import numpy as np
import random
import toml
from .helpers import sig, softmax
from .classes import Node, Species

cfg = toml.load('./config.toml')

# Fires a genome with a given input
def eval(gen, inp, i_count = cfg['i_count'], o_count = cfg['o_count']):
    
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
    # If stochastic, softmax. If deterministic, just return
    if cfg['decision_method'] == 0:
        return softmax([
            sig(network[node].value) for node in range(i_count, i_count + o_count)
        ])
    elif cfg['decision_method'] == 1:
        return [sig(network[node].value) for node in range(i_count, i_count + o_count)]
    else:
        print('invalid decision method. check/change config.toml')

# Speciates a population of genomes
def speciate(
    almanac,
    pop,
    delta_t = cfg['delta_t'],
    c1 = cfg['excess_c'],
    c2 = cfg['disjoint_c'],
    c3 = cfg['weight_c'],
    n_t = cfg['size_norm_t']
):
    unsorted = pop[:] # Members of the population that haven't been put into a species
    volxplus1 = [] # The next volume of the almanac
    refs = [] # Genomic reference point for each species

    # Choose new species representatives
    # For each species in the previous generation
    for s in almanac:
        # Use a random member of each species for making the next volume of the almanac
        refs.append((random.choice(s.genomes), len(volxplus1)))
        volxplus1.append(Species(s.staleness))

    # While there are unsorted genomes
    while unsorted:
        # If there are no remaining species references, create a new reference and species
        if not refs:
            refs.append(random.choice(unsorted), len(volxplus1))
            volxplus1.append(Species())

        # For each unsorted genome, determine if said genome fits into the current reference species
        r = refs[0] #set current reference species
        for g in reversed(unsorted):
            # Establish genomic innovation numbers
            r_i = set(i.innovation for i in r[0].genes)
            g_i = set(i.innovation for i in g.genes)

            # Calculate genomic distance between reference genome and unsorted genome
            overlap = r_i & g_i
            r_unique = r_i - g_i
            g_unique = g_i - r_i
            smallmax = max(r_i) if max(r_i) < max(g_i) else max(g_i)
            disjoint = len([0 for i in r_unique|g_unique if i <= smallmax])
            excess = len(r_unique|g_unique) - disjoint
            w_bar = np.average(np.abs(np.array([i.weight for i in r[0].genes if i.innovation in overlap]) - np.array([i.weight for i in g.genes if i.innovation in overlap])))
            n = max(len(r_i), len(g_i)) if max(len(r_i), len(g_i)) >= n_t else 1.0
            delta = ((c1 * excess)/n) + ((c2 * disjoint)/n) + (c3 * w_bar)

            if delta <= delta_t:
                volxplus1[r[1]].genomes.append(g)
                unsorted.remove(g)
        refs.remove(r)

    return volxplus1
