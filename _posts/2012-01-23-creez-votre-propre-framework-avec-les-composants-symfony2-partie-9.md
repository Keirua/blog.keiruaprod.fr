---
id: 226
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 9)
date: 2012-01-23T20:29:44+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=226
permalink: /2012/01/23/creez-votre-propre-framework-avec-les-composants-symfony2-partie-9/
keywords:
  - Design pattern, Framework, Observer, Symfony2
description:
  - Tutoriel sur les dessous des composants Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Design pattern
  - Framework
  - Observer
  - Symfony2
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/58/create-your-own-framework-on-top-of-the-symfony2-components-part-9).

Actuellement, il manque à notre framework une caractéristique essentielle à tout bon framework : **l&rsquo;extensibilité**. Être extensible signifie que le développeur doit pouvoir facilement s&rsquo;intégrer dans le cycle de vie du framework pour modifier la manière dont les requêtes sont gérées.

De quel genre d&rsquo;intégration parlons nous ? D’authentification ou de système de cache par exemple. Pour être flexible, il faut que le développeur puise s&rsquo;intégrer de manière plug-and-play. Beaucoup d&rsquo;applications appliquent des concepts similaires, tel que WordPress ou Drupal. Dans certains langages, il y a même des standards tel que [WSGI](http://www.python.org/dev/peps/pep-0333/#middleware-components-that-play-both-sides) en Python ou [Rack](http://rack.rubyforge.org/) en Ruby.  
<!--more-->

  
Comme il n&rsquo;y a pas de standard en PHP, nous allons utiliser un design pattern bien connu, **Observer**, pour permettre d&rsquo;attacher n&rsquo;importe quel type de comportement à notre framework. Le composant EventDispatcher de Symfony2 implémente une version légère de ce patron de conception :

<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*",&lt;br />
		"symfony/http-foundation": "2.1.*",&lt;br />
		"symfony/routing": "2.1.*",&lt;br />
		"symfony/http-kernel": "2.1.*",&lt;br />
		"symfony/event-dispatcher": "2.1.*"&lt;br />
	},&lt;br />
	"autoload": {&lt;br />
		"psr-0": { "Simplex": "src/", "Calendar": "src/" }&lt;br />
	}&lt;br />
}&lt;br />
</code>

Comment ça marche ? Le **dispatcher**, objet central du système de répartition des évènements, notifie des **écouteurs** (listeners) qu&rsquo;un évènement a été transmis. Dit d&rsquo;une autre manière : votre code fournit un évènement au dispatcher, le dispatcher prévient tous ceux qui écoutent cet évènement, et les écouteurs font ce qu&rsquo;ils souhaitent de l&rsquo;évènement.

Comme exemple, créons un écouteur qui va, de manière transparente, ajouter le code de Google  
Analytics code à toutes les réponses.

Pour que cela marche, le framework doit transmettre un évènement juste avant de renvoyer l&rsquo;instance de la réponse :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/Framework.php

namespace Simplex;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Matcher\UrlMatcherInterface;
use Symfony\Component\Routing\Exception\ResourceNotFoundException;
use Symfony\Component\HttpKernel\Controller\ControllerResolverInterface;
use Symfony\Component\EventDispatcher\EventDispatcher;

class Framework
{
	protected $matcher;
	protected $resolver;
	protected $dispatcher;

	public function __construct(EventDispatcher $dispatcher, UrlMatcherInterface $matcher, ControllerResolverInterface $resolver)
	{
		$this->matcher = $matcher;&lt;br />
		$this->resolver = $resolver;&lt;br />
		$this->dispatcher = $dispatcher;&lt;br />
	}&lt;/p>
&lt;p>	public function handle(Request $request)&lt;br />
	{&lt;br />
		try {&lt;br />
			$request->attributes->add($this->matcher->match($request->getPathInfo()));&lt;/p>
&lt;p>			$controller = $this->resolver->getController($request);&lt;br />
			$arguments = $this->resolver->getArguments($request, $controller);&lt;/p>
&lt;p>			$response = call_user_func_array($controller, $arguments);&lt;br />
		} catch (ResourceNotFoundException $e) {&lt;br />
			$response = new Response('Not Found', 404);&lt;br />
		} catch (\Exception $e) {&lt;br />
			$response = new Response('An error occurred', 500);&lt;br />
		}&lt;/p>
&lt;p>		// dispatch a response event&lt;br />
		$this->dispatcher->dispatch('response', new ResponseEvent($response, $request));&lt;/p>
&lt;p>		return $response;&lt;br />
	}&lt;br />
}&lt;br />
</code>

A chaque fois que le framework gère une requête, un évènement **ResponseEvent** est envoyé :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/ResponseEvent.php

namespace Simplex;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\EventDispatcher\Event;

class ResponseEvent extends Event
{
	private $request;
	private $response;

	public function __construct(Response $response, Request $request)
	{
		$this->response = $response;&lt;br />
		$this->request = $request;&lt;br />
	}&lt;/p>
&lt;p>	public function getResponse()&lt;br />
	{&lt;br />
		return $this->response;&lt;br />
	}&lt;/p>
&lt;p>	public function getRequest()&lt;br />
	{&lt;br />
		return $this->request;&lt;br />
	}&lt;br />
}&lt;br />
</code>

La dernière étape de la création du dispatcher dans le contrôleur de façade, c&rsquo;est de faire écouter l&rsquo;évènement **response** par un listener :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

// ...

use Symfony\Component\EventDispatcher\EventDispatcher;

$dispatcher = new EventDispatcher();
$dispatcher->addListener('response', function (Simplex\ResponseEvent $event) {&lt;br />
	$response = $event->getResponse();&lt;/p>
&lt;p>	if ($response->isRedirection()&lt;br />
		|| ($response->headers->has('Content-Type') && false === strpos($response->headers->get('Content-Type'), 'html'))&lt;br />
		|| 'html' !== $event->getRequest()->getRequestFormat()&lt;br />
	) {&lt;br />
		return;&lt;br />
	}&lt;/p>
&lt;p>	$response->setContent($response->getContent().'GA CODE');&lt;br />
});&lt;/p>
&lt;p>$framework = new Simplex\Framework($dispatcher, $matcher, $resolver);&lt;br />
$response = $framework->handle($request);&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Cet écouteur sert juste pour la démonstration, vous devriez ajouter le code Google Analytics juste avant le tag body.

Comme vous pouvez le voir, addListener() associe un callback PHP valide à un évènement nommé (« response »); le nom de l&rsquo;évènement doit être le même que celui de l&rsquo;appel à dispatch().

Dans l&rsquo;écouteur, nous ajoutons le code Google Analytics seulement si la réponse n&rsquo;est pas une redirection et si le format de sortie est en HTML (ces conditions démontrent à quel point il est facile de manipuler les données de la requête et de la réponse depuis votre code).

Très bien pour le moment, mais ajoutons un nouvel écouteur pour le même évènement. Disons que je veux définir la valeur de « Content-Length«  du header de la réponse si il n&rsquo;est pas déjà paramétré :

<code lang="php">&lt;br />
$dispatcher->addListener('response', function (Simplex\ResponseEvent $event) {&lt;br />
	$response = $event->getResponse();&lt;br />
	$headers = $response->headers;&lt;/p>
&lt;p>	if (!$headers->has('Content-Length') && !$headers->has('Transfer-Encoding')) {&lt;br />
		$headers->set('Content-Length', strlen($response->getContent()));&lt;br />
	}&lt;br />
});&lt;br />
</code>

Selon si vous avez ajouté ce morceau de code avant ou après l&rsquo;enregistrement du précédent écouteur, vous aurez la bonne ou la mauvaise valeur de Content-Length dans le header. Parfois, l&rsquo;ordre des écouteurs importe mais par défaut, tous les écouteurs sont enregistrés avec la même priorité, 0. Pour dire au dispatcher d&rsquo;envoyer un évènement tôt, changez la priorité pour un nombre positif. Les nombres négatifs peuvent par contre être utilisés pour des écouteurs à basse priorité. Ici, nous voulons que l&rsquo;écouteur pour Content-Length soit exécuté en dernier, donc on lui met comme priorité -255 :

<code lang="php">&lt;br />
$dispatcher->addListener('response', function (Simplex\ResponseEvent $event) {&lt;br />
	$response = $event->getResponse();&lt;br />
	$headers = $response->headers;&lt;/p>
&lt;p>	if (!$headers->has('Content-Length') && !$headers->has('Transfer-Encoding')) {&lt;br />
		$headers->set('Content-Length', strlen($response->getContent()));&lt;br />
	}&lt;br />
}, -255);&lt;br />
</code>

Lorsque vous créez votre framework, pensez aux priorités (réservez des nombres pour les écouteurs internes par exemple), et documentez les abondamment.

Refactorons un peu le code en déplacant l&rsquo;écouteur Google dans sa propre classe :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/GoogleListener.php

namespace Simplex;

class GoogleListener
{
	public function onResponse(ResponseEvent $event)
	{
		$response = $event->getResponse();&lt;/p>
&lt;p>		if ($response->isRedirection()&lt;br />
			|| ($response->headers->has('Content-Type') && false === strpos($response->headers->get('Content-Type'), 'html'))&lt;br />
			|| 'html' !== $event->getRequest()->getRequestFormat()&lt;br />
		) {&lt;br />
			return;&lt;br />
		}&lt;/p>
&lt;p>		$response->setContent($response->getContent().'GA CODE');&lt;br />
	}&lt;br />
}&lt;br />
</code>

Faisons la même chose avec l&rsquo;autre écouteur :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/ContentLengthListener.php

namespace Simplex;

class ContentLengthListener
{
	public function onResponse(ResponseEvent $event)
	{
		$response = $event->getResponse();&lt;br />
		$headers = $response->headers;&lt;/p>
&lt;p>		if (!$headers->has('Content-Length') && !$headers->has('Transfer-Encoding')) {&lt;br />
			$headers->set('Content-Length', strlen($response->getContent()));&lt;br />
		}&lt;br />
	}&lt;br />
}&lt;br />
</code>

Notre contrôleur de façade devrait maintenant ressembler à ça :

<code lang="php">&lt;br />
$dispatcher = new EventDispatcher();&lt;br />
$dispatcher->addListener('response', array(new Simplex\ContentLengthListener(), 'onResponse'), -255);&lt;br />
$dispatcher->addListener('response', array(new Simplex\GoogleListener(), 'onResponse'));&lt;br />
</code>

Même si le code est maintenant convenablement séparé dans des classes, il y a toujours un léger problème : la connaissance de la priorité est codé en dur dans le contrôleur de façade, au lieu d&rsquo;être définie dans les écouteurs eux-même. Dans chaque application, il va vous falloir vous souvenir des priorités appropriées. De plus, les noms des méthodes des écouteurs sont également exposées ici, ce qui signifie que si l&rsquo;on refactore le code, il faudra changer tout le code qui en dépend. Bien sûr, il y a une solution : utiliser des inscription (subscribers) au lieu des écouteurs.

<code lang="php">&lt;br />
$dispatcher = new EventDispatcher();&lt;br />
$dispatcher->addSubscriber(new Simplex\ContentLengthListener());&lt;br />
$dispatcher->addSubscriber(new Simplex\GoogleListener());&lt;br />
</code>

Une inscription sait tout de l&rsquo;évènement auquel elle s&rsquo;intéresse et fournit les informations au dispatcher via la méthode getSubscribedEvents(). Regardez la nouvelle version du « GoogleListener » :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/GoogleListener.php

namespace Simplex;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class GoogleListener implements EventSubscriberInterface
{
	// ...

	public static function getSubscribedEvents()
	{
		return array('response' => 'onResponse');&lt;br />
	}&lt;br />
}&lt;br />
</code>

Et il y a également une nouvelle version du « ContentLengthListener » :  
<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/ContentLengthListener.php

namespace Simplex;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ContentLengthListener implements EventSubscriberInterface
{
	// ...

	public static function getSubscribedEvents()
	{
		return array('response' => array('onResponse', -255));&lt;br />
	}&lt;br />
}&lt;br />
</code>

Une unique inscription pour héberger autant d&rsquo;écouteurs que vous le voulez, vers autant d&rsquo;évènements que vous le souhaitez.

Pour rendre votre framework vraiment flexible, n&rsquo;hésitez pas à ajouter plus d&rsquo;évènements; et pour le rendre génial dès la sortie de sa boite, ajoutez plus d&rsquo;écouteurs. Je vous rappelle que cette série n&rsquo;a pas pour but de créer un framework générique, mais un qui soit taillé sur mesure à vos besoins. Arrêtez quand vous le pensez nécessaire, et faites évoluer le code de votre côté.