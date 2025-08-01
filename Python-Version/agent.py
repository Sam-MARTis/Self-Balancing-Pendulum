from utils import Helpers, Action, State
import pickle
from typing import List, Callable

def relu (x:float) -> float:
    return max(0, x)

activation_function = relu
class Neuron:
    def __init__(self, id=0, value=0.0, activation_function=lambda x: x):
        self.id = id
        self.value = value
        self.activation_function:Callable = activation_function
        self.outgoing_genes:List['Gene'] = [] 
class Gene:
    def __init__(self, from_node:Neuron, to_node:Neuron, weight=0.0, bias=0.0):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.bias = bias
        
class Brain:
    def __init__(self, id:int=0, input_nodes_count:int = 4, output_nodes_count:int = 1, hidden_layers:List[int] = [2], weights_range = 4, bias_range = 4):

        self.id = id


        self.neurons:List[Neuron] = []
        self.genes:List[Gene] = []
        self.input_nodes_count = input_nodes_count
        self.output_nodes_count = output_nodes_count
        self.weights_range = weights_range
        self.bias_range = bias_range
        self.score = 0.0
        """
        There neurons are arranged in a 1D array. 
        Each neuron can only have inputs from neurons with a lower index.
        It can only output to neurons with a higher index.
        This means that the neurons are topologically ordered.
        The first neurons are the input neurons, and the last one is the output neurons.
        """
        id = 0
        for i in range(self.input_nodes_count):
            neuron = Neuron(id=id, value=0.0, activation_function=lambda x: x)
            id += 1
            self.neurons.append(neuron)
            
        
        for i in range(len(hidden_layers)):
            for j in range(hidden_layers[i]):
                neuron = Neuron(id=id, value=0.0, activation_function=activation_function)
                id += 1
                self.neurons.append(neuron)

        for i in range(self.output_nodes_count):
            neuron = Neuron(id=id, value=0.0, activation_function=lambda x: x)
            id += 1
            self.neurons.append(neuron)
            
            
            
        #Insert a bunch of genes now
        for i in range(20):
            weight = Helpers.rand(-weights_range, weights_range)
            bias = Helpers.rand(-bias_range, bias_range)
            try:
                self.insert_random_gene(weight=weight, bias=bias)
            except ValueError as e:
                print(f"Error inserting random gene: {e}")
                break
            
    
    # def initialize_random_brain(self, hidden_layers:List[int] = [4]):
    def copy(self, keep_score=False):
        """
        Create a copy of the brain.
        """
        new_brain = Brain(id=self.id, input_nodes_count=self.input_nodes_count, output_nodes_count=self.output_nodes_count)
        
        
        
        #Recheck this logic again later
        new_brain.neurons = [Neuron(neuron.id, neuron.value, neuron.activation_function) for neuron in self.neurons] 
        for neuron in new_brain.neurons:
            self_index = self.neurons.index(neuron)
            for gene in neuron.outgoing_genes:
                other_index = self.neurons.index(gene.to_node)
                new_gene = Gene(from_node=new_brain.neurons[self_index], to_node=new_brain.neurons[other_index], weight=gene.weight, bias=gene.bias)
                new_brain.neurons[self_index].outgoing_genes.append(new_gene)
                new_brain.genes.append(new_gene)
        new_brain.score = self.score if keep_score else 0.0
        return new_brain
    
    
    
    def reset_neurons(self):
        for neuron in self.neurons:
            neuron.value = 0.0

    
    def perform_computation(self, state:State)-> Action:
        for i in range(len(self.neurons)):
            if i < self.input_nodes_count:
                
                self.neurons[i].value = state.properties[i]
            else:
                self.neurons[i].value = 0.0
        
        for i in range(self.input_nodes_count):
            self.neurons[i].value = state.properties[i]
            
        for neuron in self.neurons:
            value = neuron.activation_function(neuron.value)
            for gene in neuron.outgoing_genes:
                gene.to_node.value += value * gene.weight + gene.bias
                
        
        result = Action(force=self.neurons[-1].value)
        return result
    

    
    def crossover(self, other):
        pass
    
    def insert_neuron(self, neuron:Neuron, position:int, insert_genes:bool=True):
        if position < self.input_nodes_count or position > len(self.neurons) - self.output_nodes_count:
            raise IndexError("Position out of bounds")
        
        if insert_genes:
            from_index = Helpers.randint(0, position - 1)
            to_index = Helpers.randint(position + 1, len(self.neurons)-1)
            neuron_from = self.neurons[from_index]
            neuron_to = self.neurons[to_index]
            
            
            
            new_gene = Gene(from_node=self.neurons[from_index], to_node=neuron, weight=Helpers.rand(-1.0, 1.0), bias=Helpers.rand(-1.0, 1.0))
            neuron_from.outgoing_genes.append(new_gene)
            new_gene2 = Gene(from_node=neuron, to_node=neuron_to, weight=Helpers.rand(-1.0, 1.0), bias=Helpers.rand(-1.0, 1.0))
            neuron.outgoing_genes.append(new_gene2)
            self.genes.append(new_gene)
            self.genes.append(new_gene2)
        
        self.neurons.insert(position, neuron)
    
    def modify_gene(self, genePosition:int, mutation_strength_weight=1.0, mutation_strength_bias=1.5):
        if genePosition < 0 or genePosition >= len(self.genes):
            raise IndexError("Gene position out of bounds")
        gene = self.genes[genePosition]
        gene.weight += Helpers.rand(-mutation_strength_weight, mutation_strength_weight)
        gene.bias += Helpers.rand(-mutation_strength_bias, mutation_strength_bias)
    
    def insert_random_gene(self, weight = 0.0, bias = 0.0):
        for i in range(20):
            random_node1 = self.neurons[Helpers.randint(0, len(self.neurons) - 1)]
            random_node2 = self.neurons[Helpers.randint(0, len(self.neurons))]
            for gene in random_node1.outgoing_genes:
                if gene.to_node == random_node2:
                    break
            else:
                new_gene = Gene(from_node=random_node1, to_node=random_node2, weight=weight, bias=bias)
                random_node1.outgoing_genes.append(new_gene)
                self.genes.append(new_gene)
                return True
        else:
            raise ValueError("Could not insert random gene after 20 attempts. Network likely full")
            
        
    # def insert_gene(self, from_node:Neuron, to_node:Neuron, weight =0.0, bias=0.0):
    #     for genes in from_node.outgoing_genes:
    #         if genes.to_node == to_node:
    #             return False
    #     new_gene = Gene(from_node=from_node, to_node=to_node, weight=weight, bias=bias)
        
    #     pass
    def mutate(self, mutation_strength_weight=1.9, mutation_strength_bias=1.5, 
            gene_mutation_rate=0.2, gene_addition_rate=0.2, neuron_addition_rate=0.1, number_of_mutations=3):
        
        total_rate = gene_mutation_rate + gene_addition_rate + neuron_addition_rate
        if total_rate > 1.0:
            raise ValueError("Mutation rates exceed 1.0")
        for _ in range(number_of_mutations):
            rand_val = Helpers.rand(0, 1)
            
            if rand_val < gene_mutation_rate:
                if len(self.genes) > 0: 
                    self.modify_gene(Helpers.randint(0, len(self.genes)-1), 
                                mutation_strength_weight, mutation_strength_bias)
            elif rand_val < gene_mutation_rate + gene_addition_rate:
                if len(self.neurons) >= 2:  # Need at least 2 neurons
                    from_node_index = Helpers.randint(0, len(self.neurons)-2)
                    to_node_index = Helpers.randint(from_node_index + 1, len(self.neurons)-1)
                    
                    from_node = self.neurons[from_node_index]
                    to_node = self.neurons[to_node_index]
                    
                    new_gene = Gene(from_node=from_node, to_node=to_node, 
                                weight=Helpers.rand(-1.0, 1.0), bias=Helpers.rand(-1.0, 1.0))
                    from_node.outgoing_genes.append(new_gene)
                    self.genes.append(new_gene)
            elif rand_val < total_rate:
                new_neuron = Neuron(id=len(self.neurons), value=0.0, activation_function=activation_function)
                # Insert between input and output layers
                if len(self.neurons) > self.input_nodes_count + self.output_nodes_count:
                    neuron_index = Helpers.randint(self.input_nodes_count, 
                                                len(self.neurons) - self.output_nodes_count)
                    self.insert_neuron(new_neuron, neuron_index, insert_genes=True)
            else:
                pass # No mutation

    def save_brain(self, filename):
        with open(filename, 'wb') as brain_file:  
            pickle.dump(self, brain_file)

    @staticmethod
    def load_brain(filename):
        """Load a brain from file"""
        with open(filename, 'rb') as brain_file:
            return pickle.load(brain_file)
        


