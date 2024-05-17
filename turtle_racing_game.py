# Game In python 
# Racing Turtle Game
import random

import colorgram
from turtle import Turtle, Screen

color = ["red", "orange", "blue", "green", "purple"]
y_position = [0, 50, 100, -50, -100]
all_turtle = []
is_race_start = False
screen = Screen()
screen.setup(width=500, height=400)
userinput = screen.textinput(title="Make Your Bet", prompt="Which turtle will win the race? Enter Color")
screen.colormode(255)
for t_index in range(0, 5):
    t = Turtle(shape="turtle")
    t.penup()
    t.color(color[t_index])
    t.goto(x=-230, y=y_position[t_index])
    all_turtle.append(t)

if userinput:
    is_race_start = True
while is_race_start:
    for turtle in all_turtle:
        if turtle.xcor() > 230:
            is_race_start = False
            if userinput == turtle.pencolor():
                print(f"You've Win winner is {turtle.pencolor()} turtle")
            else:
                print(f"You Loss winner is {turtle.pencolor()} turtle")

        turtle.forward(random.randint(0, 10))


screen.exitonclick()
