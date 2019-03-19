---
id: 143
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 7)
date: 2012-01-15T22:16:43+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=143
permalink: /2012/01/15/creez-votre-propre-framework-avec-les-composants-symfony2-partie-7/
keywords:
  - controleur, Refactoring, Symfony2
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - controleur
  - Refactoring
  - Symfony
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/56/create-your-own-framework-on-top-of-the-symfony2-components-part-7).

Un des inconvénients actuel de notre framework réside dans le fait qu&rsquo;il faut copier le code de front.php à chaque fois que l&rsquo;on veut créer un nouveau site web. 40 lignes de code ça n&rsquo;est pas grand chose, mais ça pourrait être sympa de pouvoir mettre ce code dans une classe dédiée. Cela nous apporterait une meilleure réutilisabilité et faciliterait les tests, pour ne citer que quelques bénéfices.

Si vous regardez de plus près le code, front.php a une entrée la Request, et une sortie, la Response. Notre classe de framework va suivre ce principe simple : la logique consiste à créer la réponse associée à une requête.

Comme les composants nécessitent PHP 5.3, créons notre propre espace de nom pour notre framework : Simplex.  
<!--more-->

  
Déplacez la logique de gestion des requêtes dans sa propre classe Simplex\\Framework :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/Framework.php

namespace Simplex;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Matcher\UrlMatcher;
use Symfony\Component\HttpKernel\Controller\ControllerResolver;

class Framework
{
	protected $matcher;
	protected $resolver;

	public function __construct(UrlMatcher $matcher, ControllerResolver $resolver)
	{
		$this->matcher = $matcher;&lt;br />
		$this->resolver = $resolver;&lt;br />
	}&lt;/p>
&lt;p>	public function handle(Request $request)&lt;br />
	{&lt;br />
		try {&lt;br />
			$request->attributes->add($this->matcher->match($request->getPathInfo()));&lt;/p>
&lt;p>			$controller = $this->resolver->getController($request);&lt;br />
			$arguments = $this->resolver->getArguments($request, $controller);&lt;/p>
&lt;p>			return call_user_func_array($controller, $arguments);&lt;br />
		} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
			return new Response('Not Found', 404);&lt;br />
		} catch (Exception $e) {&lt;br />
			return new Response('An error occurred', 500);&lt;br />
		}&lt;br />
	}&lt;br />
}&lt;br />
</code>

  
Mettez à jour example.com/web/front.php en conséquences :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

// ...

$request = Request::createFromGlobals();
$routes = include __DIR__.'/../src/app.php';

$context = new Routing\RequestContext();
$context->fromRequest($request);&lt;br />
$matcher = new Routing\Matcher\UrlMatcher($routes, $context);&lt;br />
$resolver = new HttpKernel\Controller\ControllerResolver();&lt;/p>
&lt;p>$framework = new Simplex\Framework($matcher, $resolver);&lt;br />
$response = $framework->handle($request);&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Pour continuer dans le refactoring, déplaçons tout sauf les définitions de routes de example.com/src/app.php vers encore un autre espace de nom : Calendar.

Pour que les classes définies dans les espaces de nom Simplex et Calendar soient chargées automatiquement, il faut mettre à jour le fichier composer.json :

<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*",&lt;br />
		"symfony/http-foundation": "2.1.*",&lt;br />
		"symfony/routing": "2.1.*",&lt;br />
		"symfony/http-kernel": "2.1.*"&lt;br />
	},&lt;br />
	"autoload": {&lt;br />
		"psr-0": { "Simplex": "src/", "Calendar": "src/" }&lt;br />
	}&lt;br />
}&lt;br />
</code>

Pour que l&rsquo;autoloader soit mis à jour, lancez la commande php composer.phar update.

Déplacez le contrôleur dans Calendar\\Controller\\LeapYearController :  
<code lang="php">&lt;br />
<?php

// example.com/src/Calendar/Controller/LeapYearController.php

namespace Calendar\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Calendar\Model\LeapYear;

class LeapYearController
{
	public function indexAction(Request $request, $year)
	{
		$leapyear = new LeapYear();
		if ($leapyear->isLeapYear($year)) {&lt;br />
			return new Response('Yep, this is a leap year!');&lt;br />
		}&lt;/p>
&lt;p>		return new Response('Nope, this is not a leap year.');&lt;br />
	}&lt;br />
}&lt;br />
</code>

Et déplacez la fonction is\_leap\_year() dans sa propre classe également :

<code lang="php">&lt;br />
<?php

// example.com/src/Calendar/Model/LeapYear.php

namespace Calendar\Model;

class LeapYear
{
	public function isLeapYear($year = null)
	{
		if (null === $year) {
			$year = date('Y');
		}

		return 0 == $year % 400 || (0 == $year % 4 &#038;&#038; 0 != $year % 100);
	}
}
</code>&lt;/p>
&lt;p>N'oubliez pas de mettre à jour le fichier example.com/src/app.php en conséquences :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />
$routes->add('leap_year', new Routing\Route('/is_leap_year/{year}', array(&lt;br />
        'year' => null,&lt;br />
        '_controller' => 'Calendar\\Controller\\LeapYearController::indexAction',&lt;br />
    )));&lt;br />
</code>

Pour résumer, voici la nouvelle architecture des fichiers :

`<br />
example.com<br />
    ├── composer.json<br />
    │   src<br />
    │   ├── app.php<br />
    │   └── Simplex<br />
    │       └── Framework.php<br />
    │   └── Calendar<br />
    │       └── Controller<br />
    │       │   └── LeapYearController.php<br />
    │       └── Model<br />
    │           └── LeapYear.php<br />
    ├── vendor<br />
    └── web<br />
        └── front.php<br />
` 

Ça y est ! Notre application a maintenant 4 couches différentes, et chacune d'entre elles a un but bien défini :

  * web/front.php : Le contrôleur de façade; le seul code PHP exposé, qui fait l'interface avec le client. Il récupère la Request et envoie la Response, et fournit le code nécessaire à l'initialisation du framework et de notre application;
  * src/Simplex : Le code réutilisable du framework qui abstrait la gestion des requêtes entrantes (au passage, il rend votre controlleur/template facilement testable -- bientôt plus de détails à ce sujet);
  * src/Calendar : Le code spécifique de notre application (contrôleur et modèle);
  * src/app.php : La configuration de l'application/la personnalisation du framework.