# Match Point AI
Match Point AI is a Novel AI Framework for evaluating data-driven Tennis strategies. 

# Project Structure
## Files for the Bots and Agents:
- mcts_agent.py (UCT selection Policy)
- mcts_greedy_agent.py (Greedy Selection Policy)
- mcts_random_agent.py (Random Selection Policy)
- average_stat_bot.py (fixed strategy Bot resembling Average Behavior from real-world data)
- simpler_stat_bot_djoko (fixed strategy Bot resembling Djokovic Behavior from real-world data)
- bot.py (currently not working and not important)

## UI Stuff and Architecture:
- rally.py (contains the rally object class)
- scoring.py (handles the scoring)
- constants.py (contains the constants and variables)
- ball.py (Ball Object for Visualization)
- button.py (Button Object for Visualization)
- rally_tree.py (MCTS Tree of the Tennis Game)
- log.py (Keeps track of the data if enables in the menu)

## Most important:
- test_menu.py (Menu for setting the Simulation Matches)
- main_loop.py (Simulates the matches)

# Using Match Point AI:
Clone the prjoject from GitHub and install the requirements from requirements.txt
Then you can start run the file test_menu.py which will open the Menu to set up an experiment.

