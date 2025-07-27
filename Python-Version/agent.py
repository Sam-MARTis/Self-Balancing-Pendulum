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
    
    def modify_gene(self, genePosition:int, mutation_strength_weight=0.1, mutation_strength_bias=0.1):
        if genePosition < 0 or genePosition >= len(self.genes):
            raise IndexError("Gene position out of bounds")
        gene = self.genes[genePosition]
        gene.weight += Helpers.rand(-mutation_strength_weight, mutation_strength_weight)
        gene.bias += Helpers.rand(-mutation_strength_bias, mutation_strength_bias)
        
        

    def mutate(self, mutation_strength_weight=0.1, mutation_strength_bias=0.1, gene_mutation_rate=0.2, gene_addition_rate=0.2, node_addition_rate=0.1):
        donothing_rate = 1 - (gene_mutation_rate + gene_addition_rate + node_addition_rate)
        if(donothing_rate < 0):
            raise ValueError("Mutation rates exceed 1.0")
        for gene in self.genes:
            if Helpers.rand(0, 1) < donothing_rate:
                continue
            if Helpers.rand(0, 1) < gene_mutation_rate :
                self.modify_gene(self.genes.index(gene), mutation_strength_weight, mutation_strength_bias)
            elif Helpers.rand(0, 1) < gene_addition_rate:
                new_gene = Gene(from_node_id=Helpers.randint(0, len(self.neurons)-1), to_node_id=Helpers.randint(0, len(self.neurons)-1), weight=Helpers.rand(-1.0, 1.0), bias=Helpers.rand(-1.0, 1.0))
                self.genes.append(new_gene)
            elif Helpers.rand(0, 1) < node_addition_rate:
                new_neuron = Neuron(id=len(self.neurons), value=0.0, activation_function=lambda x: x)
                self.insert_neuron(new_neuron, Helpers.randint(0, len(self.neurons)))
                new_gene = Gene(from_node_id=Helpers.randint(0, len(self.neurons)-1), to_node_id=new_neuron.id, weight=Helpers.rand(-1.0, 1.0), bias=Helpers.rand(-1.0, 1.0))
                self.genes.append(new_gene)
                
            
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
        pass
    

