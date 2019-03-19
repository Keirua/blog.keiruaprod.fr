---
id: 636
title:
  - "Présentation d'Apache Bench"
date: 2013-08-18T22:14:33+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=636
permalink: /2013/08/18/presentation-dapache-bench/
keywords:
  - apache bench, monitoring, benchmark, serveur, dimensionnement
description:
  - "Présentation d'Apache Bench, un outil de benchmark serveur qui sert pour le dimensionnement"
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - apache bench
  - benchmark
  - dimensionnement
  - monitoring
  - serveur
---
Apache bench est un outil qui sert à faire des tests de performances sur une URL donnée.  
On l&rsquo;installe via apt-get install apache2-utils, puis on s&rsquo;en sert (par exemple) de la manière suivante :

<code lang="bash">&lt;br />
ab -n x -c y url&lt;br />
</code>

Avec :

  * **x** le nombre de requêtes à lancer
  * **y** le nombre de requêtes concurrentes
  * **url** l&rsquo;url à tester, qui doit finir par un /

Exemple :  
<code lang="bash">&lt;br />
ab -n 1000 -c 100 www.google.com/&lt;br />
</code>

On obtient ensuite un rapport avec notamment, le temps moyen de réponse, la bande passante consommée, le nombre de requêtes traitées par secondes&#8230; D&rsquo;autres options sont possibles, et vous les trouverez dans les pages man.

Il est important de savoir que cet outil effectue uniquement une requête HTTP GET sur l&rsquo;url concernée : dans l&rsquo;exemple donné il va donc uniquement télécharger le HTML, mais pas les fichiers images, js et css externes, et ne les utilisera pas. Cela ne représente donc pas le ressenti réel de l&rsquo;utilisateur, mais sert pour du dimensionnement.

On peut s&rsquo;en servir de plusieurs manières. Sur une machine locale (ou la notion de bande passante n&rsquo;a aucun sens), cela peut servir à tester l&rsquo;effet de la mise en place d&rsquo;un système de cache type Memcached ou Redis, ou bien pour voir si la configuration du reverse proxy tient la route. En production ou préproduction, cela permet de voir si la stack fait bien son travail. Mais surtout, Après avec effectué ce genre de requêtes, on regarde les outils de monitoring, et peut surveiller l&rsquo;état de nombreux éléments : load, accès disques, etat de la base de données&#8230;

Attention, comme cet outil fonctionne url par url, il est important d&rsquo;effectuer des tests sur plusieurs pages différentes, surtout les plus critiques (en terme de temps d&rsquo;exécution et de fréquentation). Bien que votre home soit probablement la plus visitée, c&rsquo;est aussi surement une des pages les mieux optimisées. D&rsquo;autres pages un peu moins visitées peuvent être dangereuses pour les performances (lorsqu&rsquo;elles ont de lourds calculs par exemples), et la santé de votre serveur.

L&rsquo;idée de ce genre de d&rsquo;outil, c&rsquo;est surtout de regarder à quel moment le serveur va tomber en terme de charge. On effectue plusieurs tests avec des valeurs de plus en plus élevées, et on regarde à partir de quel moment le serveur ne tient plus. On fait ce genre de tests bien avant que le serveur n&rsquo;atteigne de tels chiffres de fréquentation, ce qui permet d&rsquo;anticiper les évolutions d&rsquo;architecture à prévoir.