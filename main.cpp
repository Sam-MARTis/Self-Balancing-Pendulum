#include <SFML/Graphics.hpp>
#include "arena.hpp"
#include "constants.hpp"
#include "pendulum.hpp"
#include "cart.hpp"
#include "utils.hpp"
#include <iostream>
#include <cmath>
#include <cstdlib>



int main(){
    sf::RenderWindow window(sf::VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT), "Inverted Pendulum");
    Arena arena(ARENA_WIDTH, ARENA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY);
    Pendulum pendulum(PENDULUM_LENGTH, PENDULUM_MASS, PI / 4.0f);
    Cart cart((CART_WIDTH*(float)SCREEN_WIDTH)/(ARENA_WIDTH), CART_MAX_SPEED, CART_MAX_ACCELERATION, 0.0f, 0.0f, 0.0f, 1.0f, pendulum);
    arena.set_cart(cart);
    arena.set_pendulum(pendulum);
    arena.set_origin(ARENA_WIDTH / 2.0f, ARENA_HEIGHT/3.0f);
    window.setFramerateLimit(60);
    float force = 0.0f;
    while(window.isOpen()){
        sf::Event event;
        while(window.pollEvent(event)){
            if(event.type == sf::Event::Closed){
                window.close();
            }
            if(event.type == sf::Event::KeyPressed){
                if(event.key.code == sf::Keyboard::Left){
                    force = -FORCE_CONSTANT; // Apply force to the left
                } else if(event.key.code == sf::Keyboard::Right){
                    force = FORCE_CONSTANT; // Apply force to the right
                }

                // Release force when no key is pressed
            } else if(event.type == sf::Event::KeyReleased){
                if(event.key.code == sf::Keyboard::Left || event.key.code == sf::Keyboard::Right){
                    force = 0.0f; // Stop applying force
                }
            }
        }
        
        window.clear(sf::Color::Black);
        
        // Simulate the pendulum and cart
        arena.step(1.0f / 60.0f, force);
        
        // Draw the arena, cart, and pendulum
        arena.draw(window);
        // force = 0.0f;
        
        window.display();
    }
    return 0;

}