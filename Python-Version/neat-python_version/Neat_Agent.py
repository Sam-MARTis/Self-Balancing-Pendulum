import neat
import pygame
from game import Cart, Pendulum
import utils
import os

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
MAX_ACCELERATION = 30
MAX_FORCE = CART_MASS*MAX_ACCELERATION
CART_BUTTON_FORCE = 20
SWING_FRICTION_CONSTANT = 0.1
GRAVITY = 9.81
LATERAL_FRICTION_CONSTANT = 0.1

pendulum_angle = utils.Helpers.radians(0)
magnification = WIDTH / ARENA_WIDTH
cart_x = ARENA_WIDTH/2
cart_y =  HEIGHT / (2 * magnification)


def eval_genomes(genomes, config):

    environment = utils.system(1, WIDTH, HEIGHT, ARENA_WIDTH,
                               CART_MASS, CART_WIDTH, CART_HEIGHT,
                               PENDULUM_LENGTH, PENDULUM_MASS, PENDULUM_THICKNESS, PENDULUM_BOB_RADIUS,
                               CART_MAX_SPEED, MAX_ACCELERATION, SWING_FRICTION_CONSTANT,
                               GRAVITY, LATERAL_FRICTION_CONSTANT)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    for i, (genome_id, genome) in enumerate(genomes):
        dt = environment.dt
        cart = Cart(screen, CART_MASS, CART_WIDTH, CART_HEIGHT, cart_x, environment)
        pendulum = Pendulum(screen, cart, PENDULUM_LENGTH, PENDULUM_MASS, pendulum_angle, environment)
        cart.pendulum = pendulum

        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            out_force = net.activate((cart.x,
                                      cart.x + pendulum.length * utils.math.cos(pendulum.angle),
                                      environment.cart_y + pendulum.length * utils.math.sin(pendulum.angle),
                                      pendulum.angular_velocity))[0] * (MAX_FORCE/2)
            
            dt = clock.tick(60)/1000.0
            environment.dt = dt
            cart.accelerate(out_force)
            cart.step(dt)
            cart.draw()
            pendulum.draw()
            pygame.display.flip()

            if 0 < utils.math.degrees(pendulum.angle) <= 10 or utils.math.degrees(pendulum.angle) >= 350:
                genome.fitness += 1
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000

            print(f'Force = {out_force}, Time = {elapsed_time}')
            if(elapsed_time > 5):
                break


def run(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-10')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 5)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    run(config)