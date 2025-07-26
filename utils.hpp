#pragma once
#include <cmath>
#include "constants.hpp"


#define SQR(x) ((x) * (x))
#define CLAMP(x, low, high) ((x) < (low) ? (low) : ((x) > (high) ? (high) : (x)))



struct vec2 {
    float x;
    float y;

    vec2 operator+(const vec2& other) const {
        return {x + other.x, y + other.y};
    }

    vec2 operator-(const vec2& other) const {
        return {x - other.x, y - other.y};
    }

    vec2 operator*(float scalar) const {
        return {x * scalar, y * scalar};
    }
    friend vec2 operator*(float scalar, const vec2& v) {
        return {v.x * scalar, v.y * scalar};
    }

    vec2 operator/(float scalar) const {
        return {x / scalar, y / scalar};
    }

};