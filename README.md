# AAST-AI_Maze_Game

## Description

AI project implementing A* algorithm to find the best path of a maze.
Starting with player 1 solving the maze and trying to solve the optimal path. Then player 2 comes to find a better path than the first player for the optimal solution.
After both are done, now the AI comes over to handle who won! Applying A* on the maze and showing them how to game is played correctly like a boss. And finally, the player who was close to the best optimal path wins!!

## How to play

### Installation

1. First download the repo or clone it.

2. run the command 

```bash
pip install -r requirements.txt 
```
3. Run the file `mainpage`
4. Click `Play 1 VS 1`

### Gameplay

<kbd>↑</kbd> <kbd>↓</kbd> <kbd>→</kbd> <kbd>←</kbd> arrows keys for movement and <kbd>x</kbd> for removing unwanted path.

press <kbd>Enter ↵</kbd> to end your turn and allow the other player to start his journey.

After the players have played the AI will show them what is the best path. Close the window to see who WON!!

### Generating a maze

- Open the file named `developermode.py`
And go to line 225 where `run_id = 4` is located and increase the number by 1 to become `run_id = 5`

- Then to get the map to be detected by the randmoizer Go the the file 'TEST6FORMINUE.PY' in line 223 where `maze_id = random.randint(1, 4)` is located and change it to be `maze_id = random.randint(1, 5)`


Now click on `Generate a Maze (Developer Mode)` in the MainPage
You will be given a window with a small grid. The first click is the Orange start initial point. Then the turquoise square is the end goal point.
Now just draw the walls and barrier you want for your maze. When you are satisfied and finished click on <kbd>C</kbd>.
And that's it :D


## Contributors
- [Amr Mohamed Mamdouh](https://github.com/MAMDOUHjr)
- [Abdallah Ashraf](https://github.com/abdallahashraf120)
- [Amr Ashraf](https://github.com/AmrEL3taaL)
- [Abdulrahman Ahmed](https://github.com/DevAbdoTolba)
- [Mohamed Adel](https://github.com/Dev-Mohamed-Adel)
