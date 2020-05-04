---
title: Monte Carlo Tarot Africain
author: Keirua
layout: post
lang: fr
---

Pendant le confinement, on ressort les jeux de cartes et dans mon cas, on a ressorti le tarot africain, un jeu d'annonces avec les atouts d'un jeu de tarot. Un des éléments a attiré mon attention: le site en ligne propose une variante que je ne connaissais pas.

## Le problème

Lors de la dernière carte d'un tour, tout le monde pioche une carte parmi les atouts. Les atouts vont du 1 au 21, et une carte particulière, l'excuse, vaut au choix 0 ou 22. On ne voit que sa propre carte.

Dans quel cas faut-il parier qu'on va avoir la carte de rang le plus élevé ?

![](/assets/pictures/monte-carlo-tarot/tarot-africain-dernier-pli.png)

## L'approche

On va s'en remettre à la puissance de calcul des ordinateurs et les laisser faire le boulot. C'est l'idée de la [méthode de Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method):

 - On simule plein de jeux de cartes, où l'on pioche une carte donnée, et on la compare à celle des autres joueurs.
 - On compte le nombre de fois où on gagne, et on divise par le nombre d'itérations.
 - Grâce à la loi des grands nombres, si on a fait suffisament d'itérations, ce chiffre est notre probabilité de victoire.

Ca a l'air un peu trop simple, mais dans plein de situations, trouver une solution analytique du problème est difficile voir impossible. Dans plein de domaines (finance, biologie, météo ou intelligence artificielle…) les simulations numériques de ce genre sont le mieux qu'on ait.

…ou bien comme ici, quand on est face à un problème de maths niveau terminale, mais que le lycée c'est un peu loin.

## Talk is cheap, show me the code

 - `argparse` pour avoir des paramètres cli
 - `numpy`/`pandas` pour l'export csv
 - `matplotlib` pour générer un graphe

Le coeur de l'algorithme, c'est `compute_card_probability`, qui pour valeur de carte fournie en paramètres, va simuler autant de mains que nécessaire et regarder combien de fois la carte demandée est gagnante.

```python
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# what we want to simulate:
# there are 3 to 5 players
# each player draws a card, whose value is between 0 and 22
# the player with the highest value of all 4 cards wins the hand
# what is the probability to win for each card value ?

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--iterations", type=int, default=1000,
    help="the number of iterations we want to perform")
ap.add_argument("-p", "--players", type=int, default=4,
    choices=[3, 4, 5],
    help="the number of players")
args = vars(ap.parse_args())

nb_players = args["players"]
nb_iterations = args["iterations"]

nb_cards = 22

wins = np.array([0 for i in range(0, nb_cards+1)])

def compute_card_probability(card_value):
    deck = [i for i in range(0, nb_cards+1)]
    deck.remove(card_value)
    # monte carlo loop: run many hands, the law of big
    # numbers will do the rest
    for _ in range(nb_iterations):
        # play a hand, look for the winner
        random.shuffle(deck)

        other_players = deck[0:nb_players-1]
        if card_value > max(other_players):
            wins[card_value]+=1

# run the simulation for all the cards
# (it's not very interesting for the first values and for the last one, since the values are known to be 0 and 1)
for card_value in range(0, nb_cards+1):
    compute_card_probability(card_value)

wins = wins/float(nb_iterations)

# draws the plot as an image, and save results as a csv file
freqs = pd.DataFrame(wins, index=range(0, nb_cards+1), columns=['probability'])
ax = freqs.plot.bar()
output_directory = 'output'
basename = "{}-p-{}-i-{}".format(os.path.splitext(os.path.basename(__file__))[0], nb_players, nb_iterations)
plt.axhline(y=0.5, linewidth=1, color='red', linestyle='--')
plt.suptitle('Winning probabilities for each card value', fontsize=12)
plt.title('{} players, {} iterations'.format(nb_players, nb_iterations), fontsize=10)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylabel('Probability')
plt.xlabel('Card value')
plt.savefig("{}/{}.png".format(output_directory, basename))
freqs.to_csv('{}/{}.csv'.format(output_directory, basename))
```

on appelle le programme par exemple avec

```bash
$ python last-see1card.py -p 4 -i 10000
```

et on obtient des graphes dans le répertoire `output`.

## Et alors, faut parier quand ?

Hé bien ça dépend du nombre de joueurs.

 - à 3 joueurs, on gagne le pli dans plus de 50% des cas à partir du 16
 - à 4 joueurs, à partir du 18
 - à 5 joueurs, à partir du 19

Je dois avouer que ce qui suit a pas mal bousillé l'intérêt du dernier pli.

![](/assets/pictures/monte-carlo-tarot/last-see1card-p-3-i-100000.png)
![](/assets/pictures/monte-carlo-tarot/last-see1card-p-4-i-100000.png)
![](/assets/pictures/monte-carlo-tarot/last-see1card-p-5-i-100000.png)

## Comment on sait que les chiffres sont bons ?

c'est à dire: comment sait-on qu'avec `n` iterations, les chiffres sont corrects et qu'il n'est pas nécessaire de prendre un nombre supérieur pour avoir des chiffres meilleurs, c'est à dire plus précis, et sans variation significative ?

Ça dépend.

### Méthode rapide

Pour ce genre de programmes où on cherche à ne pas trop s'embêter, le plus simple, c'est de faire varier les paramètres, et de voir pifométriquement à partir de quand on arrête d'avoir des graphiques qui bougent. Pour `n = 10`, vous aurez des résultats très différents si vous faites tourner plusieurs fois le programme. À partir de `n=10000`, ça commence à ne plus trop bouger.

Ensuite, on peut voir si on gagne en précision. La courbe pour `n=10000` est presque identique à celle qu'on a avec `n=100000` (mais ça commence à prendre quelques secondes de calcul). C'est du au fait que la convergence des méthodes de Monte Carlo est proportionnelle à `sqrt(n)`: pour gagner un facteur 10 en précision, il faut multiplier par 100 le nombre d'itérations. Il y a donc un arbitrage à faire entre précision souhaitée, et temps de calcul

### Méthode rigoureuse

Si on veut une approche plus rigoureuse pour décider quand s'arrêter −c'est à dire pour constater qu'on a convergé au dela d'un seuil de précision à choisir−, il faut rentrer dans les méthodes statistiques.

C'est la [loi des grands nombres](https://fr.wikipedia.org/wiki/Loi_des_grands_nombres) qui indiquent que la moyenne des échantillons converge vers la valeur attendue (ici, la probabilité) au dela d'un certain nombre d'itérations. Et le [théorème central limite](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_central_limite) nous dit que la distribution de l'erreur converge vers une distribution normale.

On peut ainsi calculer l'[intervalle de confiance](https://fr.wikipedia.org/wiki/Intervalle_de_confiance). Tant qu'on atteint pas le degré de confiance recherché, on augmente la taille de l'échantillon.

## Pour aller plus loin

Parmi les conférences qui m'ont marqué, j'ai beaucoup aimé [Statistics for Hackers](https://www.youtube.com/watch?v=L5GVOFAYi8k) (40mn) ou, plus court, [Statistics without the agonizing pain](https://www.youtube.com/watch?v=5Dnw46eC-0o) (10mn) dont les titres sont explicites: il est question de faire des statistiques avec du code, sans s'embêter avec tout le (nécessaire et expliquable) formalisme mathématique. En raisonnant un peu, dans plein de situations, on peut facilement s'en sortir avec quelques boucles. Ca ressemble à ce qu'on a fait, mais ils proposent des outils un peu différents.

J'ai aussi commencé [Thinking in statistics](http://greenteapress.com/thinkstats2/html/index.html) qui semble prometteur.