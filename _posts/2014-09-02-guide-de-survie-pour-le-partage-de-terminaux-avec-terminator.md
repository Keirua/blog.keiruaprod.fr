---
id: 732
title: Guide de survie pour le partage de terminaux avec Terminator
date: 2014-09-02T17:22:33+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=732
permalink: /2014/09/02/guide-de-survie-pour-le-partage-de-terminaux-avec-terminator/
robotsmeta:
  - index,follow
categories:
  - Astuce
---
[<img src="http://blog.keiruaprod.fr/wp-content/uploads/2014/09/terminator-300x139.png" alt="terminator" width="300" height="139" class="alignright size-medium wp-image-734" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2014/09/terminator-300x139.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2014/09/terminator-1024x476.png 1024w, http://blog.keiruaprod.fr/wp-content/uploads/2014/09/terminator.png 1306w" sizes="(max-width: 300px) 100vw, 300px" />](http://blog.keiruaprod.fr/wp-content/uploads/2014/09/terminator.png)Il y a quelques semaines, mon collègue [tilap](http://www.tilap.net) écrivait [un article sur l&rsquo;utilisation de screen](http://tilap.net/ubuntu-splitter-fenetres-terminal-screen/) partager un terminal en plusieurs.

Screen est plus largement répandu, et permet de partager un terminal sans installation préalable lors d&rsquo;une connection SSH. Par contre au quotidien je préfère utiliser [terminator](http://gnometerminator.blogspot.fr/p/introduction.html), qui est quand même plus simple et convivial. Voici donc un petit guide de survie.

## Installation

L&rsquo;installation sur Ubuntu 14.04 se fait via :  
<code lang="bash">&lt;br />
apt-get install terminator&lt;br />
</code>

## Les raccourcis essentiels

4 raccourcis servent à faire la plupart des choses :

  * **ctrl+maj+o** = ouvre un terminal dans le répertoire actuel, une barre horizontale sépare alors les 2 terminaux
  * **ctrl+maj+e** = ouvre un terminal dans le répertoire actuel, une barre verticale sépare alors les 2 terminaux
  * **ctrl+maj+w** = ferme le terminal sélectionné
  * **ctrl+maj+x** = fait disparaitre les autres terminaux, en ouvrant le terminal sélectionné en grand. ctrl+maj+x permet de revenir aux autres écrans

Pour ceux qui aiment naviguer au clavier, on peut se déplacer entre les terminaux rapidement assez rapidement avec quelques  
**ctrl+tab** permet de naviguer vers le terminal suivant (ctrl+maj+tab pour obtenir le précédent)  
**ctrl+maj+gauche/droite/haut/bas** permet déplacer les séparateurs entre les différents terminaux

La configuration de terminator est stockée dans **~/.config/terminator/config**. Voici quelques paramètres que je trouve bien pour donner à terminator l&rsquo;apparence d&rsquo;un gnome shell :

`<br />
[global_config]<br />
  suppress_multiple_term_dialog = True<br />
[profiles]<br />
  [[default]]<br />
    background_image = None<br />
    background_color = "#2c001e"<br />
    split_to_group = True<br />
    show_titlebar = False<br />
    foreground_color = "#ffffff"<br />
`  
Cela permet d&rsquo;avoir la couleur de fond d&rsquo;ubuntu et masque les titres ajoutés par terminator, donnant ainsi aux terminaux le même aspect qu&rsquo;un gnome-terminal, mais en ayant plus de possibilités.