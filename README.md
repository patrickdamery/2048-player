Title: 2048 AI Player.
Description: AI utilizes Mini max algorithm with alpha-beta pruning to explore the most revelant search space based on predefined heuristics. Heuristic weights were selected by Bayesian Optimization function.

To run download the repository and unpack it, navigate to the directory in the command line and type:
python GameManager.py

That will begin a new game and will allow visualization of the game as it's being played.

They bayesian optimization script that I used to find weights can be found in bayesian.py, in order to be used PlayerAI must be modified:
  Lines 29 and 31-40 must be uncommented.
  Lines 30 and 41-48 must be commented.

After making these changes you can run: python bayesian.py

An example of the output of bayesian.py can be found in bayesianresults.txt
