#pragma once
#include "pendulum.hpp"

struct Cart
{
    float width;
    float max_speed;
    float max_acceleration;
    float position;
    float velocity;
    float acceleration;
    float mass;
    Pendulum aPend;
    // Constructor with default values
    Cart(float width = 0, float max_speed = 0, float max_acceleration = 0, float position = 0, float velocity = 0, float acceleration = 0, float mass = 0, Pendulum aPend = Pendulum())
        : width(width), max_speed(max_speed), max_acceleration(max_acceleration), position(position), velocity(velocity), acceleration(acceleration), mass(mass), aPend(aPend) {}
    // Cart(float width, float max_speed, float max_acceleration, float position, float velocity, float acceleration, float mass, Pendulum aPend)
    //     : width(width), max_speed(max_speed), max_acceleration(max_acceleration), position(position), velocity(velocity), acceleration(acceleration), mass(mass), aPend(aPend) {}
    void accelerate(const float force, const float gravity);
    void step(const float dt, const float force, const float gravity);
};