from dotenv import load_dotenv
import streamlit as st
import time
from flask import Flask, request
from llm import get_openai_response
import game_state   
from controller import update_plots, initialize_plots, day_win_check, week_win_check
import random
from deathmessage import day_death_message, week_death_message
import numpy as np
from PIL import Image
from astronaut import context

# Load
load_dotenv()
app = Flask(__name__)
# Streamlit page setup
st.set_page_config(page_title="Ares Mission - Mars Communications", layout="centered")


def create_pixel_map(size=(20, 20)):
    """Create a basic pixel map with the Hab location"""
    # Create empty map (black background)
    map_array = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    
    # Set Hab location (center, marked in red)
    center = (size[0]//2, size[1]//2)
    map_array[center[0], center[1]] = [255, 0, 0]  # Red pixel for Hab
    
    return map_array

def initialize_app():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.communication_log = [
            {
                "commander": "Initializing Ares mission communication link...",
                "{game_state.astronaut_name}": "Hello, can you read?"
            }
        ]
        st.session_state.commandnum = random.randint(3, 6)
        st.session_state.pixel_map = create_pixel_map()
        initialize_plots()

# Move message handling into a separate function
def handle_new_message(command):
    # Create a temporary copy of the current log
    current_log = st.session_state.communication_log.copy()
    
    # Add the commander's message and force a rerun
    current_log.append({"commander": command, "{game_state.astronaut_name}": None})
    st.session_state.communication_log = current_log
    
    
    with st.spinner("Data transmission to Mars... please wait for response"):
        time.sleep(4)
    response = get_openai_response(context, command)
    with st.spinner("Data transmission to Earth... please wait for response"):
        time.sleep(4)

    # Update with {game_state.astronaut_name}'s response and force another rerun
    current_log[-1]["{game_state.astronaut_name}"] = response
    st.session_state.communication_log = current_log
    game_state.day_commands_array.append(command)
    game_state.week_commands_array.append(command)
    st.session_state.commandnum -= 1

    if st.session_state.commandnum == 0:
        handle_end_of_sol(command)
    st.rerun()

def show_game_over(type, command):
    if type == "day":
        death_message = day_death_message()["death_message"]
    else:
        death_message = week_death_message()["death_message"]
    st.session_state.communication_log.append(
        {"commander": command, "{game_state.astronaut_name}": death_message}
    )
    st.markdown(
        """
        <div style='text-align: center; padding: 50px;'>
            <h1 style='color: red; font-size: 72px;'>GAME OVER</h1>
            <h2 style='color: white;'>Reload the page to play again</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

def handle_end_of_sol(command):
    st.session_state.commandnum = random.randint(3, 6)
    game_state.sols += 1
    game_state.plotsignal = True

    if game_state.weekcounter + 6 < game_state.sols:
        game_state.weekcounter = game_state.sols
        handle_end_of_week(command)

    if not day_win_check():
        show_game_over("day", command)

    update_plots()
    game_state.day_commands_array = []
    

def handle_end_of_week(command):
    game_state.week_signal = True

    if not week_win_check():
        show_game_over("week", command)

    update_plots()
    game_state.week_commands_array = []

def main():
    initialize_app()
    
    st.markdown("""
        <style>
        /* Global styles */
        .stApp, .stMarkdown, .stText, p, div, h1, h2, h3, h4, h5, h6, .sidebar-header h3, .mission-stat {
            color: #000000 !important;
        }
        
        .stApp { background-color: #f5f5f5; }
        [data-testid="stSidebar"] { background-color: #ffffff !important; }
        
        /* Message styling */
        .message-content {
            background-color: #ffffff;
            padding: 15px;
            border: 1px solid #cccccc;
            margin-top: 5px;
        }
        
        .timestamp {
            font-size: 12px;
            font-family: monospace;
        }
        
        /* Button styling */
        .stForm [data-testid="stFormSubmitButton"] button {
            background-color: #198754 !important;
            color: #ffffff !important;
            border: 1px solid #198754 !important;
            border-radius: 3px !important;
        }
        
        .stForm [data-testid="stFormSubmitButton"] button:hover,
        .stForm [data-testid="stFormSubmitButton"] button:active,
        .stForm [data-testid="stFormSubmitButton"] button:focus {
            background-color: #146c43 !important;
            border: 1px solid #146c43 !important;
            outline: none !important;
        }
        
        .stTextArea textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add Font Awesome for the search icon
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

    # Remove sidebar checkbox and directly use sidebar
    with st.sidebar:
        st.markdown("<div class='sidebar-header'><h3>Mission Status</h3></div>", unsafe_allow_html=True)
        
        st.markdown("""
            This sidebar displays critical mission information including remaining 
            resources and time elapsed on Mars. Monitor these values carefully 
            as they directly impact mission survival.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display mission stats
        st.markdown(f"""
            <div class='mission-stat'>
                <span class='stat-label'>Sols on Mars:</span> {game_state.sols}
            </div>
            <div class='mission-stat'>
                <span class='stat-label'>Food Supply:</span> {game_state.food} days
            </div>
            <div class='mission-stat'>
                <span class='stat-label'>Water Supply:</span> {game_state.water} L
            </div>
            <div class='mission-stat'>
                <span class='stat-label'>Oxygen Supply:</span> {game_state.oxygen} days
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='playbook-header'><h2>Mission Control Playbook</h2></div>", unsafe_allow_html=True)
    st.markdown(f"Sol #{game_state.sols} - Remaining transmissions: {st.session_state.commandnum}")

    # Display messages in chronological order
    for entry in st.session_state.communication_log:
        # Commander's message
        st.markdown(f"""
            <div class='message-container'>
                <div style='display: flex; align-items: start;'>
                    <div class='role-icon' style='background-color: #dc3545;'></div>
                    <div style='flex-grow: 1;'>
                        <div class='timestamp'>CDR</div>
                        <div class='message-content'>{entry['commander']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # {game_state.astronaut_name}'s response
        if entry['{game_state.astronaut_name}'] is not None:
            st.markdown(f"""
                <div class='message-container'>
                    <div style='display: flex; align-items: start;'>
                        <div class='role-icon' style='background-color: #198754;'></div>
                        <div style='flex-grow: 1;'>
                            <div class='timestamp'>MCC</div>
                            <div class='message-content'>{entry['{game_state.astronaut_name}']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Update the message input form
    with st.form(key="command_input", clear_on_submit=True):
        st.text_area(f"Communication Protocol: Mission Control to {game_state.astronaut_name}", 
                    key="command_text", 
                    height=100,
                    on_change=None,
                    kwargs=dict(on_key="enter"))
        cols = st.columns([1, 5])
        with cols[0]:
            st.checkbox("High Priority!")
        with cols[1]:
            submit = st.form_submit_button("Send")

    if submit and st.session_state.command_text:
        handle_new_message(st.session_state.command_text)


if __name__ == "__main__":
    main()
 