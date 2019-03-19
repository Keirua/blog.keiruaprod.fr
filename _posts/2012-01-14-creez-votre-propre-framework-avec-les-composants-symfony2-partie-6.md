---
id: 136
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 6)
date: 2012-01-14T11:35:01+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=136
permalink: /2012/01/14/creez-votre-propre-framework-avec-les-composants-symfony2-partie-6/
keywords:
  - controleur, Framework, HttpKernel, Symfony2
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - controleur
  - Framework
  - HttpKernel
  - Symfony2
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/55/create-your-own-framework-on-top-of-the-symfony2-components-part-6).

Vous pensez peut être que notre framework est déjà plutôt solide et vous avez probablement raison. Mais regardons quand même comment nous pouvons l&rsquo;améliorer.

Actuellement, tous nos exemples utilisent du code procédural, mais souvenez vous que les contrôleurs peuvent être n&rsquo;importe quel callback PHP valide. Convertissons notre contrôleur pour utiliser une classe dédiée :

<code lang="php">&lt;br />
class LeapYearController&lt;br />
{&lt;br />
	public function indexAction($request)&lt;br />
	{&lt;br />
		if (is_leap_year($request->attributes->get('year'))) {&lt;br />
			return new Response('Yep, this is a leap year!');&lt;br />
		}&lt;/p>
&lt;p>		return new Response('Nope, this is not a leap year.');&lt;br />
	}&lt;br />
}&lt;br />
</code>  
<!--more-->

  
Mettez à jour la définition de la route en conséquences :

<code lang="php">&lt;br />
$routes->add('leap_year', new Routing\Route('/is_leap_year/{year}', array(&lt;br />
        'year' => null,&lt;br />
        '_controller' => array(new LeapYearController(), 'indexAction'),&lt;br />
    )));&lt;br />
</code>

La manipulation est plutôt simple et a du sens à partir du moment où l&rsquo;on commence à créer plusieurs pages, mais vous avez sûrement remarqué un effet secondaire indésirable&#8230; la classe LeapYearController est toujours instanciée, même si l&rsquo;URL demandé ne correspond par à la route leap_year. C&rsquo;est pas terrible pour un aspect important : du point de vue performances, tous les contrôleurs de toutes les routes sont instanciés pour toutes les requêtes. Ce serait mieux si les contrôleurs étaient chargés uniquement lorsque c&rsquo;est nécessaire, afin que seul le contrôleur associé à la route soit instancié.

Pour résoudre ce problème ainsi que plusieurs autres, installons et utilisons le composant HttpKernel :  
<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*",&lt;br />
		"symfony/http-foundation": "2.1.*",&lt;br />
		"symfony/routing": "2.1.*",&lt;br />
		"symfony/http-kernel": "2.1.*"&lt;br />
	}&lt;br />
}&lt;br />
</code>

Le composant HttpKernel a plutôt fonctionnalités intéressantes, mais celle dont nous avons besoin maintenant, c&rsquo;est le résolveur de contrôleur. Un résolveur de contrôleur sait comment déterminer le contrôleur à exécuter et les arguments à lui fournir à partir d&rsquo;un objet Request. Tous les résolveurs de contrôleurs implémentent l&rsquo;interface suivante :

<code lang="php">&lt;br />
namespace Symfony\Component\HttpKernel\Controller;&lt;/p>
&lt;p>interface ControllerResolverInterface&lt;br />
{&lt;br />
	function getController(Request $request);&lt;/p>
&lt;p>	function getArguments(Request $request, $controller);&lt;br />
}&lt;br />
</code>

La méthode getController() utilise les mêmes conventions que celles définies plus tôt. L&rsquo;attribut de requête _controller doit contenir le contrôleur associé à la requête. En plus du système de callback PHP, getController() supporte également des chaines composées du nom d&rsquo;une classe suivi par 2 « : » ainsi qu&rsquo;un nom de méthode, tel que « class::method » :

<code lang="php">&lt;br />
$routes->add('leap_year', new Routing\Route('/is_leap_year/{year}', array(&lt;br />
        'year' => null,&lt;br />
        '_controller' => 'LeapYearController::indexAction',&lt;br />
    )));&lt;br />
</code>

Pour que ce code marche, modifiez le code du framework pour utiliser le résolveur de contrôleurs du composant HttpKernel :

<code lang="php">&lt;br />
use Symfony\Component\HttpKernel;&lt;/p>
&lt;p>$resolver = new HttpKernel\Controller\ControllerResolver();&lt;/p>
&lt;p>$controller = $resolver->getController($request);&lt;br />
$arguments = $resolver->getArguments($request, $controller);&lt;/p>
&lt;p>$response = call_user_func_array($controller, $arguments);&lt;br />
</code>

Bonus supplémentaire, le résolveur de contrôleurs gère correctement les erreurs pour vous : lorsque vous oubliez de définir un attribut _controller pour une route par exemple.

Maintenant, regardons comment les arguments du contrôleur sont devinés. getArguments() fait de l&rsquo;introspection sur la signature du contrôleur pour déterminer quels arguments lui fournir en utilisant la [réflection](http://php.net/reflection) native de PHP.

La méthode indexAction() a besoin de l&rsquo;objet Request en argument. getArguments() sait quand l&rsquo;injecter si le type est correctement suggéré :

<code lang="php">&lt;br />
public function indexAction(Request $request)&lt;/p>
&lt;p>// Ne marchera pas&lt;br />
public function indexAction($request)&lt;br />
</code>

Plus intéressant, getArguments() est également capable d&rsquo;injecter n&rsquo;importe quel attribut de requête; l&rsquo;argument doit simplement avoir le même nom que l&rsquo;attribut correspondant :

<code lang="php">public function indexAction($year)</code>

Vous pouvez également injecter l&rsquo;objet Request et certains attributs en même temps (car l&rsquo;association est faite à partir des noms de paramètres ou des types proposés, leur ordre n&rsquo;a pas d&rsquo;importance) :

<code lang="php">&lt;br />
public function indexAction(Request $request, $year)&lt;/p>
&lt;p>public function indexAction($year, Request $request)&lt;br />
</code>

Enfin, vous pouvez également définir des valeurs par défaut pour les arguments qui correspondent à un attribut optionnel de la requête :  
<code lang="php">public function indexAction($year = 2012)</code>

Contentons nous d&rsquo;injecter l&rsquo;attribut de requête $year dans notre contrôleur :

<code lang="php">&lt;br />
class LeapYearController&lt;br />
{&lt;br />
	public function indexAction($year)&lt;br />
	{&lt;br />
		if (is_leap_year($year)) {&lt;br />
			return new Response('Yep, this is a leap year!');&lt;br />
		}&lt;/p>
&lt;p>		return new Response('Nope, this is not a leap year.');&lt;br />
	}&lt;br />
}&lt;br />
</code>

Le résolveur de contrôleur se charge également de valider la méthode à appeler et ses arguments. En cas de problème, il lance une exception avec un message sympa expliquant le problème (la classe de contrôleur n&rsquo;existe pas, la méthode n&rsquo;est pas définie, une argument n&rsquo;a pas d&rsquo;attributs associés&#8230;).

Avec la grande flexibilité du résolveur de contrôleur par défaut, vous vous demandez peut être pourquoi on pourrait vouloir en implémenter un autre (Pourquoi y aurait-il une interface si ce n&rsquo;était pas le cas ?). 2 exemples : dans Symfony2, getController() est amélioré pour supporter les [« contrôleurs comme des services »](http://symfony.com/doc/current/cookbook/controller/service.html).  
Dans [FrameworkExtraBundle](http://symfony.com/doc/current/bundles/SensioFrameworkExtraBundle/annotations/converters.html), getArguments() est amélioré pour supporter les convertisseurs de paramètres, où les attributs de requêtes sont directement convertis en objets.

Concluons avec la nouvelle version de notre framework :  
<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing;
use Symfony\Component\HttpKernel;

function render_template($request)
{
	extract($request->attributes->all());&lt;br />
	ob_start();&lt;br />
	include sprintf(__DIR__.'/../src/pages/%s.php', $_route);&lt;/p>
&lt;p>	return new Response(ob_get_clean());&lt;br />
}&lt;/p>
&lt;p>$request = Request::createFromGlobals();&lt;br />
$routes = include __DIR__.'/../src/app.php';&lt;/p>
&lt;p>$context = new Routing\RequestContext();&lt;br />
$context->fromRequest($request);&lt;br />
$matcher = new Routing\Matcher\UrlMatcher($routes, $context);&lt;br />
$resolver = new HttpKernel\Controller\ControllerResolver();&lt;/p>
&lt;p>try {&lt;br />
	$request->attributes->add($matcher->match($request->getPathInfo()));&lt;/p>
&lt;p>	$controller = $resolver->getController($request);&lt;br />
	$arguments = $resolver->getArguments($request, $controller);&lt;/p>
&lt;p>	$response = call_user_func_array($controller, $arguments);&lt;br />
} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
} catch (Exception $e) {&lt;br />
	$response = new Response('An error occurred', 500);&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Repensez-y encore une fois : notre framework n&rsquo;a jamais été aussi robuste et flexible, et il fait pourtant toujours moins de 40 lignes de code.