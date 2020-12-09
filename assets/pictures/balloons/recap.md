Current status: trying to find the best algorithm for optimal play at…
"ballons", the favorite game of my 3yo.

It's a game mostly based on luck; each player is dealt a hand of 5 balloons. There are 25 balloon cards, and 5 different colors.
Then, you pick action cards in turns. They can be:
 - either burst a balloon (20 cards/25)
 - either recover a balloon of your choice (5 cards/25)

Game is lost when you run out of balloons.

There's only one action possible, which is to carefully choose which balloon to recover.

The question at first is: "what is the baseline I'm fighting against": my kids play randomly, so:
 - if I play randomly what are my odds of winning, depending
 - is there a way to improve the play ?

I wrote a few tools in rust and python, so far I have a few things

 - the distribution of the length of the game (I ran a monte carlo simulation of a few hundreds of thousands of games, and plotted the game length)
 - the game hands (only 7 different kinds when you remove all the symetries) along with their probability of encounter from a fair deck
 - all the possible hand encounters
 - an accurate model of the probabilities of victory (again, a bruteforce montecarlo simulation, written in 3 different ways)

I wrote 3 models for the last part.
First, I randomly picked 2 hands, ran a game to compute the winner: it works well for the frequent encounters, but I did not have enough data for the least frequent hands because they did not occur often enough.

Then, I generated all possible hands you can draw (only about 250 when you remove the symmetries)

With this, I mapped all the possible encounters, then ran again the monte carlo simulation with a fixed number of iterations per encounter.

First in python, but 100000 iterations per encounters took about 5 minutes
…so I rewrote it partly in rust.
The results were similar, but it was about 10x faster.

I could win a bit more in many ways, first by using rayon, but that's not the point for now.

I could run less iterations by using a better monte carlo stopping condition

