### NEATLY CLASSES ###

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
