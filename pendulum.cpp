#include "utils.hpp"
#include "constants.hpp"
#include <cmath>
#include "pendulum.hpp"


Pendulum::Pendulum(float length, float mass, float angle)
    : length(length), mass(mass), angle(angle), angular_velocity(0.0f)
{
    MOI_inv = 1.0f / (mass * length * length);
}

void Pendulum::step(float dt, vec2 force)
{
    const float torque = ((-force.x * length * sin(angle)) +
                         (force.y * length * cos(angle))) - SWING_FRICTION_CONSTANT * angular_velocity;
    const float angular_acceleration = torque * MOI_inv;
    angular_velocity += angular_acceleration * dt;
    angle += angular_velocity * dt;
}