#pragma once
#include <functional>
#include <vector>
#include <memory>
#include "constants.hpp"
#include "utils.hpp"
#include "arena.hpp"

struct Neuron{
    int id;
    float value;
    std::function<float(float)> activation_function;
    // Default constructor
    Neuron(int id = 0, float value = 0.0f, std::function<float(float)> activation_function = [](float x) { return x; })
        : id(id), value(value), activation_function(activation_function) {}
};

struct Gene{
    int from_node_id;
    int to_node_id;
    float weight;
    float bias;
    // Default constructor
    Gene(int from_node_id = 0, int to_node_id = 0, float weight = 0.0f, float bias = 0.0f)
        : from_node_id(from_node_id), to_node_id(to_node_id), weight(weight), bias(bias) {}
};

struct Brain{
    int id;
    std::vector<Neuron> neurons;
    std::vector<Gene> genes;

    // Default constructor
    Brain(int id = 0, std::vector<Neuron> neurons = {}, std::vector<Gene> genes = {})
        : id(id), neurons(std::move(neurons)), genes(std::move(genes)) {}
    
    Action perform_computation(const State& state);
    void crossover(const Brain& other);
    void mutate(float mutation_rate, float mutation_strength);

    
    
    
};

