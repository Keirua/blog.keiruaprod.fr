---
id: 146
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 8)
date: 2012-01-17T12:46:47+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=146
permalink: /2012/01/17/creez-votre-propre-framework-avec-les-composants-symfony2-partie-8/
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Framework
  - PHPUnit
  - Symfony2
  - Tests unitaires
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/57/create-your-own-framework-on-top-of-the-symfony2-components-part-8).

Des lecteurs vigilants ont fait remarquer des bugs subtils mais non moins importants dans le framework que nous avons construit hier. Lorsque l&rsquo;on crée un framework, il faut être certain qu&rsquo;il se comporte comme annoncé. Si ce n&rsquo;est pas le cas, toutes les applications basées dessus souffriront des mêmes bugs. La bonne nouvelle, c&rsquo;est que quand on corrige un bug, on le corrige dans plusieurs applications à la fois.

La mission du jour est d&rsquo;écrire des tests unitaire pour le framework que nous avons créé en utilisant [PHPUnit](http://www.phpunit.de/manual/current/en/index.html). Créez un fichier de configuration de PHPUnit dans example.com/phpunit.xml.dist :  
<code lang="xml">&lt;br />
<?xml version="1.0" encoding="UTF-8"?>&lt;/p>
&lt;phpunit backupGlobals="false"
		 backupStaticAttributes="false"
		 colors="true"
		 convertErrorsToExceptions="true"
		 convertNoticesToExceptions="true"
		 convertWarningsToExceptions="true"
		 processIsolation="false"
		 stopOnFailure="false"
		 syntaxCheck="false"
		 bootstrap="vendor/.composer/autoload.php"
>&lt;br />
	&lt;testsuites>&lt;br />
		&lt;testsuite name="Test Suite">&lt;br />
			&lt;directory>./tests&lt;/directory>&lt;br />
		&lt;/testsuite>&lt;br />
	&lt;/testsuites>
&lt;/phpunit>
&lt;p></code>

  
<!--more-->

  
Cette configuration définit définit des valeurs par défaut pour la plupart des paramètres PHPUnit; plus intéressant, l&rsquo;autoloader est utilisé pour bootstrapper les tests, et les tests seront stockés dans le répertoire example.com/tests/.

Maintenant, écrivons un test pour les ressources « Non trouvées ». Pour éviter la création de dépendances lorsque l&rsquo;on écrit des tests et pour ne réellement tester unitairement que ce qui nous intéresse, nous allons utiliser des [objets mocks](http://www.phpunit.de/manual/current/en/test-doubles.html). Les objets mocks sont plus faciles à créer lorsque l&rsquo;on utilise des interfaces plutôt que des classes concrètes. Heureusement, Symfony2 nous fournit de telles interfaces pour pour les objets du coeur de la librairie, tel que UrlMatcher et le résolveur de contrôleurs. Modifiez le framework pour vous en servir :

<code lang="php">&lt;br />
<?php
// example.com/src/Simplex/Framework.php

namespace Simplex;

// ...

use Symfony\Component\Routing\Matcher\UrlMatcherInterface;
use Symfony\Component\HttpKernel\Controller\ControllerResolverInterface;

class Framework
{
	protected $matcher;
	protected $resolver;

	public function __construct(UrlMatcherInterface $matcher, ControllerResolverInterface $resolver)
	{
		$this->matcher = $matcher;&lt;br />
		$this->resolver = $resolver;&lt;br />
	}&lt;/p>
&lt;p>	// ...&lt;br />
}&lt;br />
</code>

Nous sommes maintenant prêts pour écrire notre premier test :

<code lang="php">&lt;br />
<?php

// example.com/tests/Simplex/Tests/FrameworkTest.php

namespace Simplex\Tests;

use Simplex\Framework;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Exception\ResourceNotFoundException;

class FrameworkTest extends \PHPUnit_Framework_TestCase
{
	public function testNotFoundHandling()
	{
		$framework = $this->getFrameworkForException(new ResourceNotFoundException());&lt;/p>
&lt;p>		$response = $framework->handle(new Request());&lt;/p>
&lt;p>		$this->assertEquals(404, $response->getStatusCode());&lt;br />
	}&lt;/p>
&lt;p>	protected function getFrameworkForException($exception)&lt;br />
	{&lt;br />
		$matcher = $this->getMock('Symfony\Component\Routing\Matcher\UrlMatcherInterface');&lt;br />
		$matcher&lt;br />
			->expects($this->once())&lt;br />
			->method('match')&lt;br />
			->will($this->throwException($exception))&lt;br />
		;&lt;br />
		$resolver = $this->getMock('Symfony\Component\HttpKernel\Controller\ControllerResolverInterface');&lt;/p>
&lt;p>		return new Framework($matcher, $resolver);&lt;br />
	}&lt;br />
}&lt;br />
</code>

Ce test simule une requête qui n&rsquo;est associé à aucune route. De ce fait, la méthode match() renvoit une exception ResourceNotFoundException et nous testons que le framework convertit bien cette exception en une réponse 404.

Pour exécuter ce test, il suffit de lancer la commande « phpunit » depuis le répertoire example.com :

`$ phpunit`

Je n&rsquo;explique pas en détail comment fonctionne le code car ce n&rsquo;est pas le but de cette série, mais si vous ne comprenez rien de ce qui se passe, je vous suggère de lire la documentation de PHPUnit sur les [objets mocks](http://www.phpunit.de/manual/current/en/test-doubles.html).

Une fois le test exécuté, vous devriez voir une barre verte. Si ce n&rsquo;est pas le cas, il y a un bug soit dans le test ou dans le code du framework !

Ajouter un test unitaire pour n&rsquo;importe quelle exception lancée dans un contrôlleur est tout aussi simple :

<code lang="php">&lt;br />
public function testErrorHandling()&lt;br />
{&lt;br />
    $framework = $this->getFrameworkForException(new \RuntimeException());&lt;/p>
&lt;p>    $response = $framework->handle(new Request());&lt;/p>
&lt;p>    $this->assertEquals(500, $response->getStatusCode());&lt;br />
}&lt;/p>
&lt;p></code>  
Et pour finir, écrivons un test pour une situation où il ne doit pas y avoir d&rsquo;erreurs :

<code lang="php">&lt;br />
use Symfony\Component\HttpFoundation\Response;&lt;br />
use Symfony\Component\HttpKernel\Controller\ControllerResolver;&lt;/p>
&lt;p>public function testControllerResponse()&lt;br />
{&lt;br />
	$matcher = $this->getMock('Symfony\Component\Routing\Matcher\UrlMatcherInterface');&lt;br />
	$matcher&lt;br />
		->expects($this->once())&lt;br />
		->method('match')&lt;br />
		->will($this->returnValue(array(&lt;br />
			'_route' => 'foo',&lt;br />
			'name' => 'Fabien',&lt;br />
			'_controller' => function ($name) {&lt;br />
				return new Response('Hello '.$name);&lt;br />
			}&lt;br />
		)))&lt;br />
	;&lt;br />
	$resolver = new ControllerResolver();&lt;/p>
&lt;p>	$framework = new Framework($matcher, $resolver);&lt;/p>
&lt;p>	$response = $framework->handle(new Request());&lt;/p>
&lt;p>	$this->assertEquals(200, $response->getStatusCode());&lt;br />
	$this->assertContains('Hello Fabien', $response->getContent());&lt;br />
}&lt;br />
</code>

Dans ce test, on simule une route correctement associé qui renvoit un contrôlleur simple. On vérifie que le status de la réponse est 200 et que son contenu est celui défini dans le contrôleur.

Pour vérifier que nous avons bien couvert tous les cas d&rsquo;utilisation, lancez la fonctionnalité de couverture de code de PHPUnit (il faut activer « XDebug » (http://xdebug.org/) d&rsquo;abord):

`$ phpunit --coverage-html=cov/`

Ouvrez example.com/cov/src\_Simplex\_Framework.php.html dans un navigateur et vérifiez que toutes les lignes de la classe du framework sont vertes (cela signifie qu&rsquo;elles ont été visitées lorsque le test a été exécuté).

Grâce au code orienté objet simple que nous avons écrit jusque là, nous avons pû écrire des tests unitaires qui couvrent tous les cas d&rsquo;utilisation possibles de notre framework; Les objets mocks nous ont permis de vérifier que nous testions bien notre code et pas celui de Symfony2.

Maintenant que nous avons (à nouveau) confiance dans le code que nous avons écrit, nous pouvons penser l&rsquo;esprit tranquille au nouveau jeu de fonctionnalités que nous allons ajouter à notre framework.