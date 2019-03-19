---
id: 336
title:
  - Bien utiliser les commandes console de Symfony2
date: 2012-03-21T18:21:24+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=336
permalink: /2012/03/21/bien-utiliser-les-commandes-console-de-symfony2/
keywords:
  - Symfony2, console, commandes
description:
  - Description des commandes les plus utiles de la console Symfony2.
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Console
  - Symfony2
---
La console Symfony2. J&rsquo;ai écrit un article sur [comment écrire ses propres commandes](http://keiruaprod.fr/blog/2012/02/28/ecrire-une-commande-console-pour-symfony2/), mais rien sur comment bien se servir de celles qui existent déjà ! Le but de cet article est donc remédier à cela, en faisant un tour d&rsquo;horizon des commandes disponibles de base, et de ce qu&rsquo;elles permettent de faire.

Commencez par lancer une terminal, et placez-vous à la racine d&rsquo;un projet Symfony2.

<code lang="bash">&lt;br />
php app/console&lt;br />
</code>  
S&rsquo;il y a une chose à retenir de cet article, c&rsquo;est cette commande. Elle liste toutes les commandes consoles disponibles, ce qui permet de ne pas avoir à retenir la syntaxe de toutes celles dont je vais vous parler par la suite. Si vous retenez cette commande et que vous savez ce qu&rsquo;il est possible de faire, vous pouvez ensuite retrouver la commande correspondante dans la liste.  
<!--more-->

  
Autre information qui va vous servir, si une commande est bien écrite, normalement le modifieur &#8211;help permet d&rsquo;accéder aux informations d&rsquo;aide, ce qui permet de se rappeller de comment on utilise une commande.

exemple:  
<code lang="bash">&lt;br />
php app/console doctrine:generate:entity --help&lt;br />
</code>

### Commandes utiles lors de la création d&rsquo;une application

<code lang="bash">&lt;br />
php app/console generate:bundle&lt;br />
</code>  
C&rsquo;est probablement la première commande que vous avez utilisée ! Tapez là, et laissez vous guider pour créer le bundle dans lequel vous allez écrire le code de votre projet. Utilisez les modifieurs décrits dans l&rsquo;aide si vous voulez gagner un peu de temps.

<code lang="bash">&lt;br />
php app/console doctrine:database:create&lt;br />
php app/console doctrine:database:drop&lt;br />
</code>  
Ces 2 commandes créent et suppriment la base de données utilisée par l&rsquo;application. Les informations de configuration sur la base de données sont précisées dans le fichier app/config/config.yml (dans la section Doctrine/dbal si vous utilisez Doctrine).

### Commandes de génération de code

En s&rsquo;en servant bien, elles peuvent un peu accélérer le développement et réduire le temps passé dans la documentation.  
<code lang="bash">&lt;br />
php app/console doctrine:generate:entity&lt;br />
</code>  
Editeur en ligne de commande pour créer une entité et ses attributs : tapez cette commande et laissez vous guider. Très pratique pour éviter de retenir la syntaxe des annotations ou de la configuration en yml, mais également très limité. Pour faire des choses à peine avancées (ajouter des contraintes sur un attribut par exemple), vous devrez mettre les mains dans le cambouis (ce qui ne vous empeche pas de générer votre entité de manière basique par cette méthode, puis faire les modifications qui restent par vous même).

<code lang="bash">&lt;br />
php app/console doctrine:generate:entities NomDuBundle&lt;br />
</code>  
A partir des entités, finalise leur conception en génèrant les accesseurs (méthodes get/set). Par la suite, ces méthodes sont utilisées par le repository par défaut de l&rsquo;entité (entre autres).

<code lang="bash">&lt;br />
php app/console generate:doctrine:form NomDuBundle:Entité&lt;br />
</code>  
Génère le code d&rsquo;un formulaire par défaut associé à l&rsquo;entité fournie en paramètre. Il ne faut pas qu&rsquo;il y ait de formulaire déjà existant pour cette entité, mais ça permet de gagner un peu de temps.

<code lang="bash">&lt;br />
php app/console generate:doctrine:crud NomDuBundle:Entité&lt;br />
</code>  
Génère quelques pages basiques de CRUD (Create, Read, Update, Delete) pour l&rsquo;entité présentée. Cela crée les controlleurs, les routes et les template. C&rsquo;est pas mal pour apprendre un peu comment marche Symfony, mais en pratique sert vraiment très peu.

### Commandes aide-mémoire

Des commandes qui vont vous permettre d&rsquo;éviter d&rsquo;aller fouiller dans les fichiers de configuration&#8230;  
<code lang="bash">&lt;br />
php app/console router:debug&lt;br />
php app/console router:debug NomDUneRoute&lt;br />
</code>  
Permet de lister toutes les routes accessibles depuis l&rsquo;application. C&rsquo;est particulièrement utile lorsque l&rsquo;on installe un nouveau bundle et que l&rsquo;on veut surveiller quelles sont les routes qui ont été ajoutées. Egalement très utile lorsque l&rsquo;on a plus en tête toutes les routes qui ont été crées lors du développement.  
Si vous précisez en argument une route, il vous fournit les informations de configuration associées à la route en question (url associée, controlleur utilisé, etc.)

<code lang="bash">&lt;br />
php app/console container:debug&lt;br />
php app/console container:debug NomDUnService&lt;br />
</code>  
De la même manière que précédemment, permet de connaitre les services déclarés dans l&rsquo;application, et d&rsquo;avoir des informations sur un service en particulier. Les services servent pas mal une fois qu&rsquo;on commence à connaitre un peu comment fonctionne le framework, donc si vous ne vous en servez pas aujourd&rsquo;hui, cela vous servira sans doute demain.

### Commandes utilitaires

Ne les oubliez pas ! Vous utilisez sans doute déjà la première, en cas de souci pensez à la seconde.  
<code lang="bash">&lt;br />
php app/console assets:install web&lt;br />
</code>  
Permet de copier les ressource publiques de tous les bundles installés (situées dans NomDuBundle/Resources/public) dans le répertoire web, où elles seront accessibles publiquement. En français, ça veut dire rendre accessible à tous les ressources de développement que vous utilisez. Si votre bundle utilisedes fichiers javascript, css ou des images, il est en général nécessaire d&rsquo;utiliser cette commande pour les dupliquer dans une répertoire accessible publiquement (le répertoire web, le plus souvent).

<code lang="bash">&lt;br />
php app/console cache:clear&lt;br />
php app/console cache:clear --env=prod&lt;br />
</code>  
La première commande vide le cache, la seconde vide spécifiquement le cache de l&rsquo;environnement de production.  
Sur le serveur de production, cette commande est indispensable lors d&rsquo;un déploiement: cela permet d&rsquo;éviter que des modifications ne soient pas prises en compte à cause d&rsquo;infos présentes dans le cache.  
En développement, ca peut être une piste si ce que vous essayez de faire n&rsquo;est pas pris en compte alors que tout indique que cela devrait.

Il en existe d&rsquo;autres, mais celles ci-dessus servent assez souvent. Lorsque vous installez un bundle (que vous avez par exemple trouvé sur [KnpBundles](http://knpbundles.com/) ou au hasard de vos errances sur [Github](https://github.com/)), il n&rsquo;est pas rare que ce dernier ajoute de nouvelles commandes, renseignez vous sur ce qu&rsquo;elles permettent de faire : celà peut vous faire gagner beaucoup de temps. Et si ce que votre bundle peut être automatisé, n&rsquo;hésitez pas à écrire une commande pour le faire !