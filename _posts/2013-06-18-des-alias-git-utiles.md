---
id: 576
title: Des alias git utiles
date: 2013-06-18T22:01:21+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=576
permalink: /2013/06/18/des-alias-git-utiles/
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - alias
  - git
---
Depuis quelques temps, j&rsquo;utilise les alias git pour un certain nombre de taches récurrentes, pour lesquelles je trouve les commandes de bases peu performantes, trop longues à taper, ou parce que je préfère ne pas retenir les nombreuses options qu&rsquo;elles proposent. Autre avantage : les alias décrits dans le fichier **.gitconfig** apparaissent dans l&rsquo;autocompletion de git, ce qui n&rsquo;est pas les cas si l&rsquo;on fait un alias bash. 

Voici quelques éléments contenus dans la section [alias] de mon fichier **~/.gitconfig**:  
<code lang="bash">&lt;br />
[alias]&lt;br />
lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)&lt;%an>%Creset' --abbrev-commit&lt;br />
</code>

Personnellement, je n&rsquo;ai jamais réussi à me servir de git log. Trop de place occupée pour trop peu d&rsquo;informations&#8230; avec cet alias, chaque commit est sur 1 ligne, les branches sont affichées et colorées, on peut voir de manière pratique qui a réalisé le commit et quand&#8230; très pratique donc, comme vous pouvez le voir sur l&rsquo;image ci-dessous :

[<img src="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log.png" alt="screen_better_log" width="724" height="463" class="alignright size-full wp-image-533" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log.png 724w, http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log-300x191.png 300w" sizes="(max-width: 724px) 100vw, 724px" />](http://blog.keiruaprod.fr/wp-content/uploads/2013/02/screen_better_log.png)

Avant un stand-up meeting, pensez à **git lg &#8211;since=yesterday**, qui vous permet de voir ce que vous avez commité depuis la veille.

<code lang="bash">&lt;br />
s = status -sb&lt;br />
</code>

L&rsquo;alias que j&rsquo;utilise le plus, car il évite de taper **git status** en entier, ou d&rsquo;avoir à appuyer sur tab pour compléter. Ca a l&rsquo;air idiot mais je tape cette commande probablement plusieurs dizaines de fois par jours, donc je revendique ma fainéantise sur la question.  
L&rsquo;option s signifie short (la sortie est épurée), et b permet d&rsquo;afficher la branche en cours, ce qui permet d&rsquo;éviter d&rsquo;avoir un commit sur la mauvaise branche&#8230;

<code lang="bash">&lt;br />
tryagain = reset –hard HEAD&lt;br />
</code>  
Parce que des fois, tout ce qui a été fait ne sert à rien et qu&rsquo;il vaut mieux recommencer à zéro.

<code lang="bash">&lt;br />
bv = branch -v&lt;br />
</code>  
pareil que **git branch**, mais affiche également le hash court du dernier commit effectué, ainsi que le titre de celui ci.  
Dans la même logique, si vous passez votre temps à jongler entre différents remote, vous pouvez penser à ajouter cet alias :  
<code lang="bash">&lt;br />
rv = remote -v&lt;br />
</code>

Si vous aussi vous avez des alias pour des taches récurrentes ou pour des commandes pratiques, n&rsquo;hésitez pas à le dire dans les commentaires !