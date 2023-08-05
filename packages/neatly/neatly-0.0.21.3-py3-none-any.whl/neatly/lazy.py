### FUNCTIONS FOR EASY SETUP ###

import toml
from .classes import Genome

try:
    cfg = toml.load('./config.toml')
except:
    cfg = {
        'pop_size': 100
    }

# Return a random population of basic genomes
def initialize_population():
    return [Genome() for i in range(cfg['pop_size'])]
