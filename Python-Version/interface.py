import pygame
import time
import pickle

from typing import List


from arena import Cart, Pendulum, Arena
from utils import system, Action, State, vec2, Helpers
from agent import Brain, Neuron, Gene






class Interface:
    def __init__(self, arena:Arena, agent:Brain, screen:pygame.Surface, dt=0.01, time_train = 100, render:bool = False):
        self.arena = arena
        self.agent = agent
        self.screen = screen
        self.dt = dt
        self.time_train = time_train
        self.render = render
        arena.set_screen(screen)
        
    
        
        
    
    def evaluate(self):
        """
        Evaluate the agent in the arena for a specified time.
        """
        time_elapsed = 0
        while time_elapsed < self.time_train:
            
            
            time_elapsed += self.dt
            state = self.arena.get_state()
            action = self.agent.perform_computation(state)
            print(action.force)
            self.arena.step(self.dt, action)
            if self.render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                        # sys.exit()
                self.screen.fill((0, 0, 0))
                self.arena.draw()
                time.sleep(self.dt)
                pygame.display.flip()
            if state.pendulum_angle < Helpers.radians(-20) or state.pendulum_angle > Helpers.radians(340):
                self.agent.score += 1 *self.dt
            if state.cart_x < -self.arena.system.ARENA_WIDTH / 4 or state.cart_x > 3*self.arena.system.ARENA_WIDTH / 4:
                self.agent.score -= 0.05 *self.dt
        
        print(f"Final Score: {self.agent.score}")
        
    def copy(self):
        self.arena.reset()
        new_interface = Interface(arena=self.arena, agent=self.agent.copy(), screen=self.screen, dt=self.dt, time_train=self.time_train, render=self.render)
        return new_interface
                






class Generation:

    def __init__(self, screen: pygame.Surface, brains_count=1, input_nodes_count=4, output_nodes_count=1):
        self.screen = screen
        self.interfaces: List[Interface] = []
        
        
    def evaluate_agents(self, fitnessfunction):
        
        pass
    
    
    
    def create_next_generation(self):
        # Sort agents based on performance and generate selection probabiltiy
        
        #Take top 20% as is
        
        #Sample the remaining 80% of the new generation from the current generation.
        
        #Peform crossover and mutation on the 80% to create new agents.


        #Return generation

        pass
    
    def save_generation(self, filename):
        generation_file = open(filename, 'ab')
        pickle.dump(self, generation_file)
    

