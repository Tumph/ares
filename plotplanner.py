#This microservice will handle the generation of the plot for the game.

from llm import get_openai_response
import random
from dotenv import load_dotenv
import game_state

load_dotenv()


weekly_plot = ""
yearly_plot = ""
issue = ""

def issue_generator():
    random_number = random.random()*10
    if random_number > 8:
        return f"However today, an issue happens to {game_state.astronaut_name}."
    else:
        return f"Today, nothing happens to {game_state.astronaut_name}."
    
day_commands_str = ", ".join(game_state.day_commands_array)
week_commands_str = ", ".join(game_state.week_commands_array)

# Game context to be used for generating plot points
daily_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that generates plot points for a game.",
    f"The game goes like this: the user is the commander of the ares mission, and {game_state.astronaut_name} has been left behind on mars.",
    f"The user must communicate with {game_state.astronaut_name} to try and keep him alive long enough for the rescue mission to arrive in 365 sols.",
    f"You are generating the plot points for the game, and the user is the one interacting with {game_state.astronaut_name}.",
    "You are given a sol number and a status update. You must generate a plot point for that sol.",
    "You must respond in a json format with the following keys: sol, plot_point",
    "Your plot point should be exactly three sentences that describe the challenges that the player must face in that sol.",
    f"However, keep in mind that most days are boring, and nothing happens to {game_state.astronaut_name}. {issue}",
    f"You must keep in mind the plot generated for the week ahead of you when determining the plot point for the current sol.",
    f"Here is the plot for the week ahead: {weekly_plot}",
    f"Also, here is the messages between the user and {game_state.astronaut_name} for the previous sol to continue building the plot: {day_commands_str}",
    f"You are currently on sol {game_state.sols} and must generate a plot point.",
    ])}
]

weekly_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that generates plot points for a game.",
    f"The game goes like this: the user is the commander of the ares mission, and {game_state.astronaut_name} has been left behind on mars.",
    f"The user must communicate with {game_state.astronaut_name} to try and keep him alive long enough for the rescue mission to arrive in 365 sols.",
    f"You are generating the plot points for the game, and the user is the one interacting with {game_state.astronaut_name}.",
    "You are given a start sol, an end sol and a status update. You must generate a plot point for that period of sols.",
    "You must respond in a json format with the following keys: start_sol, end_sol, plot_point", 
    "Your plot point should be exactly seven sentences that describe the challenges that the player must face in that period of sols.",
    f"You must keep in mind the plot generated for the year ahead of you when determining the plot point for the current period of sols.",
    f"Here is the plot for the year ahead: {yearly_plot}",
    f"Also, here is the messages between the user and {game_state.astronaut_name} for the previous week to continue building the plot: {week_commands_str}",
    f"You are currently on sol {game_state.sols} and the end sol for your generated plot point is at your discretion, but include it in your json response.",
    ])}
]

yearly_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that generates plot points for a game.",
    f"The game goes like this: the user is the commander of the ares mission, and {game_state.astronaut_name} has been left behind on mars.",
    f"The user must communicate with {game_state.astronaut_name} to try and keep him alive long enough for the rescue mission to arrive in 365 sols.",
    f"You are generating the plot points for the game, and the user is the one interacting with {game_state.astronaut_name}.",
    "You must respond in a json format with one key: plot_point", 
    "Your plot point should be exactly 30 sentences that describe the challenges that the player must face in that year.",
    "Be inspired by various survival movies and books to come up with the plot points for the year, such as hatchet or the martian.",
    "Example events: hab depressurization, power outages, solar storms, asteroid impact, rover breakdown, crop failure, etc.",
    "Example issues caused by these events: loss of oxygen, loss of power, loss of water, loss of life support, loss of food, etc.",
    ])}
]


# Function to generate a single day's plot point
def generate_daily_plot(sol):
    question = f"Generate a plot point for Sol {sol}. What challenge or challenges does {game_state.astronaut_name} face? What happens?"
    return get_openai_response(daily_context, question)

# Function to generate a week's worth of plot points (7 days)
def generate_weekly_plot(sol):
    question = f"Generate a plot point for the week starting on Sol {sol} and ending on Sol {sol + 6}. What challenges does {game_state.astronaut_name} face? What happens?"
    return get_openai_response(weekly_context, question)

# Function to generate an entire year's plot points (365 days)
def generate_yearly_plot():
    question = f"Generate a plot point for the year. What challenges does {game_state.astronaut_name} face? What happens?"
    return get_openai_response(yearly_context, question)
