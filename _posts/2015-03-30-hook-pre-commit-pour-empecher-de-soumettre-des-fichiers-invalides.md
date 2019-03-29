---
id: 775
title: Un hook pre-commit pour empêcher de soumettre des fichiers PHP invalides
date: 2015-03-30T22:30:46+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=775
permalink: /2015/03/30/hook-pre-commit-pour-empecher-de-soumettre-des-fichiers-invalides/
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - git
  - hook
  - Php
lang: fr
---
Il est facile d&rsquo;ajouter des fichiers invalides dans un système de contrôle de version si on ne fait pas attention. Un des moyens d&rsquo;éviter ça, c&rsquo;est d&rsquo;utiliser les hooks de git.

On peut « s&rsquo;accrocher » à un événement, et exécuter du code à ce moment. Git permet de le faire à peu près n&rsquo;importe quand : avant un commit, avant un push, après un checkout&#8230; La liste complète des possibilités est [dans la doc](http://git-scm.com/docs/githooks "Les différents hooks git").  
Pour cela, il suffit d&rsquo;ajouter un script shell dans le répertoire **.git/hooks** d&rsquo;un dépôt git. On peut d&rsquo;ailleurs y trouver quelques exemples (inactifs, il faut les renommer pour les « activer »).

Pour éviter de soumettre des fichiers à la syntaxe invalide, on peut donc écrire un hook pre-commit en creant le fichier **_pre-commit_** dans ce répertoire. Ce script s&rsquo;exécutera avant que le commit soit réalisé lorsque l&rsquo;on exécute la commande **_commit_**.

Voici son code :

<code lang="bash">#!/bin/sh&lt;br />
# On récupère la liste des fichiers modifiés&lt;br />
modifiedFiles=`git diff --cached --name-only --diff-filter=ACM`;&lt;br />
error=false;&lt;/p>
&lt;p>for file in $modifiedFiles; do&lt;br />
# On vérifie la syntaxe des fichiers PHP avec php -l&lt;br />
   if [[ $file =~ .*\.php ]]; then&lt;br />
      result=`php -l $file 2>&1`;&lt;br />
      if [[ $result =~ .*'Parse error'.* ]];&lt;br />
      then&lt;br />
         echo $file;&lt;br />
         echo $result;&lt;br />
         error=true;&lt;br />
      fi;&lt;br />
   fi;&lt;br />
done&lt;/p>
&lt;p>if [ $error != false ]; then&lt;br />
   # En cas d'erreur on empêche le commit&lt;br />
   echo "Erreur de syntaxe dans l'un des fichiers";&lt;br />
   exit 1;&lt;br />
fi;&lt;br />
</code>

Le code est simple et commenté, le comprendre ne devrait pas poser de problème (l&rsquo;écrire a demandé quelques coups de main à google ceci-dit. bash, quelle galère&#8230;). La vérification de syntaxe se fait avec **_php -l_**, le linter de PHP, en parsant le texte de sortie car il n&rsquo;y a pas de code de retour qui permette de déduire une erreur de syntaxe. En cas d&rsquo;erreur, on interrompt le **_commit_** et on affiche les fichiers à corriger. Simple et efficace.

On pourrait bien sûr faire d&rsquo;autre vérifications : validation de la **syntaxe des fichiers JavaScript** avec [jslint](https://github.com/reid/node-jslint "JSLint"), assurer le bon respect des **règles de codage** avec [PHPCS](https://github.com/squizlabs/PHP_CodeSniffer "PHPCS")&#8230;

Plus d&rsquo;informations sur les hooks dans [la documentation](http://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks "documentation des hooks git").