import pygame
import math
import sys

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum on Cart")
clock = pygame.time.Clock()


cart_width = 0.5
cart_height = 0.2
pendulum_length = 0.5
pendulum_angle = math.radians(30)

ARENA_WIDTH = 3
magnification = WIDTH / ARENA_WIDTH

cart_x = ARENA_WIDTH/2
cart_y =  HEIGHT / (2 * magnification)
cart_max_speed = 0.1
SWING_FRICTION_CONSTANT = 0.1
# Main Loop

"""


void Cart::accelerate(const float force, const float gravity = GRAVITY)
{
    // const float acceleration = (force - aPend.mass * gravity * sin(aPend.angle) * cos(aPend.angle)) / (mass + aPend.mass * SQR(cos(aPend.angle)));
    const float acceleration = (force/mass)  - LATERAL_FRICTION_CONSTANT*velocity;
    this->acceleration = CLAMP(acceleration, -max_acceleration, max_acceleration);
}
void Cart::step(const float dt, const float force, const float gravity = GRAVITY)
{
    accelerate(force, gravity);
    velocity += (acceleration) * dt ;
    velocity = CLAMP(velocity, -max_speed, max_speed);
    position += velocity * dt;
    const vec2 pendForce = {-aPend.mass * acceleration, -aPend.mass * gravity};
    aPend.step(dt, pendForce);
}

void Pendulum::step(float dt, vec2 force)
{
    const float torque = ((-force.x * length * sin(angle)) +
                         (force.y * length * cos(angle))) - SWING_FRICTION_CONSTANT * angular_velocity;
    const float angular_acceleration = torque * MOI_inv;
    angular_velocity += angular_acceleration * dt;
    angle += angular_velocity * dt;
}


"""

MAX_ACCELERATION = 40


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
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = cart_x
        self.vx = 0
        self.accx = 0
        self.pendulum: Pendulum = None
        
    def accelerate(self, force, gravity=9.81):
        # Calculate acceleration based on force and gravity
        acceleration = (force / self.width) - SWING_FRICTION_CONSTANT * self.vx
        self.accx = max(-MAX_ACCELERATION, min(MAX_ACCELERATION, acceleration))
    
        
    def step(self, dt):
        self.vx += self.accx * dt
        # self.vx = max(-cart_max_speed, min(cart_max_speed, self.vx))
        self.x += self.vx * dt
        pendulum_force = vec2(-self.pendulum.mass * self.accx, -self.pendulum.mass * 9.81)
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

        pygame.draw.line(self.screen, (255, 255, 255), (pivot_x*magnification, pivot_y*magnification), (pendulum_x*magnification, pendulum_y*magnification), 10)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(pendulum_x*magnification), int(pendulum_y*magnification)), 12)
    

if __name__ == "__main__":
    cart = Cart(screen, cart_width, cart_height)
    pendulum = Pendulum(screen, cart, pendulum_length, 1.0, pendulum_angle)
    cart.pendulum = pendulum

    # Main loop
    clock = pygame.time.Clock()
    cart_speed = 5
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
            force = -cart_speed
        elif keys[pygame.K_RIGHT]:
            force = cart_speed

        cart.accelerate(force)
        dt = clock.tick(60)/1000
        cart.step(dt)

        # screen.fill((255, 255, 255))
        cart.draw()
        pendulum.draw()
        
        pygame.display.flip()