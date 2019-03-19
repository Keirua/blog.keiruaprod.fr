---
id: 437
title:
  - De bonnes bases avec Silex et HTML5Boilerplate
date: 2012-08-02T11:12:32+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=437
permalink: /2012/08/02/de-bonnes-bases-avec-silex-et-html5boilerplate/
keywords:
  - Silex, HTMLBoilelplate, framework
description:
  - Intro à Silex et HTML5Boilerplate
robotsmeta:
  - index,follow
categories:
  - Développement Web
tags:
  - Framework
  - HTMLBoilelplate
  - Silex
---
<div id="attachment_450" style="width: 210px" class="wp-caption alignright">
  <a href="http://silex.sensiolabs.org/"><img class=" wp-image-450  " title="logo-silex3" src="http://keiruaprod.fr/blog/wp-content/uploads/2012/08/logo-silex3.png" alt="Silex, micro framework PHP" width="200" height="150" /></a>
  
  <p class="wp-caption-text">
    Silex, un micro framework PHP
  </p>
</div>

Cela fait en effet un moment que j&rsquo;ai envie de réécrire ma page [KeiruaProd](www.keiruaprod.fr), afin qu&rsquo;elle soit conçue à partir d&rsquo;une base de code bien propre. Il n&rsquo;y a que quelques pages statiques à l&rsquo;heure actuelle, mais j&rsquo;ai 2-3 idées d&rsquo;évolutions dans les cartons, ce qui est une bonne occasion de repartir sur une base saine sur tous les plans (back et front).

Mes besoins sont simples :  
&#8211; du code propre, léger, maintenable, respectueux des standards  
&#8211; séparation front/back  
&#8211; apprendre, tester des outils  
&#8211; évolutivité

Ma recherche d&rsquo;outils adaptés s&rsquo;est arrêtée sur 2 outils : **[Silex](http://silex.sensiolabs.org/)** pour le PHP, et **[HTML5 Boilerplate](http://fr.html5boilerplate.com/)** pour le code front.

Ca va être l&rsquo;occasion de vous en parler !

<!--more-->

Je vous laisse regarder **[HTML5 Boilerplate](http://fr.html5boilerplate.com/)** si vous ne connaissez pas, mais comme ils le disent eux même « HTML5 Boilerplate est un template HTML/CSS/JS de tueurs pour développer des sites rapides, robustes et éprouvés pour le futur. » Il contient simplement une structure de code propre par dessus laquelle écrire du code multi-navigateurs devient plus simple. Aujourd&rsquo;hui, je vais principalement parler du back.

Concernant le back, pourquoi un framework, même minimal ? A vrai dire, à l&rsquo;heure actuelle, j&rsquo;ai au mieux besoin (et encore) d&rsquo;un moteur de templating pour être heureux. Mais je vais avoir besoin de coder 2-3 trucs, pour lesquels avoir un code un peu structuré et surtout testable est une bonne chose. A l&rsquo;heure actuelle, c&rsquo;est trop fouilli (les cordonniers sont les plus mal chaussés) pour que je puisse avancer sereinement. L&rsquo;argument « pour apprendre » est par contre dangereux, faites attention à ce que vous mettez en production 🙂

Maintenant, pourquoi celui là ? Ses fonctionnalités sont très intéressantes : templating, validation, formulaire, cache, securité, logging, traduction, ORM&#8230; Bref de quoi saliver, surtout quand on sait que le code est largement testé, d&rsquo;où une confiance accrue.

Voyons voir comment on s&rsquo;en sert !

## Installation

L&rsquo;installation de Silex est triviale, il suffit de remplir un fichier composer.json avec ce qui suit :  
<code lang="javascript">&lt;br />
{&lt;br />
    "minimum-stability": "dev",&lt;br />
    "require": {&lt;br />
        "silex/silex": "1.0.*",&lt;br />
		"twig/twig": ">=1.8,&lt;2.0-dev",
		"symfony/twig-bridge": "2.1.*",
		"monolog/monolog": ">=1.0.0"&lt;br />
    }&lt;br />
}&lt;br />
</code>  
On exécute [composer](http://getcomposer.org/download/) via  
<code lang="bash">&lt;br />
php composer.phar install&lt;br />
</code>  
Et quelques secondes plus tard, c&rsquo;est parti, on a un répertoire vendor avec tout ce dont on a besoin.

J&rsquo;ai inclus Twig (templating) et Monolog (logging) dans cet exemple, mais vous pouvez vous en passer.

Par la suite, lorsqu&rsquo;on ajoutera une extension, il suffira de lancer  
<code lang="bash">&lt;br />
php composer.phar update&lt;br />
</code>  
pour la récupérer.

## Architecture

Niveau architecture, j&rsquo;ai fait une architecture très proche de ce qui se fait chez Symfony, avec 3 répertoires à la racine : web, src, et app.

<code lang="bash">&lt;br />
web/&lt;br />
  index.php&lt;br />
app/&lt;br />
  bootstrap.php&lt;br />
src/&lt;br />
  app.php&lt;br />
</code>

Le répertoire web, c&rsquo;est celui qui est exposé. Un fichier .htaccess va rediriger toutes les requêtes vers le fichier index.php, qui fait office de contrôleur de facade. C&rsquo;est lui qui va rediriger les requêtes vers le bon contrôleur. Le fichier inclut bootstrap.php (qui référence a configuration de l&rsquo;application) et app.php (qui référence les contrôleurs).

Voici le contenu de notre index.php :  
<code lang="php">&lt;br />
<?php
// On charge les librairies
require_once __DIR__.'/../vendor/autoload.php';

// On crée l'application
$app = require __DIR__.'/../app/bootstrap.php';
// On charge les contrôleurs
require __DIR__.'/../src/app.php';

$app->run();&lt;br />
</code>

Pas bien lourd, hein ? C&rsquo;est pourtant ces 4 lignes qui vont faire tourner notre application.

Par la suite, le répertoire app/ contiendra par exemple les logs et les fichiers de mise en cache, là où le répertoire src contiendra le code métier (php et template).

## Configuration

Maintenant, la configuration de notre application, dans app/bootstrap.php :  
<code lang="php">&lt;br />
<?php
use Silex\Provider\MonologServiceProvider, 
	Silex\Provider\TwigServiceProvider;

$app = new Silex\Application();

$app->register(new MonologServiceProvider(), array(&lt;br />
    'monolog.logfile'       => __DIR__.'/log/app.log',&lt;br />
    'monolog.name'          => 'kp_app',&lt;br />
    'monolog.level'         => 300 // = Logger::WARNING&lt;br />
));&lt;/p>
&lt;p>$app->register(new TwigServiceProvider(), array(&lt;br />
    'twig.path'             => array(__DIR__ . '/../src/views')&lt;br />
));&lt;/p>
&lt;p>return $app;&lt;br />
</code>

On crée une application Silex, on enregistre les fonctionnalités dont on a besoin, et les configure. Ici, les noms d&rsquo;options parlent d&rsquo;eux même, mais vous pouvez trouver plus d&rsquo;informations sur les services disponibles et leurs options de configuration dans la [documentation](http://silex.sensiolabs.org/documentation).

## Code métier

Maintenant, il ne nous reste plus qu&rsquo;à créer des contrôleurs :  
<code lang="php">&lt;br />
// dans src/app.php&lt;br />
<?php 
use Symfony\Component\HttpFoundation\Response;

$app->match('/', function() use ($app) {&lt;br />
	return new Response ('Yeah !');&lt;br />
})->bind('kp_homepage');&lt;/p>
&lt;p>$app->match('/hello/{name}', function($name) use ($app) {&lt;br />
	return $app['twig']->render ('hello.html.twig', array('name' => $name));&lt;br />
})->bind('kp_hello');&lt;br />
</code>

On crée 2 contrôleurs, l&rsquo;un pour la route /, l&rsquo;autre pour /hello/clement par exemple. L&rsquo;une génère une réponse directement, l&rsquo;autre passe par un modèle twig très simple :  
<code lang="html">&lt;br />
# src/views/hello.html.twig&lt;br />
Hello {{ name }}&lt;br />
</code>

Il y a plein de manières de structurer ses contrôleurs : un fichier par contrôleur, une classe dédiée avec autoloading&#8230; Vu la taille de cet exemple, j&rsquo;ai créé mes 2 routes dans un seul fichier.

Et voila, on est prêt à avancer. On peut d&rsquo;ores et déjà se rendre sur les 2 routes qui ont été créées pour voir que tout marche comme il faut. Reste plus qu&rsquo;à ajouter des routes, écrire des vues&#8230; à coder l&rsquo;application quoi !

Si ça vous a plu et que vous voulez continuer avec Silex, après avoir regardé un peu la documentation, jetez un oeil à **[Silex Kitchen Edition](https://github.com/lyrixx/Silex-Kitchen-Edition)**. C&rsquo;est une version prête à l&#8217;emploi du framework qui va vous permettre d&rsquo;écrire directement vos fonctionnalités dans un environnement déjà bien configuré.