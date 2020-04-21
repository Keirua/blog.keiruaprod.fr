L'organisation chez démarches-simplifiées.

## Qui fait quoi chez les tech ?

Tout le monde fait de tout, au moins à petite dose: frontend JS/CSS, backend (rails), écriture de tests automatisés, déploiement de l'application et publication de releases, suivi de l'infrastructure via ansible, monitoring, support utilisateurs, réunions avec les utilisateurs…

## Combien on bosse ?

Comme dans beaucoup de projets beta.gouv (même si nous sommes un peu à l'extérieur de l'incubateur), les développeurs travaillent max 4j/5. Seule contrainte: être présent le mardi. C'est le jour où l'on place nos réunions d'équipes. On évite de mettre des réunions les autres jours, afin de réduire les interruptions.

Certains prennent le mercredi, d'autres travaillent seulement 3j. En général, chacun a tout le temps les mêmes jours de travail (ex: je ne travaille jamais pour DS le vendredi), ce qui permet aux autres d'organiser les projets, les séances de pair-programming en conséquences.

## Qui travaille aujourd'hui

Slack est notre principal moyen de communication asynchrone.
Tous les jours, on met un p'tit emoji slack pour indiquer si on travaille, et si on le fait depuis les bureaux ou depuis chez soi. En cas d'imprévu (fiston malade à garder?), on met un petit icone "off" pour prévenir.

## Rotation du support tech client

Tous les jours, quelqu'un parmi les développeurs s'occupe de répondre au support client (helpscout), de faire un tour des bugs sur sentry et/ou de traiter des issues github. Une notif rappelle dans slack de qui il s'agit.

## Standup quotidien

Tous les jours à midi, nous faisons une visio de max 15mn, sur zoom, où chacun parle de ce sur quoi il travaille et quelle sont les sujets qui le bloquent. Après ce tour de table, chacun peut évoquer si nécessaire des points transverses. Une notif slack invite tout le monde à rejoindre une visio dédiée à cela.

## Rétro/backlog grooming

Une semaine sur deux on fait un point d'une heure pour 
 - soit faire une rétro du sprint. On sort les tickets terminés du board, on fait éventuellement de la place. On fait une démo des tickets mis en prod, puis on prend 5mn pour faire un tour des +/- de la quinzaine et les présenter aux autres. On en tire des actions
 - soit trier le backlog: on fait le tour des tickets priorisés, on voit ce qu'on peut inclure raisonnablement dans l'itération

## Réunion d'équipe

Dans nos réunions d'équipe, on utilise parfois le format des petits séminaires de beta.gouv:

 - au début, on fait une liste de sujets transverses à toute l'équipe dont on souhaite discuter
 - on trie cette liste grossièrement par importance. Si des sujets sont portés par quelqu'un qui doit partir ensuite car réunion ailleurs, on l'aborde en priorité également.
 - un maitre du temps met un chrono sur 5mn
 - un scribe prend en note les discussions dans un framapad collaboratif
 - la personne qui a le premier sujet le présente, et on en discute
 - au bout de 5mn, s'il reste des choses à dire, on vote pour continuer à en parler ou pour passer au sujet suivant
 - quand on a fini avec un sujet, on passe au sujet suivant

## Pair programming en remote ?

Avec un p'tit coup de zoom, on a le son, et on peut partager l'écran pour faire du pair programming. Nous n'utilisons pas Vscode (c'est plutôt vim ou rubymine), nous n'avons pas testé leurs outils de travail collaboratif.

Avec une session tmux on peut se partager un terminal sur un serveur de dev à distance :

    # l'hôte crée une session
    $ tmux new -s tache_machin

    # l'invité s'y attache:
    $ tmux a -t tache_machin

En général ça sert plutôt pour les urgences (truc cassé en prod où une opération manuelle mineure permet d'aller chercher des logs) ou pour avoir 2 paires d'yeux quand on fait des mises à jours un peu lourdes.



