---
id: 760
title: 'Faire une vidéo timelapse d&rsquo;un écran sous Ubuntu'
date: 2015-01-24T17:00:17+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=760
permalink: /2015/01/24/faire-une-video-timelapse-dun-ecran-sous-ubuntu/
robotsmeta:
  - index,follow
categories:
  - Astuce
lang: fr
---
Il y a quelques temps, j&rsquo;ai du filmer un écran pendant un long moment, plusieurs heures; comme il n&rsquo;allait rien s&rsquo;y passer pendant la majeure partie du temps, utiliser une application qui allait prendre plusieurs images par seconde n&rsquo;était pas envisageable, car le fichier de sortie aurait rapidement atteint une taille trop grosse. De plus, j&rsquo;avais juste besoin de voir en gros les moments où il y aurait de l&rsquo;activité donc je n&rsquo;avais pas besoin d&rsquo;une telle précision. Une précision de l&rsquo;ordre de la seconde suffisait largement.

J&rsquo;ai donc opté pour un script shell, qui faisait **une capture d&rsquo;image par seconde**, que j&rsquo;ai ensuite assemblée, à une vitesse supérieure (plusieurs images par secondes). On appelle ce genre de vidéo un **timelapse**.

Divers articles m&rsquo;ont aidé, mais c&rsquo;est finalement [celui-ci](http://www.bhalash.com/archives/885403473) que j&rsquo;ai mis en oeuvre car il est simple. Le processus est assez facile à reproduire sur une Ubuntu.

On commence **récupérer les deux packages** que l&rsquo;on va utiliser, pour faire les captures puis l&rsquo;assemblage :

<codelang="bash">$ apt-get install scrot mplayer</code>

Pour faire les captures d&rsquo;écran, on écrit le **script shell** suivant, qu&rsquo;on lance et qu&rsquo;on laisse tourner :

<code lang="bash">#!/bin/sh&lt;br />
while [ 1 ]; do scrot -q 100 $(date +%Y%m%d%H%M%S).jpg; sleep 1; done</code>

Ce script prend une capture toute les secondes, et sauvegarde dans un fichier JPEG dont le nom correspond à la date formattée.

Une fois la capture terminée, on arrête le script et **on liste les fichiers images** dans un fichier, du plus récent au plus ancien :

<code lang="bash">$ ls -1tr *.jpg > files.txt</code>  
C&rsquo;est l&rsquo;occasion de découvrir de nouveaux paramètres pour ls !

**-1** permet d&rsquo;avoir un nom de fichier par ligne (attention, c&rsquo;est le chiffre « un », pas la lettre « l »)  
**-t** trie les fichiers par date de modification  
**-r** inverse l&rsquo;ordre des fichiers

**On assemble enfin les images** avec mencoder, à raison de 20 images par secondes. Vous pouvez ou non ajouter un fichier mp3 directement pendant l&rsquo;assemblage :

<code lang="bash">$ mencoder -ovc x264 -oac mp3lame -audiofile basket_case.mp3 -mf w=1400:h=900:fps=20:type=jpg 'mf://@files.txt' -o screenlapse.avi</code>

Et voila. Prochaine utilisation de ce script lors de ma participation à une future Ludum Dare, peut être la 32ème ? Les timelapse de participants y sont monnaie courante.