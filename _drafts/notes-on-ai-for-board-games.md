---
title: Notes on AI for board games, card games and puzzles.
layout: post
lang: en
image: balloons.png
---

Some notes on «AI» for board games, card games and puzzles.

First, lets clarify a thing : «AI» is a very ill-defined term. In this article I will use it as « a way to make the computer play good moves in games ». 

Many models of AI in board games involve a search in a tree. In the case of a 2-player card game, the goal of the AI is to find optimal play by traversing the tree in some way. As for puzzles, the goal is to find a solution. The problem is a bit different, but they share a non real-time approach.

Depending on the structure of the tree (depth, branching factor), there are many ways to make an AI for a card or board games :

 - brute forcing a solution.
 - hand-rolling the rules for the AI.
 - minmax and variants (alpha-beta, MTD(f))
 - Monte Carlo methods, along with Monte Carlo Tree Search.
 - Deeplearning

# Brute force

This solution is often easy to implement, but very slow when the search tree is large. In order to find a solution in a reasonnable time, you most likely will need to use another solution from later in this article.

That being said, brute force has its place in games, for instance as a [database of endgames](https://en.wikipedia.org/wiki/Endgame_tablebase). This is used in ["traditionnal" chess AIs](https://www.chessprogramming.org/Endgame_Tablebases). A popular table is called [Syzygy](https://github.com/syzygy1/tb)

# Hand-rolled heuristic

In the case of the [tic-tac-toe](https://xkcd.com/832/) where the tree is small, that’s possible.

https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

This is also very frequently used in real-time games, such as FPSes.

# Minmax and variants

Many complex games can be solved using minmax/negamax, [alphabeta-pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) or [MTD(f)](https://en.wikipedia.org/wiki/MTD-f). Speedup can be obtained through [transposition tables](https://en.wikipedia.org/wiki/Transposition_table) (basically, memoization: cache for previously seen positions)

Here is a nice article on building a chess engine:

 - [https://healeycodes.com/building-my-own-chess-engine/](https://healeycodes.com/building-my-own-chess-engine/). [Sunfish](https://github.com/thomasahle/sunfish/blob/master/sunfish.py) is also both a short and detailled python implementation of a good chess engine.

It is more detailled [here in the context of solving connect-4](http://blog.gamesolver.org/solving-connect-four/01-introduction/)

It can also be applied to [complex card games](https://news.ycombinator.com/item?id=25525554) : 

 > A lot of the same tools as chess engine development apply: alpha-beta and the myriad variant search algorithms like MTD(f), transposition tables, heuristics like the [killer move heuristic](https://www.chessprogramming.org/Killer_Heuristic) or the [countermove heuristic](https://www.chessprogramming.org/Countermove_Heuristic). But you also need to apply some domain specific heuristics and tools, and since the whole thing is performance critical you need to worry about low level optimizations and good multithreading. In the bridge case it's not at all trivial to get something that can even finish at all in a reasonable timespan.

# Monte Carlo methods

Many games involves are not perfect information games. When it involves probabilities (think Poker), your goal is to find, based on the probabilities of future events what is the best play.

I’ve seen this being used:

- for [can’t stop](https://github.com/norvig/pytudes/blob/master/ipynb/Cant-Stop.ipynb)

# Constraint propagation

Many puzzles like sudoku or [fillomino](https://en.wikipedia.org/wiki/Fillomino) involve constraints on the content of cells. This is often a huge improvement over brute force search, since the search space is strongly reduced.

There are many ways to solve this:

 - Depth first search + constraint propagation. That's what Peter Norvig did for [sudokus](http://norvig.com/sudoku.html). This is particularly efficient here: norvig solves most puzzles in way less than a second.
 - Using a general purpose solver like z3. Tautvidas Sipavičius wrote an article on [solving Puzlogic, a flash puzzle game](https://www.tautvidas.com/blog/2019/02/solving-a-puzzle-game-with-z3-theorem-prover/) like this. (bonus: he also wrote articles on [using computer vision in order to automate solving puzzles](https://www.tautvidas.com/blog/2018/11/adding-basic-vision-part-2-of-solving-puzlogic-with-python-and-opencv/)). That's probaly way slower, but can be a quick way to solve a complex problem

# Monte Carlo Tree Search (MCTS)

MCTS is often the go-to method for algorithmic solving. It can be used to find solutions in complex games with a large branching factor like [Kingdomino](https://zayenz.se/blog/post/kingdomino-cig2018-paper/).

# Deep learning

Computer have long been way better than humans at chess, but deeplearning has provided even better AIs through an improvement over reinforcement learning.

 - for chess, the insights feel more human-like (even though it can anticipate moves that are waaaay deeper than human can). The initial implementation was deepmind, but [Lilachess zero/lc0](https://github.com/LeelaChessZero/lc0/wiki) is an open source implementation.
 - [AlphaGo](https://deepmind.com/blog/article/alphago-zero-starting-scratch) beat human in Go, which was not possible through algorithmic solving due to the size of the search tree.
 - it [solved 6-player no limit hold'em poker](https://science.sciencemag.org/content/365/6456/885.full) in 2019. The issues were different but was not solved before.
