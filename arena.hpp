#pragma once
#include <SFML/Graphics.hpp>
#include "constants.hpp"  
#include "pendulum.hpp"
#include "utils.hpp"
#include "cart.hpp"



struct State{
    float cpos;
    float cvel;
    float pangle;
    float pomega;
};
struct Action{
    float force;
};

struct Arena
{
    float width;
    float height;
    float screen_width;
    float screen_height;
    float gravity;
    float origin_x = 0.0f;
    float origin_y = 0.0f;
    Cart cart;
    sf::RectangleShape cart_shape;
    sf::CircleShape pendulum_shape;
    sf::Vertex pendulum_rod[2] = {
        sf::Vertex(sf::Vector2f(0, 0), sf::Color::Red),
        sf::Vertex(sf::Vector2f(0, 0), sf::Color::Red)
    };

    Arena(float width, float height, float screen_width, float screen_height, float gravity);
    void set_origin(const float x, const float y);
    void set_pendulum(const Pendulum& pendulum);
    void set_cart(const Cart& cart);
    void step(const float dt, const float force);
    State get_state() const;

    void draw(sf::RenderWindow& window);

};
