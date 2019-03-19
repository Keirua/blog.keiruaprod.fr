---
id: 531
title:
  - "Identifier l'origine d'une régression avec git bisect"
date: 2013-02-22T08:24:35+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=531
permalink: /2013/02/22/identifier-lorigine-dune-regression-avec-git-bisect/
keywords:
  - git, git bisect, recherche dichotomique, régression, outil de gestion de version
description:
  - "Comment identifier l'origine d'une regression grâce à la recherche dichotomique de git avec git bisect."
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - gestion de version
  - git
  - git bisect
  - recherche dichotomique
  - régression
---
[<img class="alignright size-full wp-image-534" alt="git_logo" src="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/git_logo.png" width="220" height="92" />](http://blog.keiruaprod.fr/wp-content/uploads/2013/02/git_logo.png)Quand on travaille sur un gros projet, on doit parfois identifier l&rsquo;origine d&rsquo;une régression. C&rsquo;est ce qui arrive par exemple lorsque l&rsquo;on modifie une fonctionnalité pour l&rsquo;enrichir : quelque chose a été cassé à un autre endroit qui utilisait la même fonctionnalité, en général sans que l&rsquo;on s&rsquo;en rende compte lors de la modification.

Une des difficultés, c&rsquo;est d&rsquo;identifier l&rsquo;origine de l&rsquo;erreur. Car lorsque l&rsquo;on est plusieurs à travailler sur le projet et qu&rsquo;il s&rsquo;est passé plusieurs dizaines (voire centaines, ou plus) de commit entre le moment où la fonctionnalité marchait et celle où elle a été identifié, retrouver le commit à l&rsquo;origine de l&rsquo;erreur peut s&rsquo;avérer être une tâche titanesque.

## Sauf que !

Parmi ses nombreuses fonctionnalités sympa, git propose une solution pour ce genre de situations : la **recherche dichotomique**. Pour ceux qui n&rsquo;écoutaient pas pendant les cours d&rsquo;algo, on va partir de l&rsquo;ensemble des commit, et regarder celui qui se trouve au milieu. On teste le programme, et si la régression est présente, on sait qu&rsquo;il faut chercher dans les commit qui se trouve avant, sinon dans ceux qui se trouvent après. Et on recommence, jusqu&rsquo;à ce qu&rsquo;on ait trouvé l&rsquo;origine de l&rsquo;erreur. Bien sûr, git propose un moyen pratique de faire ça, il s&rsquo;agit de **git bisect.**

## L&rsquo;avantage ?

La vitesse, et la rigueur ! Quand comme moi on a 85 commits à revoir, au lieu de tester un peu au hasard et n&rsquo;être pas sûr de trouver après de nombreux essais, avec cette méthode on est certain de trouver l&rsquo;origine de l&rsquo;erreur en environ 6 étapes. Et avec cette méthode, le nombre d&rsquo;étapes augmente lentement : pour 1000 commits, il y aurait seulement une dizaine de commits à revoir !

On fait comment ? Il faut tout d&rsquo;abord identifier un commit où la fonctionnalité marchait. Ça peut être une ancienne version taggée, un commit&#8230; bref, il faut avoir un point de départ. Dans cet exemple, on va dire qu&rsquo;il n&rsquo;y avait pas régression lors du commit bacd25e, et qu&rsquo;on s&rsquo;en est rendu compte dans la dernière version (sur le HEAD courant).

On démarre le mode de recherche :  
<code lang="bash">&lt;br />
git bisect start&lt;br />
</code>  
On indique que le HEAD est une version où la fonctionnalité considérée ne fonctionne pas :  
<code lang="bash">&lt;br />
git bisect bad&lt;br />
</code>  
On indique ensuite un commit où ça marche avec git bisect bad [hash du commit]

 <code lang="bash">git bisect good bacd25e </code>

**Et c&rsquo;est parti !**

Git nous positionne sur un commit intermédiaire, il faut maintenant tester l&rsquo;application dans ses différents états.

Après avoir testé, on indique à git si notre fonctionnalité marchait (avec **git bisect good**) ou ne marchait pas (avec **git bisect bad**). On obtient alors un nouveau commit à essayer, et ainsi de suite.

<p style="text-align: center;">
  <a href="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_goodbad.png"><img class="size-medium wp-image-535 aligncenter" alt="gitbisect_goodbad" src="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_goodbad-300x89.png" width="300" height="89" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_goodbad-300x89.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_goodbad.png 724w" sizes="(max-width: 300px) 100vw, 300px" /></a>
</p>

On continue à tester les différentes versions jusqu&rsquo;à ce que git nous dise qu&rsquo;on a fini de chercher.  
Git nous présente alors le coupable :

<p style="text-align: center;">
  <img class="size-medium wp-image-532 aligncenter" alt="gitbisect_summary" src="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_summary-300x75.png" width="300" height="75" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_summary-300x75.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/02/gitbisect_summary.png 724w" sizes="(max-width: 300px) 100vw, 300px" />
</p>

Il ne reste plus qu&rsquo;à regarder dans les modifications faites lors de ce commit (avec un outil tel que gitk par exemple, pour ne pas galérer dans la console s&rsquo;il y a eu de grosses modifications), et trouver l&rsquo;origine de l&rsquo;erreur. Avant de se mettre au boulot, revenez au bon endroit sur votre branche de travail en quittant le mode de recherche avec :

 <code lang="bash">git bisect reset</code>

## Bonus !

La commande log de git est par défaut assez peu pratique. Voici une commande que je trouve assez utile pour gagner de la place, voir les branches et mettre de la couleur :

 <code lang="bash">git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)&lt;%an&gt;%Creset' --abbrev-commit</code>

<p style="text-align: center;">
  <a href="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log.png"><img class="size-medium wp-image-533 aligncenter" alt="screen_better_log" src="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log-300x191.png" width="300" height="191" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log-300x191.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log.png 724w" sizes="(max-width: 300px) 100vw, 300px" /></a>
</p>

&nbsp;

Bon OK, c&rsquo;est très flou, mais vous voyez l&rsquo;idée.

Comme il n&rsquo;est pas très pratique de taper régulièrement cette commande, le plus simple est d&rsquo;en faire un alias :

 <code lang="bash">git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)&lt;%an&gt;%Creset' --abbrev-commit"&lt;br />
</code>

Désormais, lorsque l&rsquo;on tape git lg dans la console on a accès à ces logs plus sympa. Merci à [Filipe Kiss](https://coderwall.com/p/euwpig?i=1&p=1&q=sort%3Aupvotes+desc&t%5B%5D=merge+conflict&t%5B%5D=reflog&t%5B%5D=stash&t%5B%5D=pull&t%5B%5D=pull+request "A better git log") pour l&rsquo;astuce !