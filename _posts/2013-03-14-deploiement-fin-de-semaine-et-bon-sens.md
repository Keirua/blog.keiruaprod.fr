---
id: 548
title:
  - Déploiement, fin de semaine et bon sens
date: 2013-03-14T23:05:52+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=548
permalink: /2013/03/14/deploiement-fin-de-semaine-et-bon-sens/
keywords:
  - bon sens, intégration continue, déploiement, tests automatisés
description:
  - "A ne pas oublier lorsque l'on réalise un déploiement"
robotsmeta:
  - index,follow
categories:
  - Bonnes pratiques
tags:
  - bon sens
  - déploiement
  - Intégration continue
---
Récemment, la question de savoir s&rsquo;il faut ou non mettre en prod un projet en fin de semaine a fait apparaître quelques trucs humouristiques, tel que [Estcequonmetenprodaujourdhui.info](http://www.estcequonmetenprodaujourdhui.info/) ou bien l&rsquo;image de [CommitStrip](http://www.commitstrip.com/2013/03/08/ceci-est-un-message-de-prevention/).

Mon opinion sur la question est plus proche de celle développée dans l&rsquo;article d&rsquo;[Yves](http://log.winsos.net/2013/03/12/ne-pas-pousser-en-prod-le-vendredi-faux.html), même si je trouve sa vision un peu trop manichéenne.

Selon lui les clés d&rsquo;un déploiement réussi c&rsquo;est, entre autres :

  * Un système de déploiement
  * Des tests
  * La maîtrise du volume de changement

Toujours selon lui, lorsque l&rsquo;on maîtrise ces 3 éléments, on peut déployer n&rsquo;importe quand.

Je le rejoins tout à fait sur le système de déploiement. Sans avoir un process complexe d&rsquo;**intégration continue**, il me semble irresponsable de travailler sans un **outil de déploiement** qui permette d&rsquo;annuler une mise en prod en cas de problème, et de revenir à un état antérieur stable. Pas besoin d&rsquo;un système complexe pourvu que ça marche et qu&rsquo;il soit fiable : je travaille actuellement avec un outil qui doit faire bien moins 30 lignes de script shell, et qui fait très largement ce dont j&rsquo;ai besoin. Je peux déployer en une commande dans un terminal, et en cas de problèmes, revenir en arrière en une commande. Plein de solutions plus complètes existent, mais cela pourrait être le sujet d&rsquo;articles dédiés.

Pour le reste, je suis plus modéré : il arrive que du code soit non testé car difficile à tester de manière automatisé, ou qu&rsquo;il y ait des effets de bords difficiles à reproduire&#8230; bref dans la vraie vie, un déploiement, ça ne se passe pas comme ça devrait. N&#8217;empêche qu&rsquo;avec un peu de bon sens et de bons outils, on peut mettre en prod un vendredi, pourvu qu&rsquo;on maîtrise ce qui est fait.

C&rsquo;est justement là où je voudrais en venir. **Le bon sens**.

Voici la scène à laquelle j&rsquo;ai participé, impuissant :  
Il y a 5 développeurs.  
Celui qui doit mettre en production est arrivé récemment dans la société et doit réaliser son premier déploiement. Il doit donc être assisté pour utiliser les outils (qu&rsquo;il ne connait pas), et pour vérifier qu&rsquo;il n&rsquo;oublie rien.  
Un des autres développeurs doit partir à 17h et faire du télétravail le lendemain. 2 autres donnent une formation à l&rsquo;étranger (6h de décalage horaire, mais joignables via messagerie instantanée). Le dernier, sur les lieux, n&rsquo;a que peu d&rsquo;expérience sur le projet, et n&rsquo;a pas la main sur de nombreux outils (base de prod, outils serveur, etc&#8230;).  
La mise en production ayant déjà été retardée à cause de divers problèmes pratiques, le moment où la mise en production peut effectivement avoir est jeudi vers 16h30.  
Outils de tests automatisés : aucuns (à mon grand désespoir).  
Impact de la mise en production : l&rsquo;intégralité du site, car liée aux URls (le but étant d&rsquo;améliorer le SEO).

## Fallait-il mettre en production ce jeudi-là ?

Tel que je le présente, il me semble évident que non.

En effet avec n&rsquo;importe quel outil de gestion de version, comme celui utilisé ici, il est possible pour ce développeur de continuer à travailler sur d&rsquo;autres choses en attendant de pouvoir mettre en ligne lorsque les conditions sont propices. Je n&rsquo;aurais pas fait ce déploiement de type &lsquo;big bang&rsquo; le lendemain, mais j&rsquo;aurais attendu le lundi. Le développeur le plus expérimenté travaillant depuis chez lui et 2 des autres n&rsquo;étant joignables qu&rsquo;à partir de 15h, celà n&rsquo;aurait pas été idéal, d&rsquo;autant plus que l&rsquo;essentiel de l&rsquo;activité de la société a lieu au cours du weekend, et qu&rsquo;il est inconcevable que le site soit KO durant cette période. Bref, dans l&rsquo;idéal j&rsquo;aurais attendu lundi. Si ce n&rsquo;était pas possible (admettons), j&rsquo;aurais au moins attendu le lendemain, plutôt que de presser un développeur déjà stressé par l&rsquo;impact potentiellement néfaste de son travail, et par la journée déjà bien avancée.

La mise en production a donc bien eu lieu. La mise en préproduction ayant en effet déjà démarré, les autres développeurs étaient bloqués pour faire les leurs. Divers projets n&rsquo;attendant que l&rsquo;arrivée d&rsquo;un développeur rendaient également pressant ce déploiement. Plutôt que de revenir en arrière et faire le déploiement tranquillement le lendemain, il a été demandé de finir ce qui avait été commencé, afin de laisser la place aux autres par la suite. Intérêt faible : le gain de ce déploiement se consaste après plusieurs semaines, et via la gestion de version, tout le monde aurait pu s&rsquo;y retrouver convenablement.

Je suis donc convaincu que le choix qui a été réalisé était plus mauvais qui puisse être fait.

Il n&rsquo;a pas fallu beaucoup de temps pour me donner raison : le déploiement a échoué à cause de nombreux effets de bord qui n&rsquo;apparaissaient pas dans les autres environnements (ce qui aurait pu  être évité), le déploiement a finalement été repoussé, et une nouvelle branche de travail a du être mise en place pour travailler en parallèle. Quand au malheureux développeur, il est resté jusqu&rsquo;à 23h pour essayer de déployer, puis revenir en arrière.

Bref, ne pas oublier d&rsquo;avoir du bon sens. C&rsquo;est ce que font [de nombreuses boites](http://log.winsos.net/2013/03/14/deploiement-continu-quelques-exemples.html), qui n&rsquo;ont plus à prouver qu&rsquo;elles savent avoir une application en ligne. Déployer ne doit pas avoir [à ressembler à ceci](http://lesjoiesducode.tumblr.com/post/24053692228/quand-je-fais-une-mise-en-prod "Quand je fais une mise en prod").