import pygame
import math
from utils import system, vec2

class Cart:
    def __init__(self, screen, mass, width, height, cart_x, environment):
        self.mass = mass
        self.screen = screen
        self.width = width
        self.height = height
        self.x = cart_x
        self.vx = 0
        self.accx = 0
        self.pendulum: Pendulum = None
        self.environment:system = environment
        
    def accelerate(self, force):
        # Calculate acceleration based on force and gravity
        acceleration = (force/ self.mass)
        self.accx = max(-self.environment.MAX_ACCELERATION, min(self.environment.MAX_ACCELERATION, acceleration))
    
        
    def step(self, dt):
        oldvx = self.vx
        vx = self.vx +  (self.accx - (self.environment.LATERAL_FRICTION_CONSTANT * self.vx) )*dt
        self.vx = max(-self.environment.CART_MAX_SPEED, min(self.environment.CART_MAX_SPEED, vx))
        accx = (self.vx - oldvx) / dt
        pendulum_force = vec2(-self.pendulum.mass * accx, -self.pendulum.mass * self.environment.GRAVITY)
        
        # self.vx -= * dt
        self.x += self.vx * dt
        
        self.accx = 0
        self.pendulum.update(dt, pendulum_force)
    
    def draw(self):
        cart_rect = pygame.Rect((self.x - self.width/ 2.0)*self.environment.magnification, (self.environment.cart_y - self.height/2)*self.environment.magnification, self.width*self.environment.magnification, self.height*self.environment.magnification)
        pygame.draw.rect(self.screen, (0, 0, 255), cart_rect)
    
        
    def getState(self):
        return self.x, self.y, self.vx

class Pendulum:
    def __init__(self, screen, cart, length, mass, angle, environment):
        self.screen = screen
        self.cart = cart
        self.length = length
        self.angle = angle
        self.mass = mass
        self.MOI_inv = 1.0 / (mass * length * length)
        self.angular_velocity = 0
        self.environment:system = environment
        

    def update(self, dt, force: vec2):
        torque = (-force.x * self.length * math.sin(self.angle) +
                  force.y * self.length * math.cos(self.angle)) -  self.environment.SWING_FRICTION_CONSTANT * self.angular_velocity
        angular_acceleration = torque * self.MOI_inv
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.angle = self.angle % (2 * math.pi) 
        
        pass
    
    def draw(self):
        pivot_x = self.cart.x
        pivot_y = self.environment.cart_y
        pendulum_x = pivot_x + self.length * math.cos(self.angle)
        pendulum_y = pivot_y - self.length * math.sin(self.angle)

        pygame.draw.line(self.screen, (255, 255, 255), (pivot_x*self.environment.magnification, pivot_y*self.environment.magnification), (pendulum_x*self.environment.magnification, pendulum_y*self.environment.magnification), math.ceil(self.environment.PENDULUM_THICKNESS*self.environment.magnification))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(pendulum_x*self.environment.magnification), int(pendulum_y*self.environment.magnification)), math.ceil(self.environment.PENDULUM_BOB_RADIUS*self.environment.magnification))
