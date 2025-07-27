from utils import Helpers
import pickle


class Neuron:
    def __init__(self, id=0, value=0.0, activation_function=lambda x: x):
        self.id = id
        self.value = value
        self.activation_function = activation_function
class Gene:
    def __init__(self, from_node_id=0, to_node_id=0, weight=0.0, bias=0.0):
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.weight = weight
        self.bias = bias
        
class Brain:
    def __init__(self, id:int=0, neurons=None, genes=None):
        if neurons is None:
            neurons = []
        if genes is None:
            genes = []
        self.id = id
        self.neurons = neurons
        self.genes = genes
    def reset_neurons(self):
        for neuron in self.neurons:
            neuron.value = 0.0
    
    
    def perform_computation(self, state):
        pass
    

    def crossover(self, other):
        pass
    
    def insert_neuron(self, neuron:Neuron, position:int):
        if position < 0 or position > len(self.neurons):
            raise IndexError("Position out of bounds")
        self.neurons.insert(position, neuron)
    
    def insert_gene(self, gene:Gene, position:int):
        if position < 0 or position > len(self.genes):
            raise IndexError("Position out of bounds")
        self.genes.insert(position, gene)
        

    def mutate(self, mutation_rate, mutation_strength_weight=0.1, mutation_strength_bias=0.1):
        for gene in self.genes: #Replace with tower based sampling
            if Helpers.rand(0, 1) < mutation_rate: 
                gene.weight += Helpers.rand(-mutation_strength_weight, mutation_strength_weight)
                gene.bias += Helpers.rand(-mutation_strength_bias, mutation_strength_bias)
        pass
    
    def save_brain(self, filename):
        brain_file = open(filename, 'ab')
        pickle.dump(self, brain_file)



class Generation:
    def __init__(self, brains_count=1, input_nodes = 4, outut_nodes = 1):
        self.brains = []
        for i in range(brains_count):
            neurons = [Neuron(id=j) for j in range(input_nodes + outut_nodes)]
            genes = [Gene(from_node_id=j, to_node_id=(j + 1) % (input_nodes + outut_nodes), weight=1.0, bias=0.0) for j in range(input_nodes)]
            self.brains.append(Brain(id=i, neurons=neurons, genes=genes))
            
    def evaluate_agents(self, fitnessfunction):
        pass
    
    
    
    def create_next_generation(self):
        # Sort agents based on performance and generate selection probabiltiy
        
        #Take top 20% as is
        
        #Sample the remaining 80% of the new generation from the current generation.
        
        #Peform crossover and mutation on the 80% to create new agents.
        
        
        #Return genertion
        
        pass
    
    def save_generation(self, filename):
        generation_file = open(filename, 'ab')
        pickle.dump(self, generation_file)
    

