---
id: 129
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 5)
date: 2012-01-13T18:14:36+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=129
permalink: /2012/01/13/creez-votre-propre-framework-avec-les-composants-symfony2-partie-5/
archived: true
keywords:
  - controleur, Request, Response, Routing, Symfony2
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - controleur
  - Request
  - Response
  - Routing
  - Symfony2
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/54/create-your-own-framework-on-top-of-the-symfony2-components-part-5).

L&rsquo;élève attentif aura remarqué que notre framework code en dur la manière dont le « code » spécifique (celui des templates) est lancé. Pour des pages simples comme celles que nous avons créées pour le moment, pas de problèmes, mais si vous voulez ajouter plus de logique, vous serez forcés de mettre la logique dans un template lui même, ce qui n&rsquo;est probablement pas une bonne idée, en particulier si vous avez toujours en tête l&rsquo;idée de séparation des responsabilités.

Séparons le code de template de la logique en ajoutant une nouvelle couche : le controleur. La mission du controleur est de générer une réponse à partir des informations fournies par la requête.

Changez la partie de rendu des templates du framework de la manière suivante :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

// ...

try {
	$request->attributes->add($matcher->match($request->getPathInfo()));&lt;br />
	$response = call_user_func('render_template', $request);&lt;br />
} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
} catch (Exception $e) {&lt;br />
	$response = new Response('An error occurred', 500);&lt;br />
}&lt;br />
</code>

  
<!--more-->

  
Comme le rendu est désormais réalisé par une fonction externe (render\_template() ici), nous devons lui fournir les attributs extraits de l&rsquo;URL. Nous aurions pu les fournir comme argument à render\_template, mais à la place, utilisons une autre fonctionnalité de la classe Request, les attributs. Les attributs de requête vous permettent de lier des informations additionnelles sur la requête qui ne sont pas directement liées aux données de la requête HTTP.

Vous pouvez maintenant créer la fonction render_template(), un controleur générique qui effectue le rendu d&rsquo;un template où il n&rsquo;y a pas de logique spécifique. Pour garder le même modèle qu&rsquo;avant, les attributs de requête sont extraits avant le rendu du template :

<code lang="php">&lt;br />
function render_template($request)&lt;br />
{&lt;br />
	extract($request->attributes->all(), EXTR_SKIP);&lt;br />
	ob_start();&lt;br />
	include sprintf(__DIR__.'/../src/pages/%s.php', $_route);&lt;/p>
&lt;p>	return new Response(ob_get_clean());&lt;br />
}&lt;br />
</code>

Comme render\_template est utilisée en argument à la fonction PHP call\_user_func(), nous pouvons la remplacer par n&rsquo;importe quel [callback PHP](http://php.net/callback#language.types.callback) valide. Cela nous permet d&rsquo;utiliser une fonction, une fonction anonyme ou la méthode d&rsquo;une classe comme controleur&#8230; à vous de choisir.

Comme convention, pour chaque route, le controleur associé est configuré via l&rsquo;attribut de route _controller :

<code lang="php">&lt;br />
$routes->add('hello', new Routing\Route('/hello/{name}', array(&lt;br />
	'name' => 'World',&lt;br />
	'_controller' => 'render_template',&lt;br />
)));&lt;/p>
&lt;p>try {&lt;br />
	$request->attributes->add($matcher->match($request->getPathInfo()));&lt;br />
	$response = call_user_func($request->attributes->get('_controller'), $request);&lt;br />
} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
} catch (Exception $e) {&lt;br />
	$response = new Response('An error occurred', 500);&lt;br />
}&lt;br />
</code>

Une route peut maintenant être associée à un controleur et, bien sûr, à l&rsquo;intérieur d&rsquo;un controleur, vous pouvez toujours appeler render_template pour afficher un template :

<code lang="php">&lt;br />
$routes->add('hello', new Routing\Route('/hello/{name}', array(&lt;br />
	'name' => 'World',&lt;br />
	'_controller' => function ($request) {&lt;br />
		return render_template($request);&lt;br />
	}&lt;br />
)));&lt;br />
</code>

C&rsquo;est plutôt flexible, car vous pouvez changer l&rsquo;objet Response par la suite et on peut même fournir des arguments supplémentaires au template :

<code lang="php">&lt;br />
$routes->add('hello', new Routing\Route('/hello/{name}', array(&lt;br />
	'name' => 'World',&lt;br />
	'_controller' => function ($request) {&lt;br />
		// $foo will be available in the template&lt;br />
		$request->attributes->set('foo', 'bar');&lt;/p>
&lt;p>		$response = render_template($request);&lt;/p>
&lt;p>		// change some header&lt;br />
		$response->headers->set('Content-Type', 'text/plain');&lt;/p>
&lt;p>		return $response;&lt;br />
	}&lt;br />
)));&lt;br />
</code>

Voici la version mise à jour et améliorée de notre framework :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing;

function render_template($request)
{
	extract($request->attributes->all(), EXTR_SKIP);&lt;br />
	ob_start();&lt;br />
	include sprintf(__DIR__.'/../src/pages/%s.php', $_route);&lt;/p>
&lt;p>	return new Response(ob_get_clean());&lt;br />
}&lt;/p>
&lt;p>$request = Request::createFromGlobals();&lt;br />
$routes = include __DIR__.'/../src/app.php';&lt;/p>
&lt;p>$context = new Routing\RequestContext();&lt;br />
$context->fromRequest($request);&lt;br />
$matcher = new Routing\Matcher\UrlMatcher($routes, $context);&lt;/p>
&lt;p>try {&lt;br />
	$request->attributes->add($matcher->match($request->getPathInfo()));&lt;br />
	$response = call_user_func($request->attributes->get('_controller'), $request);&lt;br />
} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
} catch (Exception $e) {&lt;br />
	$response = new Response('An error occurred', 500);&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Pour fêter la naissance de notre nouveau framework, créons une toute nouvelle application qui a besoin d&rsquo;un peu de logique simple. Notre application a une page qui dit si une année donnée est bissextile ou non. Lorsqu&rsquo;on appelle /is\_leap\_year, on a la réponse pour l&rsquo;année en cours, mais on peut également spécifier l&rsquo;année via /is\_leap\_year/2009« . Etant générique, le framework n&rsquo;a pas besoin d&rsquo;être modifié, il suffit de créer un nouveau fichier app.php :

<code lang="php">&lt;br />
<?php

// example.com/src/app.php

use Symfony\Component\Routing;
use Symfony\Component\HttpFoundation\Response;

function is_leap_year($year = null) {
	if (null === $year) {
		$year = date('Y');
	}

	return 0 == $year % 400 || (0 == $year % 4 &#038;&#038; 0 != $year % 100);
}

$routes = new Routing\RouteCollection();
$routes->add('leap_year', new Routing\Route('/is_leap_year/{year}', array(&lt;br />
	'year' => null,&lt;br />
	'_controller' => function ($request) {&lt;br />
		if (is_leap_year($request->attributes->get('year'))) {&lt;br />
			return new Response('Yep, this is a leap year!');&lt;br />
		}&lt;/p>
&lt;p>		return new Response('Nope, this is not a leap year.');&lt;br />
	}&lt;br />
)));&lt;/p>
&lt;p>return $routes;&lt;br />
</code>

La fonction is\_leap\_year renvoit true lorsque l&rsquo;année est bissextile, et false sinon. Si l&rsquo;année vaut null, c&rsquo;est l&rsquo;année en cours qui est testée. Le controleur est simple : il récupère l&rsquo;année à partir des attributs de la requête, et fournit cette information à la fonction is\_leap\_year(), et en fonction de la valeur de retour un objet Response est créé.

Comme toujours, vous pouvez décider de vous arrêter là et utiliser le framework tel quel; c&rsquo;est probablement tout ce dont vous avez besoin pour créer des sites web simple comme [ces sites sympa](http://kottke.org/08/02/single-serving-sites) en une page, et, espérons-le, pour quelques autres.