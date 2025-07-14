#include <cmath>
#include "pendulum.hpp"
#include "utils.hpp"
#include "cart.hpp"


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
