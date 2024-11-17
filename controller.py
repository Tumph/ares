#Master controller for the game, handles the flow of the game and the user's actions.

from plotplanner import generate_daily_plot, generate_weekly_plot, generate_yearly_plot
import game_state

def update_plots():
    if game_state.plotsignal:
        game_state.current_day_plot = generate_daily_plot(game_state.sols)
        game_state.plotsignal = False
    if game_state.week_signal:
        game_state.current_week_plot = generate_weekly_plot(game_state.sols)
        game_state.week_signal = False

def initialize_plots():
    game_state.current_day_plot = generate_daily_plot(game_state.sols)
    game_state.current_week_plot = generate_weekly_plot(game_state.sols)
    game_state.current_year_plot = generate_yearly_plot()

def day_win_check():
    from solver import day_problem_solver
    return day_problem_solver()["win_loss"]

def week_win_check():
    from solver import week_problem_solver
    return week_problem_solver()["win_loss"]