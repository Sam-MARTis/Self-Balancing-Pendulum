import pygame
import math
import sys

# Pygame Setup



WIDTH, HEIGHT = 800, 600
ARENA_WIDTH = 3
CART_WIDTH = 0.3
CART_HEIGHT = 0.1
CART_MASS = 1.0
PENDULUM_LENGTH = 0.3

PENDULUM_MASS = 1.0
PENDULUM_THICKNESS = 0.02
PENDULUM_BOB_RADIUS = 0.03



CART_MAX_SPEED = 5
MAX_ACCELERATION = 40
CART_BUTTON_FORCE = 8
SWING_FRICTION_CONSTANT = 0.1
GRAVITY = 9.81
LATERAL_FRICTION_CONSTANT = 0.1


pendulum_angle = math.radians(30)
magnification = WIDTH / ARENA_WIDTH
cart_x = ARENA_WIDTH/2
cart_y =  HEIGHT / (2 * magnification)




class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return vec2(self.x / scalar, self.y / scalar)

class Cart:
    def __init__(self, screen, mass, width, height):
        self.mass = mass
        self.screen = screen
        self.width = width
        self.height = height
        self.x = cart_x
        self.vx = 0
        self.accx = 0
        self.pendulum: Pendulum = None
        
    def accelerate(self, force):
        # Calculate acceleration based on force and gravity
        acceleration = (force/ self.mass)
        self.accx = max(-MAX_ACCELERATION, min(MAX_ACCELERATION, acceleration))
    
        
    def step(self, dt):
        oldvx = self.vx
        vx = self.vx +  (self.accx - (LATERAL_FRICTION_CONSTANT * self.vx) )*dt
        self.vx = max(-CART_MAX_SPEED, min(CART_MAX_SPEED, vx))
        accx = (self.vx - oldvx) / dt
        pendulum_force = vec2(-self.pendulum.mass * accx, -self.pendulum.mass * GRAVITY)
        
        # self.vx -= * dt
        self.x += self.vx * dt
        
        self.accx = 0
        self.pendulum.update(dt, pendulum_force)
    
    def draw(self):
        cart_rect = pygame.Rect((self.x - self.width/ 2.0)*magnification, (cart_y - self.height/2)*magnification, self.width*magnification, self.height*magnification)
        pygame.draw.rect(self.screen, (0, 0, 255), cart_rect)
    
        
    def getState(self):
        return self.x, self.y, self.vx

class Pendulum:
    def __init__(self, screen, cart, length, mass, angle):
        self.screen = screen
        self.cart = cart
        self.length = length
        self.angle = angle
        self.mass = mass
        self.MOI_inv = 1.0 / (mass * length * length)
        

    def update(self, dt, force: vec2):
        torque = (-force.x * self.length * math.sin(self.angle) +
                  force.y * self.length * math.cos(self.angle)) - SWING_FRICTION_CONSTANT * self.angular_velocity
        angular_acceleration = torque * self.MOI_inv
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.angle = self.angle % (2 * math.pi) 
        
        pass
    
    def draw(self):
        pivot_x = self.cart.x
        pivot_y = cart_y    
        pendulum_x = pivot_x + self.length * math.cos(self.angle)
        pendulum_y = pivot_y - self.length * math.sin(self.angle)

        pygame.draw.line(self.screen, (255, 255, 255), (pivot_x*magnification, pivot_y*magnification), (pendulum_x*magnification, pendulum_y*magnification), math.ceil(PENDULUM_THICKNESS*magnification))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(pendulum_x*magnification), int(pendulum_y*magnification)), math.ceil(PENDULUM_BOB_RADIUS*magnification))

    








if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pendulum on Cart")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    cart = Cart(screen, CART_MASS, CART_WIDTH, CART_HEIGHT)
    pendulum = Pendulum(screen, cart, PENDULUM_LENGTH, PENDULUM_MASS, pendulum_angle)
    cart.pendulum = pendulum

    # Main loop
    clock = pygame.time.Clock()
    pendulum.angular_velocity = 0.0
    while True:
        screen.fill((0, 0, 0))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        force = 0
        if keys[pygame.K_LEFT]:
            force = -CART_BUTTON_FORCE
        elif keys[pygame.K_RIGHT]:
            force = CART_BUTTON_FORCE

        cart.accelerate(force)
        dt = clock.tick(60)/1000
        cart.step(dt)

        # screen.fill((255, 255, 255))
        cart.draw()
        pendulum.draw()
        
        pygame.display.flip()