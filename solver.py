#This microservice will take the plot and determine if the user has won or lost.

from llm import get_openai_response
import game_state

day_commands_str = ", ".join(game_state.day_commands_array)
week_commands_str = ", ".join(game_state.week_commands_array)

day_problem_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that determines if the user has won or lost the game.",
           "You are given the plot point for the current sol, and the user's command.",
           "You must determine if the user has won or lost the game based on the plot point and the user's commands.",
           "You must respond with a true or false in a json format with two keys: win_loss and reason",
           "Example: {'win_loss': true, 'reason': 'The hab depressurized, but the user was able to repair it in time.'}",
           "Example: {'win_loss': false, 'reason': 'The hab depressurized, and the user was not wearing his space suit.'}",
           "The plot point for the current sol is: {game_state.current_day_plot}",
           "And for context, the user has been on the mission for {game_state.sols} sols.",
           "The user's commands for the whole sol are: {day_commands_str}",
    ])}
]
week_problem_context = [
    {"role": "system", "content": "\n".join(["You are an AI assistant that determines if the user has won or lost the game.",
           "You are given the plot point for the current week, and the user's command.",
           "You must determine if the user has won or lost the game based on the plot point and the user's command.",
           "You must respond with a true or false in a json format with two keys: win_loss and reason",
           "Example: {'win_loss': true, 'reason': 'The user succeeded in fixing the solar panels, and survived the week.'}",
           "Example: {'win_loss': false, 'reason': 'The user failed to fix the oxygen reclaimer, and oxygen levels dropped to 0.'}",
           "The plot point for the current week is: {game_state.current_week_plot}",
           "And for context, the user has been on the mission for {game_state.sols} sols.",
           "The user's commands for the whole week are: {week_commands_str}",
    ])}
]

def day_problem_solver():
    return get_openai_response(day_problem_context, "You are an AI assistant that determines if the user has won or lost the game. You have been given the plot point for the current sol, and the user's commands for the whole sol. You must determine if the user has won or lost the game based on the plot point and the user's commands. Respond with a true or false in a json format with two keys: win_loss and reason.")

def week_problem_solver():
    return get_openai_response(week_problem_context, "You are an AI assistant that determines if the user has won or lost the game. You have been given the plot point for the current week, and the user's commands for the whole week. You must determine if the user has won or lost the game based on the plot point and the user's commands. Respond with a true or false in a json format with two keys: win_loss and reason.")