import pygame
import math
import sys
from utils import vec2, system, Action, State
from agent import Brain, Neuron, Gene
from arena import Cart, Pendulum, Arena


# Pygame Setup



WIDTH, HEIGHT = 800, 600
ARENA_WIDTH = 3
CART_WIDTH = 0.3
CART_HEIGHT = 0.1
CART_MASS = 1.0
PENDULUM_LENGTH = 0.3

PENDULUM_MASS = 0.5
PENDULUM_THICKNESS = 0.02
PENDULUM_BOB_RADIUS = 0.03



CART_MAX_SPEED = 5
MAX_ACCELERATION = 20
CART_BUTTON_FORCE = 20
SWING_FRICTION_CONSTANT = 0.1
GRAVITY = 9.81
LATERAL_FRICTION_CONSTANT = 5.0


pendulum_angle = math.radians(30)
magnification = WIDTH / ARENA_WIDTH
cart_x = ARENA_WIDTH/2
cart_y =  HEIGHT / (2 * magnification)







"""
struct Neuron{
    int id;
    float value;
    std::function<float(float)> activation_function;
    // Default constructor
    Neuron(int id = 0, float value = 0.0f, std::function<float(float)> activation_function = [](float x) { return x; })
        : id(id), value(value), activation_function(activation_function) {}
};

struct Gene{
    int from_node_id;
    int to_node_id;
    float weight;
    float bias;
    // Default constructor
    Gene(int from_node_id = 0, int to_node_id = 0, float weight = 0.0f, float bias = 0.0f)
        : from_node_id(from_node_id), to_node_id(to_node_id), weight(weight), bias(bias) {}
};

struct Brain{
    int id;
    std::vector<Neuron> neurons;
    std::vector<Gene> genes;

    // Default constructor
    Brain(int id = 0, std::vector<Neuron> neurons = {}, std::vector<Gene> genes = {})
        : id(id), neurons(std::move(neurons)), genes(std::move(genes)) {}
    
    Action perform_computation(const State& state);
    void crossover(const Brain& other);
    void mutate(float mutation_rate, float mutation_strength);

    
    
    
};
"""


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pendulum on Cart")
    clock = pygame.time.Clock()
    
    environment = system(1, WIDTH, HEIGHT, ARENA_WIDTH, CART_MASS, CART_WIDTH, CART_HEIGHT, PENDULUM_LENGTH, PENDULUM_MASS, PENDULUM_THICKNESS, PENDULUM_BOB_RADIUS, CART_MAX_SPEED, MAX_ACCELERATION, SWING_FRICTION_CONSTANT, GRAVITY, LATERAL_FRICTION_CONSTANT)
    pendulum_angle = math.radians(30)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # cart = Cart(screen, CART_MASS, CART_WIDTH, CART_HEIGHT, cart_x, environment)
    # pendulum = Pendulum(screen, cart, PENDULUM_LENGTH, PENDULUM_MASS, pendulum_angle, environment)
    # cart.pendulum = pendulum
    Arena = Arena(environment)
    Arena.set_screen(screen)
    
    

    # Main loop
    clock = pygame.time.Clock()
    # pendulum.angular_velocity = 0.0
    while True:
        screen.fill((0, 0, 0))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # force = 0
        act = Action(0)
        if keys[pygame.K_LEFT]:
            # force = -CART_BUTTON_FORCE 
            act.force = -CART_BUTTON_FORCE
        elif keys[pygame.K_RIGHT]:
            act.force = CART_BUTTON_FORCE
        dt = clock.tick(60) / 1000.0
        environment.dt = dt

        Arena.step(dt, act)

        
        # cart.step(dt)

        # screen.fill((255, 255, 255))
        # cart.draw()
        # pendulum.draw()
        # Arena.cart.draw()
        Arena.draw()
        

        pygame.display.flip()