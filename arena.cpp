#include <SFML/Graphics.hpp>
#include "constants.hpp"
#include "pendulum.hpp"
#include "utils.hpp"
#include "cart.hpp"
#include "arena.hpp"

Arena::Arena(float width, float height, float screen_width, float screen_height, float gravity)
    : width(width), height(height), screen_width(screen_width), screen_height(screen_height), gravity(gravity) {}

void Arena::set_origin(const float x, const float y) {
    origin_x = x;
    origin_y = y;
}

void Arena::set_pendulum(const Pendulum& pendulum) {
    cart.aPend = pendulum;
    pendulum_shape.setRadius(pendulum.mass * 10.0f);
    pendulum_shape.setFillColor(sf::Color::Red);
    pendulum_shape.setPosition(0, 0);
    pendulum_shape.setOrigin(pendulum_shape.getRadius(), pendulum_shape.getRadius());
}

void Arena::set_cart(const Cart& cart) {
    this->cart = cart;
    cart_shape.setSize(sf::Vector2f(cart.width, cart.width * 0.3f));
    cart_shape.setPosition(0, 0);
    cart_shape.setOrigin(cart.width / 2.0f, cart.width * 0.3f / 2.0f);
    cart_shape.setFillColor(sf::Color::Green);
}

void Arena::step(const float dt, const float force) {
    cart.step(dt, force, gravity);
}

void Arena::draw(sf::RenderWindow& window) {
    float x_mag = screen_width / width;
    float y_mag = screen_height / height;
    float cart_pos = (cart.position + origin_x);
    const vec2 pendulum_end = vec2{
        cart_pos + (cart.aPend.length) * float(cos(cart.aPend.angle)),
        (cart.aPend.length * float(sin(cart.aPend.angle)) + origin_y)
    };
    cart_shape.setPosition(cart_pos * x_mag, (height - origin_y) * y_mag);
    // cart_shape.setPosition((cart_pos - cart.width / 2.0f) * x_mag, (height - origin_y - cart_shape.getSize().y / 2.0f) * y_mag);
    pendulum_shape.setPosition(pendulum_end.x * x_mag, (height - pendulum_end.y) * y_mag);
    pendulum_rod[0].position = sf::Vector2f(cart_pos * x_mag, (height - origin_y) * y_mag);
    pendulum_rod[1].position = sf::Vector2f(pendulum_end.x * x_mag, (height - pendulum_end.y) * y_mag);
    window.draw(cart_shape);
    window.draw(pendulum_shape);
    window.draw(pendulum_rod, 2, sf::Lines);
}

State Arena::get_state() const {
    State state;
    state.cpos = cart.position + origin_x;
    state.cvel = cart.velocity;
    state.pangle = cart.aPend.angle;
    state.pomega = cart.aPend.angular_velocity;
    return state;
}