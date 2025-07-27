import math

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
    
class Helpers:
    @staticmethod
    def radians(degrees):
        return degrees * (math.pi / 180.0)

    @staticmethod
    def degrees(radians):
        return radians * (180.0 / math.pi)
    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    @staticmethod
    def lerp(start, end, t):
        return start + (end - start) * t
    @staticmethod
    def randint(min_value, max_value):
        return int(min_value + (max_value - min_value) * math.random())
    @staticmethod
    def rand(min_value, max_value):
        return min_value + (max_value - min_value) * math.random()
    
    
# HEIGHT, WIDTH = 600, 800
# ARENA_WIDTH = 3
# CART_WIDTH = 0.3
# CART_HEIGHT = 0.1
# CART_MASS = 1.0
# PENDULUM_LENGTH = 0.3

# PENDULUM_MASS = 1.0
# PENDULUM_THICKNESS = 0.02
# PENDULUM_BOB_RADIUS = 0.03



# CART_MAX_SPEED = 5
# MAX_ACCELERATION = 40
# CART_BUTTON_FORCE = 8
# SWING_FRICTION_CONSTANT = 0.1
# GRAVITY = 9.81
# LATERAL_FRICTION_CONSTANT = 0.1


# # pendulum_angle = math.radians(30)
# magnification = WIDTH / ARENA_WIDTH
# cart_x = ARENA_WIDTH/2
# cart_y =  HEIGHT / (2 * magnification)


class system:
    def __init__(self,dt, width, height, arena_width, cart_mass, cart_width, cart_height, pendulum_length, pendulum_mass, pendulum_thickness, pendulum_bob_radius, cart_max_speed, max_acceleration, swing_friction_constant, gravity, lateral_friction_constant):
        self.dt = dt
        self.WIDTH = width
        self.HEIGHT = height
        self.CART_MASS = cart_mass
        self.ARENA_WIDTH = arena_width
        self.CART_WIDTH = cart_width
        self.CART_HEIGHT = cart_height
        self.PENDULUM_LENGTH = pendulum_length
        self.PENDULUM_MASS = pendulum_mass
        self.PENDULUM_THICKNESS = pendulum_thickness
        self.PENDULUM_BOB_RADIUS = pendulum_bob_radius
        self.CART_MAX_SPEED = cart_max_speed
        self.MAX_ACCELERATION = max_acceleration
        # self.CART_BUTTON_FORCE = CART_BUTTON_FORCE
        self.SWING_FRICTION_CONSTANT = swing_friction_constant
        self.GRAVITY = gravity
        self.LATERAL_FRICTION_CONSTANT = lateral_friction_constant
        self.magnification = self.WIDTH / self.ARENA_WIDTH
        self.cart_y = self.HEIGHT / (2 * self.magnification)