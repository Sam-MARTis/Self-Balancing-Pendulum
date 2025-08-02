
import pygame
import time
import pickle

from typing import List


from arena import Cart, Pendulum, Arena
from utils import system, Action, State, vec2, Helpers
from agent import Brain, Neuron, Gene
from interface import Interface


class Generation:

    def __init__(self, screen: pygame.Surface, environment, brains_count=50, input_nodes_count=4, output_nodes_count=1, dt=0.01, time_train=100, render=False):
        self.screen = screen
        self.environment = environment
        self.interfaces: List[Interface] = []
        self.brains_count = brains_count
        self.input_nodes_count = input_nodes_count
        self.output_nodes_count = output_nodes_count
        self.dt = dt
        self.time_train = time_train
        self.render = render
        self.scores: List[float] = []
        self.evaluation_completed = False
        
        
        for i in range(self.brains_count):
            arena = Arena(environment)
            brain = Brain(id=i, input_nodes_count=self.input_nodes_count, output_nodes_count=self.output_nodes_count)
            interface = Interface(arena=arena, agent=brain, screen=self.screen, dt=self.dt, time_train=self.time_train, render=self.render)
            self.interfaces.append(interface)
            
        

    def evaluate_agents(self) -> List[float]:
        self.scores = []
        for i in range(self.brains_count):
            score = self.interfaces[i].evaluate()
            self.scores.append(score)
        self.evaluation_completed = True
        return self.scores
                
        
    
    
    
    def create_next_generation(self) -> None:
        if not self.evaluation_completed:
            raise Exception("Evaluation not completed. Please evaluate the agents before creating the next generation.")
        new_generation:List[Interface] = []
        # Sort agents based on performance and generate selection probabiltiy
        
        # APply softmax to scores to get selection probabilities
        
        sorted_indices = sorted(range(len(self.scores)), key=lambda k: self.scores[k], reverse=True)
        sorted_scores = [self.scores[i] for i in sorted_indices]
        normalized_scores = Helpers.square_normalize(sorted_scores)
        top_count = int(self.brains_count * 0.2)
        
        #Take top 20% as is
        for i in range(top_count):
            new_generation.append(self.interfaces[sorted_indices[i]].copy())
        
        # probability_counter = normalized_scores[0]
        # random_selection = Helpers.random_float(0, 1)
        for i in range(self.brains_count - top_count):
            index = Helpers.sample(normalized_scores)
            new_interface = self.interfaces[sorted_indices[index]].copy()
            new_interface.agent.mutate(mutation_rate=0.2, mutation_strength=0.3)
            new_generation.append(new_interface)
        self.interfaces = new_generation
        self.scores = []
        self.evaluation_completed = False
        pass
    
    def save_generation(self, filename):
        generation_file = open(filename, 'ab')
        pickle.dump(self, generation_file)
    

