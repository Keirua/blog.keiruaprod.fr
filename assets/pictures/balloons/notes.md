# une partie avec les règles de base:

```
cargo build
./target/release/multiple_games --nb_players 2  --nb_parents 5 --nb_cards 5 --nb_iterations 10000000 > data2/2-5-5-10000000.json
source .env/bin/activate
(.env) clem@mobius:~/dev/ballons$ python3 mk_rs_plot.py -f /home/clem/dev/ballons/data2/2-5-5-10000000.json
```

![](./notes/2-5-5-10000000.png)

# Comparaison de l’influence du nombre de cartes "parent" sur la longueur des parties à 2 joueurs:

On sort les chiffres

```bash
./target/release/multiple_games --nb_players 2  --nb_parents 5 --nb_cards 5 --nb_iterations 10000000 > data2/2-5-5-10000000.json
./target/release/multiple_games --nb_players 2  --nb_parents 4 --nb_cards 5 --nb_iterations 10000000 > data2/2-4-5-10000000.json
./target/release/multiple_games --nb_players 2  --nb_parents 3 --nb_cards 5 --nb_iterations 10000000 > data2/2-3-5-10000000.json
./target/release/multiple_games --nb_players 2  --nb_parents 2 --nb_cards 5 --nb_iterations 10000000 > data2/2-2-5-10000000.json
```

On sort quelques graphiques
```bash
python3 mk_rs_plot.py -f /home/clem/dev/ballons/data2/2-2-5-10000000.json
python3 mk_rs_plot.py -f /home/clem/dev/ballons/data2/2-3-5-10000000.json
python3 mk_rs_plot.py -f /home/clem/dev/ballons/data2/2-4-5-10000000.json
python3 mk_rs_plot.py -f /home/clem/dev/ballons/data2/2-5-5-10000000.json
```

# Énumération manuelle des mains possibles:

11111
2111
311
41
5
221
32

## Dénombrement des différentes mains:

https://perso.univ-rennes1.fr/philippe.roux/enseignement/proba1/exo762sol.pdf

## Probabilité d’avoir les différentes mains

raw hand count with 1000000 hands:
{'5': 100, '14': 9426, '23': 37340, '11111': 58588, '113': 141093, '122': 283629, '1112': 469824}
{'5': 94,  '14': 9519, '23': 37610, '11111': 59149, '113': 141198, '122': 281279, '1112': 471151}
problem = quadratic convergence: having 1 more digit = 100 times more iterations
time python3 gen_hand_structure.py -p 5 -b 5 -i 1000000
{'5': 79, '14': 9387, '23': 37784, '11111': 58973, '113': 140978, '122': 282434, '1112': 470365}

real	0m19,588s
user	0m19,587s
sys	0m0,000s

# most frequent hands
```
python3 gen_hand_structure_pie.py
```

'1112', '122', '113', '11111', '23', '14', '5'

probabilité de les rencontrer:

5, 0.0079
14, 0.9387
23, 3.7784
11111, 5.8973
113, 14.0978
122, 28.2434
1112, 47.0365

47% des mains sont des 1112
96% des mains sont des 1112, 122, 113, 11111

![](./notes/piechart.png)

# Heatmap avec les probabilités de victoire en fonction des différentes rencontres de mains ?

Certaines rencontres sont impossibles:
 - 5 vs 11111
Certaines sont très peu probables, donc il faut aider le destin pour en avoir:
 - 5 vs 11111

Dans une première approche, on génère

On récupère les comptes de rencontres et de victoires:

```bash
time python3 gen_hand_heatmap.py -p 5 -b 5 -i 10000000
{'1112': {'1112': [1096634, 2264360], '122': [534765, 1316073], '113': [199703, 633220], '11111': [169968, 292299], '23': [43289, 163734], '14': [5431, 37203], '5': [7, 314]}, '122': {'1112': [748418, 1317176], '122': [387001, 793237], '113': [159508, 408524], '11111': [108201, 163988], '23': [36298, 109777], '14': [5929, 30139], '5': [30, 379]}, '113': {'1112': [420634, 632480], '122': [242647, 409511], '113': [106885, 217067], '11111': [54222, 72753], '23': [26445, 61486], '14': [4603, 16608], '5': [21, 175]}, '11111': {'1112': [112353, 292343], '122': [51235, 163561], '113': [17070, 72373], '11111': [18536, 38556], '23': [3447, 18062], '14': [292, 2964], '5': [0, 0]}, '23': {'1112': [118097, 163429], '122': [71744, 109826], '113': [34123, 61269], '11111': [14407, 18205], '23': [9059, 18273], '14': [1761, 5487], '5': [11, 75]}, '14': {'1112': [31439, 37283], '122': [24018, 30261], '113': [11879, 16574], '11111': [2688, 3042], '23': [3644, 5433], '14': [765, 1513], '5': [6, 25]}, '5': {'1112': [306, 318], '122': [318, 344], '113': [170, 184], '11111': [0, 0], '23': [69, 80], '14': [15, 17], '5': [0, 0]}}

real	9m57,285s
user	9m57,191s
sys	0m0,032s
```
on met ça dans plot_hand_heatmap.py:

![](notes/heatmap.png)

Le problème de cette approche, c’est qu’elle génère beaucoup de parties probables, mais les parties peu probables sont mal représentées (cf les chiffres dans `heatmap-naive.json`).
Sur ces types de parties, il y a donc moins de parties simulées, et donc les chiffres de probabilités de victoires sont moins précis.

Il faut un meilleur algorithme de génération de parties.

Cependant, pour les parties fréquentes (carré avec '1112', '122' et '113'), on a déja pas mal de parties simulées et on pourrait déjà regarder les chiffres.

Maintenant, il n’est pas nécessaire de générer tous les matchs ; seuls la moitié supérieure de la matrice des rencontres est nécessaire, l’autre peut être déduite (si a rencontre b et gagen dans x% des cas, lors de la rencontre b contre a la victoire aura lieu dans 100-x % des cas).


# Génération de toutes les mains possibles


## Nombre de mains par types de mains

il se trouve qu’il y a beaucoup de symétries et qu’il y a au final assez peu de mains différents.

Voici le nombre de mains par types de mains:

```
$ time python3 gen_every_hands.py 
11111 	1
5 		5
41 		20
32 		20
311 	60
221 	60
2111 	120
```

Au total, 286 mains différentes, réparties sur 7 structures différentes, existent

 - genération de toutes les mains
 - genération de toutes les rencontres possibles
 - création d’une partie à 2 joueurs avec des mains sélectionnées


## Régénération des chiffres de probabilités de victoire, avec plus de chiffres pour les rencontres peu fréquentes

```bash
 time python3 gen_hand_heatmap_uniform.py --nb_iterations 10000
{'11111': {'11111': [4753, 10000], '5': [0, 0], '41': [1081, 10000], '32': [1946, 10000], '311': [2444, 10000], '221': [3111, 10000], '2111': [3815, 10000]}, '5': {'11111': [0, 0], '5': [4945, 10000], '41': [7750, 10000], '32': [8633, 10000], '311': [8956, 10000], '221': [9323, 10000], '2111': [9529, 10000]}, '41': {'11111': [8790, 10000], '5': [2229, 10000], '41': [4888, 10000], '32': [6680, 10000], '311': [7164, 10000], '221': [7926, 10000], '2111': [8386, 10000]}, '32': {'11111': [7912, 10000], '5': [1232, 10000], '41': [3352, 10000], '32': [4963, 10000], '311': [5653, 10000], '221': [6520, 10000], '2111': [7218, 10000]}, '311': {'11111': [7383, 10000], '5': [979, 10000], '41': [2808, 10000], '32': [4244, 10000], '311': [4839, 10000], '221': [5949, 10000], '2111': [6602, 10000]}, '221': {'11111': [6675, 10000], '5': [637, 10000], '41': [2025, 10000], '32': [3394, 10000], '311': [4024, 10000], '221': [4804, 10000], '2111': [5714, 10000]}, '2111': {'11111': [5808, 10000], '5': [461, 10000], '41': [1533, 10000], '32': [2636, 10000], '311': [3208, 10000], '221': [4080, 10000], '2111': [4886, 10000]}}

real	0m36,663s
user	0m36,661s
sys	0m0,000s
```

En fusionnant les résultats précédents afin de ne pas avoir à recalculer trop les parties très fréquentes qui ont déjà beaucoup de chiffres:

```bash
time python3 gen_hand_heatmap_uniform.py --nb_iterations 100000
{'2111': {'2111': [1096634, 2264360], '221': [534765, 1316073], '311': [199703, 633220], '11111': [169968, 292299], '32': [69997, 263734], '41': [21130, 137203], '5': [4297, 100314]}, '221': {'2111': [748418, 1317176], '221': [387001, 793237], '311': [159508, 408524], '11111': [108201, 163988], '32': [70114, 209777], '41': [25779, 130139], '5': [6455, 100379]}, '311': {'2111': [420634, 632480], '221': [242647, 409511], '311': [106885, 217067], '11111': [128528, 172753], '32': [69617, 161486], '41': [32812, 116608], '5': [9761, 100175]}, '11111': {'2111': [112353, 292343], '221': [82382, 263561], '311': [40647, 172373], '11111': [66401, 138556], '32': [22986, 118062], '41': [11305, 102964], '5': [0, 0]}, '32': {'2111': [118097, 163429], '221': [136920, 209826], '311': [89716, 161269], '11111': [93415, 118205], '32': [58034, 118273], '41': [35266, 105487], '5': [12623, 100075]}, '41': {'2111': [115177, 137283], '221': [103424, 130261], '311': [83104, 116574], '11111': [90862, 103042], '32': [69726, 105433], '41': [50588, 101513], '5': [22455, 100025]}, '5': {'2111': [95782, 100318], '221': [93662, 100344], '311': [90142, 100184], '11111': [0, 0], '32': [87187, 100080], '41': [77193, 100017], '5': [49855, 100000]}}

real	4m42,866s
user	4m42,708s
sys	0m0,056s
```

En réécrivant l’algorithme clé en rust, et en l’appelant coté python qui s’occupe de générer les rencontres, on peut obtenir 100000 itérations beaucoup plus rapidement:

```bash
cd ballonslib
cargo build
cd ..
source .env/bin/activate
time python3 gen_hand_heatmap_uniform_rs.py --nb_iterations 100000
{'11111': {'11111': [47717, 100000], '5': [0, 0], '41': [10470, 100000], '32': [19045, 100000], '311': [22469, 100000], '221': [30415, 100000], '2111': [37516, 100000]}, '5': {'11111': [0, 0], '5': [49962, 100000], '41': [75715, 100000], '32': [86602, 100000], '311': [88586, 100000], '221': [92827, 100000], '2111': [95045, 100000]}, '41': {'11111': [88793, 100000], '5': [23996, 100000], '41': [49737, 100000], '32': [66697, 100000], '311': [70526, 100000], '221': [79542, 100000], '2111': [84292, 100000]}, '32': {'11111': [79415, 100000], '5': [13231, 100000], '41': [32596, 100000], '32': [49590, 100000], '311': [54352, 100000], '221': [64268, 100000], '2111': [71442, 100000]}, '311': {'11111': [75366, 100000], '5': [10967, 100000], '41': [28740, 100000], '32': [44613, 100000], '311': [49328, 100000], '221': [59507, 100000], '2111': [66636, 100000]}, '221': {'11111': [66348, 100000], '5': [6770, 100000], '41': [19502, 100000], '32': [33529, 100000], '311': [38470, 100000], '221': [48903, 100000], '2111': [56727, 100000]}, '2111': {'11111': [58909, 100000], '5': [4856, 100000], '41': [15418, 100000], '32': [27192, 100000], '311': [31425, 100000], '221': [40904, 100000], '2111': [48065, 100000]}}

real	0m19,683s
user	0m19,635s
sys	0m0,048s
```

# Better algorithm

one of the players counts the remaining cards in the hope of improving its odds of staying in the game

```bash
time python gen_hand_heatmap_uniform_with_counter.py --nb_iterations 10000
{'11111': {'11111': [5304, 10000], '5': [0, 0], '41': [1338, 10000], '32': [2379, 10000], '311': [2804, 10000], '221': [3656, 10000], '2111': [4356, 10000]}, '5': {'11111': [0, 0], '5': [4998, 10000], '41': [7717, 10000], '32': [8681, 10000], '311': [9027, 10000], '221': [9337, 10000], '2111': [9543, 10000]}, '41': {'11111': [8781, 10000], '5': [2189, 10000], '41': [4775, 10000], '32': [6572, 10000], '311': [7062, 10000], '221': [7765, 10000], '2111': [8348, 10000]}, '32': {'11111': [7915, 10000], '5': [1346, 10000], '41': [3489, 10000], '32': [5082, 10000], '311': [5684, 10000], '221': [6601, 10000], '2111': [7253, 10000]}, '311': {'11111': [7547, 10000], '5': [978, 10000], '41': [2833, 10000], '32': [4341, 10000], '311': [4938, 10000], '221': [6000, 10000], '2111': [6700, 10000]}, '221': {'11111': [6752, 10000], '5': [720, 10000], '41': [2273, 10000], '32': [3725, 10000], '311': [4176, 10000], '221': [5088, 10000], '2111': [5914, 10000]}, '2111': {'11111': [6063, 10000], '5': [543, 10000], '41': [1894, 10000], '32': [3029, 10000], '311': [3543, 10000], '221': [4461, 10000], '2111': [5169, 10000]}}

real	0m44,034s
user	0m44,033s
sys	0m0,001s
```

# Facteur de branchement

Le facteur de branchement, c’est le nombre d’état vers lequel on peut aller depuis un état donné.

On peut l’encadrer: il est entre 1 (après toutes les cartes, ballon ou action, on joue une nouvelle carte) et 4 (si on a 4 ballons explosés et qu’on pioche une carte "parent", on a le choix parmi 4 cartes).

On peut le moyenner:
 - 20 cartes sur 25, les cartes «ballon», ont un facteur de branchement de 1
 - 5 cartes sur 25, les cartes «parent», ont un facteur de branchement qui est maximum de 4

Le facteur de branchement moyen est donc majoré par 20/25 * 1 + 5/25 * 4 = 0.8 + 4*0.2 = 1.6

Enfin, on peut le simuler pour trouver une valeur approchée plus réaliste de ce chiffre:

```python
python3 gen_branching_factor.py --nb_iterations 10000
1.2827724636190512
```

Avec 10000 itérations, on a `1.28` de manière consistante.

Ceci étant dit, même avec un facteur de branchement très faible, on a vu que les parties peuvent être longues, parfois plus de 100 coups.

>>> 1.28 ** 100
52601359015.48384

Il reste difficile d’explorer toutes les branches


Du coup:
 - on ne joue pas vraiment une main contre une autre, mais plutôt une structure de main contre une autre
 - la simulation par Monte Carlo direct fourni quand même des résultats satisfaisants
 - on constate la convergence empirique des résultats
 - 2 facteurs influencent les chances de victoire d'une main:
  - en général, la probabilité d'obtenir chaque main
  - le nombre de cartes de la plus longue chaine
 - du fait du faible facteur de branchement et des résultats constatés, une méthode plus élaboré type MCTS (Monte Carlo Tree Search), qui élague l'espace de recherche, ne parait pas nécessaire pour effectuer des simulations plus précises
 - optimisation par heuristique gloutonne:
 	- compter les cartes restantes permet d'améliorer ses chances de victoire dans certains cas, jusqu'à +6%.
 		- todo: tester avec plus d'itérations (`time python3 gen_hand_heatmap_uniform_with_counter.py -i 100000`) pour avoir des chiffres plus précis
 	- c'est l'idée qui m'apparaissait évidente, ici les résultats sont chiffrés.
 	- Certaines mains (comme 5) ne peuvent pas être optimisée (ainsi, ou tout court) car leur facteur de branchement est nécessairement de 1
 - autre idée d'optimisation ():
    - si possible, récupérer les cartes dans les plus longues chaine, sinon parmi celles les moins présentes dans le tas ?
 - un constat qui n'était pas évident au départ pour moi: plus une main est fréquente lors de la distribution, plus… elle a de chance de perdre. Au contraire, les mains peu probables avec de nombreuses cartes d'une même couleur perdent en général moins souvent.
 - la main de type 5 est un cas particulier, et le résultat m'a surpris car contre-intuitif. C'est la meilleure main, avec des scores de victoire bien supérieurs aux autres il y a seulement 4 cartes action de chaque couleur, mais 5 cartes «parent» qui permettent de récupérer des cartes. Il est donc plus probable de récupérer des cartes que d'en perdre, cette main peut donc rester en jeu
 - idée de simulation:
  - faire une partie à une main de chaque type, et se dire que l'optimisation de la chance de victoire de ce type de main, c'est l'optimisation de la longueur en jeu de cette main. ainsi:
    - on peut regarder le facteur de branchement moyen sur une partie à une main
  	- la main de type 5 ne peut être optimisée, car le facteur de branchement est toujours de 1
  - on peut retrier les graphiques pour avoir la main 11111 en haut

On peut classer les mains par forces:

11111 	1
2111 	120
221 	60
311 	60
32 		20
41 		20
5 		5

Sauf pour la main 11111, la force est inversement corrélée au nombre de cartes dans le type de main en question. Plus le nombre est élevé, plus il est difficile de gagner




```
time python3 gen_hand_heatmap_uniform_with_counter.py -i 100000
{'11111': {'11111': [52385, 100000], '5': [0, 0], '41': [13985, 100000], '32': [23765, 100000], '311': [28522, 100000], '221': [36589, 100000], '2111': [43711, 100000]}, '5': {'11111': [0, 0], '5': [49818, 100000], '41': [77532, 100000], '32': [87073, 100000], '311': [89931, 100000], '221': [93437, 100000], '2111': [95476, 100000]}, '41': {'11111': [87588, 100000], '5': [21144, 100000], '41': [48194, 100000], '32': [64776, 100000], '311': [70108, 100000], '221': [78355, 100000], '2111': [83127, 100000]}, '32': {'11111': [79615, 100000], '5': [13319, 100000], '41': [34845, 100000], '32': [50853, 100000], '311': [57183, 100000], '221': [65705, 100000], '2111': [72647, 100000]}, '311': {'11111': [74691, 100000], '5': [10042, 100000], '41': [28545, 100000], '32': [43752, 100000], '311': [50238, 100000], '221': [59222, 100000], '2111': [66464, 100000]}, '221': {'11111': [67806, 100000], '5': [7517, 100000], '41': [22438, 100000], '32': [36058, 100000], '311': [41905, 100000], '221': [51285, 100000], '2111': [58744, 100000]}, '2111': {'11111': [60751, 100000], '5': [5369, 100000], '41': [18006, 100000], '32': [29949, 100000], '311': [34969, 100000], '221': [44153, 100000], '2111': [51788, 100000]}}

```


time target/release/gen_hand_heatmap_uniform_parallel --nb_iterations 100000
time target/release/gen_hand_heatmap_uniform_parallel --nb_iterations 100000 --fast