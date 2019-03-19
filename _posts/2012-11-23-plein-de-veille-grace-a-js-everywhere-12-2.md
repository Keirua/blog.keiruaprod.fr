---
id: 506
title:
  - Plein de veille grâce à JS.Everywhere (1/2)
date: 2012-11-23T09:56:04+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=506
permalink: /2012/11/23/plein-de-veille-grace-a-js-everywhere-12-2/
keywords:
  - JS.Everywhere, veille, technos web, javascript
description:
  - "Compte rendu des conférences présentes lors de JS.Everywhere : sécurité, scaling d'application, applications pour télévisions"
robotsmeta:
  - index,follow
categories:
  - Développement Web
tags:
  - javascript
  - JS.Everywhere
  - technos web
  - veille
---
La semaine dernière, j&rsquo;ai gagné une entrée à la conférence JS.Everywhere grâce à un article sur [RudeBaguette](http://www.rudebaguette.com/2012/11/15/js-everywhere/). Merci aux organisateurs de m&rsquo;avoir donné cette opportunité de participer. Le planning était alléchant et je n&rsquo;ai pas été déçu, que ce soit par les conférences ou par le salon en lui même. Il y a avait de plus quelques pointures du web, comme par exemple [Douglas Crockford](http://en.wikipedia.org/wiki/Douglas_Crockford) (évangéliste célèbre du Javascript) et [Tristan Nitot](http://fr.wikipedia.org/wiki/Tristan_Nitot) (fondateur de Mozilla Europe).

Au niveau logistique, tout s&rsquo;est bien passé : les conférences avaient lieu au Tapis Rouge, un hotel plutôt classe dans le Xe, à Paris. La nourriture et les cafés n&rsquo;ont pas manqués toute la journée. Les conférences étaient à l&rsquo;heure, et elles se sont toutes globalement bien déroulés (à 2-3 soucis techniques près, comme toujours). Les écrans étaient gros, on y voyait bien, et on entendait bien les conférenciers. Bref sur le plan pratique, félicitation aux organisateurs qui pourront difficilement faire mieux.

Au niveau des conférences, c&rsquo;était très bon également. Certaines étaient pour tout le monde, mais pour la majorité des autres, il fallait choisir une conférence parmi 4. Toutes ne m&rsquo;intéressaient pas, mais j&rsquo;ai parfois regretté de ne pas avoir le don d&rsquo;ubiquité. J&rsquo;ai choisi de faire des conférence sur un peu tous les sujets : scalabilité, applis mobiles, sécurité, bonnes pratiques&#8230;

Qu&rsquo;en retenir ? Le mieux c&rsquo;est de vous parler un peu des conférences auxquelles j&rsquo;ai assisté. Je ne suis clairement pas un expert sur tous les sujets, autant le dire tout de suite. Mais c&rsquo;est l&rsquo;occasion de faire un tour d&rsquo;horizon de ce qui se passe dans plusieurs domaines. <!--more-->

## L&rsquo;architecture matérielle de grosses applications web

La journée a commencé par une présentation faite par Pierre Gilot, de chez Amazon, sur la conception de grosses applications qui ont besoin de grosse capacité, et de bien scaler. Comme Vimeo et SoundCloud, qu&rsquo;ils hébergent.  
Comment concevoir des applications de ce genre ? 3 choses essentielles selon lui :

  * **Concevoir pour planter**  
    L&rsquo;appli doit être conçue pour gérer les plantages : ça arrivera tôt ou tard. Il faut quand même continuer à fonctionner au mieux. Certaines boites comme NetFlix utilisent [Chaos Monkey](https://github.com/Netflix/SimianArmy/wiki), une application open source qui tue de manière aléatoire des process EN PRODUCTION pour simuler des plantages, et obliger l&rsquo;appli à être conçue pour gérer ça.
  * **Peu de couplage physique**  
    On nous a présenté comment concevoir l&rsquo;archi d&rsquo;une grosse application, à travers l&rsquo;exemple d&rsquo;un Youtube-like. Comment faire pour qu&rsquo;une telle appli scale correctement ? En découplant les entités physiquemment : une entité pour la communication avec le client, une entité pour recevoir les vidéos, une entité pour les encoder et éventuellement les raccourcir&#8230; Plus de détails sur [la page d&rsquo;Amazon si ça vous branche](http://aws.amazon.com/fr/architecture/). Ils présentent différents type d&rsquo;architecture pour différents types d&rsquo;applications.
  * **Du NoSQL**  
    Le problème du SQL, c&rsquo;est que ça ne scale pas bien quand le nombre de requêtes augmente, au contraire du [NoSQL](http://blog.neoxia.com/nosql-5-minutes-pour-comprendre/), qui scale linéairement avec le nombre de requêtes. De plus, le NoSQL chez Amazon propose une latence < 10ms quoi qu&rsquo;il arrive, donc des temps de réponses très bons. Le speaker présentait donc le NoSQL comme solution pour scaler, dommage qu&rsquo;il n&rsquo;ait pas parlé des sacrifices qui sont faits pour en arriver là. Si vous n&rsquo;avez jamais entendu parler de NoSQL, jetez un oeil à ce que proposent [MongoDB](http://www.mongodb.org/) et [CouchDB](http://couchdb.apache.org/ "CouchDB").

## Architecture javascript full stack avec Wakanda

A suivi une conférence sur le design d&rsquo;une architecture JavaScript full stack pour des applications business. C&rsquo;est à dire une application que n&rsquo;aurait que du JS chez le client, le serveur, et pour communiquer avec la base de données. Un tel design pourrait être une solution au problème des autres architectures, que ce soit pour du PHP, du Ruby ou de l&rsquo;ASP, qui sont obligées d&rsquo;utiliser plein de langage et d&rsquo;outils. Ca a été l&rsquo;occasion de parler de la solution développée par 4D, organisateur de l&rsquo;évènement (promis, après on a eu des conférences non sponsorisées). Il s&rsquo;agit de [Wakanda](http://www.wakanda.org/).

Le but du logiciel est de gérer le design de l&rsquo;appli via un editeur WYSIWYG, le design des entités en base, ainsi que d&rsquo;écrire le code serveur depuis l&rsquo;IDE (avec un serveur similaire à du nodeJS), et de déployer l&rsquo;application&#8230; Une fonctionnalité très sympa, c&rsquo;est celle de pouvoir faire des drag-n-drop d&rsquo;une entité vers un widget : quand on fait glisser l&rsquo;icone « Client » vers une listbox, l&rsquo;application sait que l&rsquo;on veut remplir la liste avec tous les clients. Après, on customize pour obtenir le résultat voulu, mais une bonne partie du travail est mâché.

Je suis pour le moment partagé sur cet outil. C&rsquo;est une bonne chose de voir des solutions javascript full-stack émerger. C&rsquo;est une bonne chose de voir que des outils de ce genre soient de plus en plus présents : cela montre que le web se dote d&rsquo;outils de qualité pour résoudre des problèmatiques pour lesquelles il est de moins en moins possible de bricoler, comme c&rsquo;est encore le cas actuellement pour pas mal de choses. Le web a beaucoup de retard par rapport à l&rsquo;informatique industrielle à ce sujet, et ce genre d&rsquo;initiatives me rend plutôt optimiste pour l&rsquo;avenir.

De l&rsquo;autre côté; il y a mon expérience de développeur. Pour avoir travaillé en C# et WPF, c&rsquo;est à dire avec des outils .Net qui permettent de faire des choses similaires (glisser-déplacer d&rsquo;entité et hydratation « magique » des widget, entre autres), je reste dubitatif. En WPF, on passe beaucoup de temps à se documenter pour arriver à modifier des comportements triviaux pour remplacer les comportements de base, que l&rsquo;on utilise au final très peu. Au lieu de gagner du temps, on en a passé autant qu&rsquo;avant, mais il a fallu se former sur des API peu intéressantes. Dans mon expérience (un gros projet en SSII, quelques milliers de jours hommes de dev), le WPF, qui était au départ une bonne idée, s&rsquo;est donc rapidement révélé contre productif. J&rsquo;espère que Wankada, passé l&rsquo;euphorie initiale, saura se montrer plus convaincant sur cet aspect.

## Les applications pour télévision

La conférence sur les applications pour télévision ne m&rsquo;a pas convaincu. J&rsquo;ai eu un peu de mal avec le speaker, qui nous balancait des Ferrero Rocher sans que l&rsquo;on comprenne vraiment pourquoi. Parfois pour féliciter les interventions pertinentes, parfois pour réveiller une salle qui s&rsquo;ennuyait un peu.

Le côté qui peut sembler attirant, c&rsquo;est le marché nouveau : tout est à faire dans le monde des applications pour télévision. Mais côté avantages, ça s&rsquo;arrête là, et l&rsquo;enthousiasme est largement calmé par les inconvénients qu&rsquo;il peut y avoir à concevoir son application pour une telle plateforme :

  * Côté développeurs, le monde des applications pour télévisions est difficile d&rsquo;accès : chaque constructeur a son propre SDK (gratuit pour la plupart il me semble). A l&rsquo;heure actuelle, il n&rsquo;y a aucun standard. Il faut donc concevoir une application par marque de téléviseur, ce qui est une première barrière.
  * Les SDK cassent régulièrement la rétro compatibilité de leurs API, rendant inutilisables les applications non mises à jour. Pas très glamour.
  * Côté utilisateurs, ça n&rsquo;est pas mieux : les gens n&rsquo;utilisent pas les applications disponibles sur leurs téléviseurs. Soit parce qu&rsquo;ils ne sont pas au courant qu&rsquo;il y a des app store, soit parce que cela ne les intéressent pas. Bref, les applications pour téléviseurs n&rsquo;ont pas l&rsquo;air très utilisées. Côté pénétration de marché, celui des smartphone/tablettes semble bien plus attirant.

En plus de tout ça, Douglas Crockford a été assez critique sur ce type d&rsquo;applications : pour lui cela n&rsquo;a pas de sens de mettre des technologies très changeantes comme les technologies web dans du matériel censé durer au moins 10 ans comme les télévisions.

## Internationalisation en Javascript

J&rsquo;ai raté les conférences de Sebastian Golasch ([@asciidisco](https://twitter.com/asciidisco) sur Github et Twitter) sur l&rsquo;internationalisation. Par contre, [sa présentation est sur le web](http://i18n.asciidisco.com/).  
C&rsquo;est une problèmatique importante et qui va probablement se développer dans les années à venir, étant donné l&rsquo;expansion du javascript côté client comme côté serveur. Pour le moment, peu de choses existent pour faire de la « vraie » internationalisation, c&rsquo;est à dire gérer correctement la pluralisation, les genres, les dates, les nombres&#8230; en javascript.  
Sa présentation était axée autour de 2 librairies :

  * [**messageformat.js**](https://github.com/SlexAxton/messageformat.js), qui vise à résoudre le problème des genres et de la pluralisation
  * [**globalize.js**](https://github.com/jquery/Globalize), qui cherche à gérer l&rsquo;internationalisation des dates et des nombres.

Je vous invite à regarder la présentation de Sebastian ainsi que les pages Github de ces 2 librairies pour aller plus en profondeur sur le sujet.

La suite de mon compte rendu dans un second article, la semaine prochaine.