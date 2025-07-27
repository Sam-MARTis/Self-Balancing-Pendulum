
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
    def __init__(self, id=0, neurons=None, genes=None):
        if neurons is None:
            neurons = []
        if genes is None:
            genes = []
        self.id = id
        self.neurons = neurons
        self.genes = genes

    def perform_computation(self, state):
        pass

    def crossover(self, other):
        pass

    def mutate(self, mutation_rate, mutation_strength):
        pass




