#This microservice will handle the death message for the game.

from llm import get_openai_response
import game_state

day_commands_str = ", ".join(game_state.day_commands_array)
week_commands_str = ", ".join(game_state.week_commands_array)

day_death_message_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that generates a death message for the game.",
           "You are given the plot point for the current sol, and the user's commands.",
           "You must generate a death message for the user based on the plot point and the user's commands.",
           "You must respond with a json format with the following keys: death_message",
           "Your death message should be exactly three sentences that describe the circumstances of the user's death.",
           "The plot point for the current sol is: {game_state.current_day_plot}",
           "And for context, the user has been on the mission for {game_state.sols} sols.",
           "The user's commands for the whole sol are: {day_commands_str}",
    ])}
]


week_death_message_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that generates a death message for the game.",
           "You are given the plot point for the current week, and the user's commands.",
           "You must generate a death message for the user based on the plot point and the user's commands.",
           "You must respond with a json format with the following keys: death_message",
           "Your death message should be exactly three sentences that describe the circumstances of the user's death.",
           "The plot point for the current week is: {game_state.current_week_plot}",
           "And for context, the user has been on the mission for {game_state.sols} sols.",
           "The user's commands for the whole week are: {week_commands_str}",
    ])}
]

def day_death_message():
    return get_openai_response(day_death_message_context, "You need to respond in a json format with the following keys: death_message")

def week_death_message():
    return get_openai_response(week_death_message_context, "You need to respond in a json format with the following keys: death_message")