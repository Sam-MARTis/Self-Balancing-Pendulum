SRC = main.cpp \
	  pendulum.cpp\
	  cart.cpp \
	  arena.cpp

OBJ = $(SRC:.cpp=.o)

TARGET = sim

all: $(TARGET)

$(TARGET): $(OBJ) constants.hpp
	g++ -o $@ $^ -lsfml-graphics -lsfml-window -lsfml-system

%.o: %.cpp constants.hpp
	g++ -c $< -o $@ 



clean:
	rm -f $(OBJ) $(TARGET)