---
id: 79
title:
  - Créez votre propre framework... avec les composants Symfony2 (partie 1)
date: 2012-01-09T22:38:15+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=79
permalink: /2012/01/09/creez-votre-propre-framework-avec-les-composants-symfony2-partie-1/
keywords:
  - Framework, Symfony2
description:
  - Tutoriel sur les dessous des composants Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Framework
  - Symfony2
---
Cet article est la traduction d&rsquo;un article original de Fabien Potencier, à l&rsquo;origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/50/create-your-own-framework-on-top-of-the-symfony2-components-part-1).

Symfony2 propose un ensemble réutilisable, découplé et uni de composants PHP qui résolvent des problèmes courants de développement web.

Au lieu d&rsquo;utiliser ces composants bas niveau, vous pouvez utiliser directement Symfony2, le framework complet, prêt à l&#8217;emploi, qui est basé sur ces composants&#8230; ou bien vous pouvez créer votre propre framework. Cette série va parler de la seconde option.

Si vous voulez uniquement utiliser le framework Symfony2 complet, vous devriez plutôt lire la [documentation officielle](http://symfony.com/doc)  
NDT: Vous pouvez également utiliser la série d&rsquo;articles que j&rsquo;ai écrit sur le sujet: <http://keiruaprod.fr/symblog-fr><!--more-->

### Pourquoi créer son propre framework ?

Pourquoi vouloir créer son propre framework ? Si vous demandez autour de vous, tout le monde vous dira que c&rsquo;est une mauvaise chose de réinventer la roue, que vous feriez mieux de choisir un framework déjà existant et que vous devriez oublier l&rsquo;idée de créer le votre. La plupart du temps, ils ont raison mais il y a plusieurs bonnes raisons de commencer à créer le votre :

Pour en apprendre plus sur l&rsquo;architecture bas niveau des framework web modernes en général, et plus particulièrement sur le fonctionnement interne de Symfony2;

Pour avoir un framework sur mesure correspondant à vos besoins (soyez tout de même sûr que vos besoins sont bien spécifiques);

Pour expérimenter la création de framework pour le plaisir (une approche « j&rsquo;apprends et je jette »);

Pour refactorer une application vieille ou déjà existant qui a besoin d&rsquo;une bonne dose de bonnes pratiques de développement web modernes;

Pour prouver au monde que vous pouvez créer un framework par vous même (&#8230; mais sans trop d&rsquo;efforts).

Je vais donc vous guider à travers la création d&rsquo;un framework web, une étape à la fois. A chaque étape, vous aurez un framework en parfait état de fonctionnement, que vous pourrez utiliser tel quel ou comme point de départ pour le votre. Nous allons commencer avec des fonctionnalités simples, et avec le temps nous allons ajouter des fonctionnalités. A la fin, nous aurons un framework web complet.

Et bien sûr, chaque étape sera l&rsquo;occasion d&rsquo;en apprendre plus à propos de certains des composants de Symfony2.

Si vous n&rsquo;avez pas le temps de lire la série complète d&rsquo;articles, ou bien si vous vous commencer rapidement, vous pouvez également jeter un oeil à [Silex](http://silex.sensiolabs.org/), un micro-framework basé sur les composants de Symfony2. Le code est très court et aborde de nombreux aspects des composants de Symfony2.

Beaucoup de framework web modernes se considèrent comme ayant une architecture MVC. Nous ne parlerons pas de MVC ici, car les composants Symfony2 permettent de créer n&rsquo;importe quel type de framework, pas seulement ceux qui suivent une architecture MVC. Quoi qu&rsquo;il en soit, si l&rsquo;on regarde la sémantique MVC, cette série va aborder l&rsquo;aspect « Controlleur » d&rsquo;un framework. En ce qui concerne le modèle et la vue, celà dépend beaucoup de vos goûts personnels et je vais vous laisser utiliser n&rsquo;importe quelle librairie externe déjà existante (Doctrine, Propel, ou même simplement PDO pour le modèle; PHP ou Twig pour la vue par exemple).

Lorsque l&rsquo;on crée un framework, chercher à suivre le modèle MVC n&rsquo;est pas le bon objectif. Le bon objectif devrait être la Séparation des Tâches; je pense que c&rsquo;est le seul modèle de de conception dont vous devriez vous soucier. Le principe fondamental des composants Symfony2 sont centrés autour des spécifications HTTP. En tant que tel, les frameworks que nous allons créer devraient plutôt être considérés comme des framework HTTP, ou bien comme des framework requête/réponse.

### Avant de commencer

Lire sur comment créer un framework ne suffit pas. Vous allez devoir réaliser et taper tous les exemples sur lesquels nous allons travailler. Pour cela, il vous faut une version récente de PHP (la version 5.3.8 ou supérieure suffit), un serveur web (comme Apache ou NGinx), une bonne connaissance de PHP et connaitre la programmation orientée objet.

Prêt ? Allons-y.

### Bootstrapping

Avant que nous puissions ne serait-ce que penser à créer notre premier framework, nous devons parler de certaines conventions: où nous allons ranger notre code, comment nommer nos classes, commenent référencer les dépendances externes, etc.

Pour stocker notre framework, créez un répertoire quelquepart sur votre machine :

<code lang="bash">&lt;br />
$ mkdir framework&lt;br />
$ cd framework&lt;br />
</code>

### Standards de codage

Avant que le débat sur les standards de codage ne soit lancé et sur pourquoi celui utilisé ici est vraiment naze, commençons par admettre que cela n&rsquo;a pas d&rsquo;importance tant que nous sommes consistants. Pour cette série d&rsquo;articles, nous allons utiliser les standards de codage de Symfony2 (http://symfony.com/doc/current/contributing/code/standards.html)

### Installation des composants

Pour installer les composantes Symfony2 dont nous avons besoin pour notre framework, nous allons utiliser Composer, un gestionnaire de dépendances pour PHP. TOut d&rsquo;abord, listez vos dépendances dans un fichier composer.json :

<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*"&lt;br />
	}&lt;br />
}&lt;br />
</code>

Ici, on dit à Composer que notre projet va utiliser le composant Symfony2 ClassLoader, version 2.1.0 ou supérieure. Pour installer les dépendances du projet, téléchargez les exécutables de composer et lancez le :

<code lang="bash">&lt;br />
$ wget http://getcomposer.org/composer.phar&lt;br />
$ # or&lt;br />
$ curl -O http://getcomposer.org/composer.phar&lt;br />
</code>

<code lang="bash">$ php composer.phar install</code>

Après avoir lancé la commande d&rsquo;installation, vous devez voir un nouveau répertoire vendor qui doit contenir le code du ClassLoader de Symfony2.

Même si nous vous recommandons fortement d&rsquo;utiliser Composer, vous pouvez également télécharger l&rsquo;archive des composantes directement ou utiliser les sous-modules de Git. Le choix dépend vraiment de vous.

### Conventions de nommage et chargement automatique

Nous allons charger automatiquement toutes nos classes via [autoloading](http://fr.php.net/autoload). Sans autoloading, il faut inclure les fichiers de déclaration d&rsquo;une classe avant qu&rsquo;elle puisse être utilisée. Mais à l&rsquo;aide de quelques conventions, nous pouvons laisser PHP le faire pour nous.

Symfony2 suit le standant de-facto de PHP, [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md), pour les noms de classes et le chargement automatique. Le composant ClassLoader de Symfony2 propose un autoloader qui implémente le standard PSR-0 et, la plupart du temps, c&rsquo;est l&rsquo;unique composant dont vous avez besoin pour charger toutes les classes de votre projet.

Créez un autoloader vide dans un nouveau fichier autoload.php :

<code lang="php">&lt;br />
<?php

// framework/autoload.php

require_once __DIR__.'/vendor/symfony/class-loader/Symfony/Component/ClassLoader/UniversalClassLoader.php';

use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$loader->register();&lt;br />
</code>

  
Vous pouvez maintenant lancer autoload.php dans la ligne de commande. Il ne devrait rien se passer, mais il ne devrait pas y avoir d&rsquo;erreurs :

`$ php autoload.php`

Le site de Symfony2 a plus d&rsquo;informations sur le composant [ClassLoader](http://symfony.com/doc/current/components/class_loader.html).

Composer crée automatique un autoloader pour toutes les dépendances installées. Au lieu d&rsquo;utiliser le composant ClassLoader, vous pouvez également vous contenter d&rsquo;utiliser vendor/.composer/autoload.php.

### Notre projet

Au lieau de créer notre framework de zéro, nous allons écrire la même application encore et encore, en ajoutant à chaque fois un peu plus d&rsquo;abstraction. Commençons par la plus simple application web possible en PHP:

<code lang="php"><?php

$input = $_GET['name'];

printf('Hello %s', $input);
</code><br />
C'est tout pour la première partie de cette série. La prochaine fois, nous allons parler du composant HttpFoundation et regarder ce qu'il nous apporte.</p>