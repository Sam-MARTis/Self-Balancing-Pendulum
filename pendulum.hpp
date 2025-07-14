#pragma once
#include "utils.hpp"


struct Pendulum{
    float length;
    float mass;
    float angle; 
    float angular_velocity;
    float MOI_inv;

    Pendulum(float length=0, float mass=0, float angle=0);
    void step(float dt, vec2 force);
};