# grimdark-clock
A chess style clock for many players

## Installation

Make sure you have python 3.4 or later.

In your terminal type:

    pipenv shell
    pipenv install -r .\requirements.txt

This should install jproperties and six.

## Running the clock

Type:

    python grimdark-clock.py

Upon the first run of the program, it will ask for a list of names for the players:

    Name of players, separate with space: 

Type in the names. It will be saved in a properties-file in the same directory. You can edit this file.
The next time you run the program, it will find the properties-file and use it as default. Then you can just
press Enter to accept the default.

Next it will ask how many minutes each player starts with:

    How many minutes do each player start with:

Now you should find a window for the program. It should have one row for each player. Each timer should be
initialized to the value you selected.

Using the up and down buttons on each row, you can organize the players in the correct order. 

Press the Play-button to start the timer.

When the first player is done, use the Next-button. Now, time will start to tick down for the next player.

A player can signal that they are done for the round by clicking Done. They will be skipped. When only one 
player remains, the Next-button stops working. That player simply finishes his remaining moves and after 
that the clock can be paused to calculate scores etc. If the last player clicks Done, it is the same as Pause. 
Pressing Pause also clears all Done states.

## Keyboard shortcuts

Press SPACE to switch to the next player.

Press 'p' to pause the clock.

Press 'd' to mark the current player as done for the round. He will be skipped until the clock is paused.

Maybe you can configure your computer to do this with voice control?

## Changing GUI scale

The labels and buttons can be scaled up and down to maximize visibility.
Use the keys + and - (minus or dash or hyphen).
