---
id: 302
title:
  - Créez votre propre framework... avec les composants Symfony2 (partie 12)
date: 2012-02-07T17:52:51+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=302
permalink: /2012/02/07/creez-votre-propre-framework-avec-les-composants-symfony2-partie-12/
description:
  - "Tutoriel sur la création d'un framework avec les composants Symfony2"
robotsmeta:
  - index,follow
categories:
  - Symfony2
tags:
  - Framework
  - Symfony2
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/62/create-your-own-framework-on-top-of-the-symfony2-components-part-12).

Dans le précédent article de cette série, nous avions vidé la classe Simplex\Framework en étendant la classe HttpKernel du composant éponyme. En voyant cette classe vide, vous pouvez être tenté de déplacer du code qui se trouve dans le contrôleur de façade dedans :  
<!--more-->

  
<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/Framework.php

namespace Simplex;

use Symfony\Component\HttpKernel\HttpKernel;
use Symfony\Component\Routing;
use Symfony\Component\HttpKernel;
use Symfony\Component\EventDispatcher\EventDispatcher;

class Framework extends HttpKernel
{
	public function __construct($routes)
	{
		$context = new Routing\RequestContext();
		$matcher = new Routing\Matcher\UrlMatcher($routes, $context);
		$resolver = new HttpKernel\Controller\ControllerResolver();

		$dispatcher = new EventDispatcher();
		$dispatcher->addSubscriber(new HttpKernel\EventListener\RouterListener($matcher));&lt;br />
		$dispatcher->addSubscriber(new HttpKernel\EventListener\ResponseListener('UTF-8'));&lt;/p>
&lt;p>		parent::__construct($dispatcher, $resolver);&lt;br />
	}&lt;br />
}&lt;br />
</code>

Le code du contrôleur de façade devient alors plus conçis :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;

$request = Request::createFromGlobals();
$routes = include __DIR__.'/../src/app.php';

$framework = new Simplex\Framework($routes);

$framework->handle($request)->send();&lt;br />
</code>

Avoir un contrôleur de façace concis vous permet d&rsquo;avoir plusieurs contrôleurs de façades dans votre application. En quoi est-ce utile ? Cela permet d&rsquo;avoir différentes configurations pour les environnements de développement et de production par exemple. Dans l&rsquo;environnement de développement, il est utile d&rsquo;activer l&rsquo;affichage des erreurs dans le navigateur pour faciliter le débuggage :

<code lang="php">&lt;br />
ini_set('display_errors', 1);&lt;br />
error_reporting(-1);&lt;br />
</code>

&#8230; Mais vous ne voudrez certainement pas la même configuration dans l&rsquo;environnement de production (car afficher le résultat des erreurs pour les utilisateurs est une faille de sécurité que peuvent exploiter les plus malicieux). Avoir 2 contrôleurs de façade différents vous donne l&rsquo;opportunité d&rsquo;avoir des configuration légèrement différentes pour chacune d&rsquo;entre elles.

Déplacer du code du contrôleur de façade vers la classe de framework rend notre framework plus configurable, mais en même temps, crée des problèmes :

  * Nous ne sommes plus capable d&rsquo;enregisitrer des écouteurs personnalisés, car le dispatcher n&rsquo;est plus disponible à l&rsquo;extérieur de la classe Framework (cela peut facilement être contourné en ajoutant une méthode Framework::getEventDispatcher()).
  * Nous avons perdu la flexibilité que nous avions avant : vous ne pouvez pas changer l&rsquo;implémentation de l&rsquo;UrlMatcher ou du ControllerResolver
  * C&rsquo;estlié au point précédent, il est plus possible de tester facilement notre framework car il est impossible d&rsquo;en mocker les objets internes
  * Nous ne pouvons plus changer le charset fourni au ResponseListener (On peut le contourner en ajoutant un argument au constructeur)

Le code précédent ne présentait pas les mêmes problèmes car nous utilisions l&rsquo;injection de dépendances; toutes les dépendances de nos objets étaient injectées dans leurs constructeurs (par exemple, les dispatchers d&rsquo;évènements étaient injectés dans le framework de telle sorte que nous ayions un contrôle totalt sur sa création et sa configuration).

Est-ce que cela signifie que nous devons faire un choix entre flexibilité, personnalisation, facilité à tester et non-copie de code identique des contrôleurs de façade dans les applications ? Comme vous vous en doutez, il y a une solution. Nous pouvons résoudre tous ces problèmes en utilisant le container d&rsquo;injection de dépendances de Symfony2 :

<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*",&lt;br />
		"symfony/http-foundation": "2.1.*",&lt;br />
		"symfony/routing": "2.1.*",&lt;br />
		"symfony/http-kernel": "2.1.*",&lt;br />
		"symfony/event-dispatcher": "2.1.*",&lt;br />
		"symfony/dependency-injection": "2.1.*"&lt;br />
	},&lt;br />
	"autoload": {&lt;br />
		"psr-0": { "Simplex": "src/", "Calendar": "src/" }&lt;br />
	}&lt;br />
}&lt;br />
</code>

Créez un nouveau fichier pour accueillir la configuration du container d&rsquo;injection de dépendaces :

<code lang="php">&lt;br />
<?php

// example.com/src/container.php

use Symfony\Component\DependencyInjection;
use Symfony\Component\DependencyInjection\Reference;

$sc = new DependencyInjection\ContainerBuilder();
$sc->register('context', 'Symfony\Component\Routing\RequestContext');&lt;br />
$sc->register('matcher', 'Symfony\Component\Routing\Matcher\UrlMatcher')&lt;br />
	->setArguments(array($routes, new Reference('context')))&lt;br />
;&lt;br />
$sc->register('resolver', 'Symfony\Component\HttpKernel\Controller\ControllerResolver');&lt;/p>
&lt;p>$sc->register('listener.router', 'Symfony\Component\HttpKernel\EventListener\RouterListener')&lt;br />
	->setArguments(array(new Reference('matcher')))&lt;br />
;&lt;br />
$sc->register('listener.response', 'Symfony\Component\HttpKernel\EventListener\ResponseListener')&lt;br />
	->setArguments(array('UTF-8'))&lt;br />
;&lt;br />
$sc->register('listener.exception', 'Symfony\Component\HttpKernel\EventListener\ExceptionListener')&lt;br />
	->setArguments(array('Calendar\\Controller\\ErrorController::exceptionAction'))&lt;br />
;&lt;br />
$sc->register('dispatcher', 'Symfony\Component\EventDispatcher\EventDispatcher')&lt;br />
	->addMethodCall('addSubscriber', array(new Reference('listener.router')))&lt;br />
	->addMethodCall('addSubscriber', array(new Reference('listener.response')))&lt;br />
	->addMethodCall('addSubscriber', array(new Reference('listener.exception')))&lt;br />
;&lt;br />
$sc->register('framework', 'Simplex\Framework')&lt;br />
	->setArguments(array(new Reference('dispatcher'), new Reference('resolver')))&lt;br />
;&lt;/p>
&lt;p>return $sc;&lt;br />
</code>

Le but de ce fichier est de configurer vos objets et leurs dépendances. Rien n&rsquo;est instancié durant cette phase de configuration. Il s&rsquo;agit pûrement d&rsquo;une description statique des objets que vous devez manipuler et comment les créer. Les objets seront créés à la demande lorsque vous y accéderez ou lorsque le container devra créer d&rsquo;autres objets.

Par exemple, pour créer l&rsquo;écouter du routeur, nous disons à Symfony que son nom de classe est Symfony\Component\HttpKernel\EventListener\RouterListener, et que son constructeur prend en arguement un objet matcher (new Reference(&lsquo;matcher&rsquo;)). Comme vous pouvez le voir, chaque objet est référencé par un nom, une chaine qui identifie chaque objet de manière unique. Ce nom nous permets d&rsquo;obtenir un objet et de le référencer dans les définitions d&rsquo;autres objets.

Par défaut, à chaque fois que vous récupérez un objet depuis le container, il renvoit la même instance. C&rsquo;est car un container gère vos objets « globaux ».

Le contrôleur de façade sert désormais seulement à tout attacher ensemble :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;

$routes = include __DIR__.'/../src/app.php';
$sc = include __DIR__.'/../src/container.php';

$request = Request::createFromGlobals();

$response = $sc->get('framework')->handle($request);&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Si vous voulez une alternative plus légère pour votre container, envisagez l&rsquo;utilisation de [Pimple](https://github.com/fabpot/Pimple), un container d&rsquo;injection de dépendances simple en environ 60 lignes de code.

Maintenant, voici comment vous pouvez enregister un écouteur personnalisé dans le contrôleur de façade :

<code lang="php">&lt;br />
$sc->register(&lt;br />
		'listener.string_response',&lt;br />
		'Simplex\StringResponseListener'&lt;br />
	);&lt;br />
$sc->getDefinition('dispatcher')&lt;br />
	->addMethodCall('addSubscriber', array(new Reference('listener.string_response')))&lt;br />
;&lt;br />
</code>

En plus de décrire vos objets, le container d&rsquo;injections de dépendances peut également être configuré à l&rsquo;aide de paramètres. Créons en un qui définit si nous sommes ou non en mode debug :

<code lang="php">&lt;br />
$sc->setParameter('debug', true);&lt;/p>
&lt;p>echo $sc->getParameter('debug');&lt;br />
</code>

Ces paramètres peuvent être utilisés lorsque l&rsquo;on décrit des définitions d&rsquo;objets. Rendons le charset configurable :

<code lang="php">&lt;br />
$sc->register(&lt;br />
		'listener.response',&lt;br />
		'Symfony\Component\HttpKernel\EventListener\ResponseListener'&lt;br />
	)->setArguments(array('%charset%'));&lt;br />
</code>

Après ce changement, il faut définir le charset avant d&rsquo;utiliser l&rsquo;objet d&rsquo;écouteur de réponse :

<code lang="php">&lt;br />
$sc->setParameter('charset', 'UTF-8');&lt;br />
</code>

Au lieu de dire que les routes sont définies par la variable $routes, utilisons encore une fois un paramètre :

<code lang="php">&lt;br />
$sc->register(&lt;br />
		'matcher',&lt;br />
		'Symfony\Component\Routing\Matcher\UrlMatcher'&lt;br />
	)->setArguments(array('%routes%', new Reference('context')));&lt;br />
</code>

Les changements correspondants dans le contrôleur de façade :

<code lang="php">&lt;br />
$sc->setParameter('routes', include __DIR__.'/../src/app.php');&lt;br />
</code>

Nous avons évidemment à peine effleuré la surface de ce que l&rsquo;on peut faire avec le container : des noms de classe comme paramètres au remplacement de définitions d&rsquo;objets déjà existants, du support de la portée à la génération d&rsquo;une classe PHP à partir du container, et bien plus. Le container d&rsquo;injection de dépendances de Symfony2 est vraiment puissant et est capable de gérer n&rsquo;importe quelle classe PHP.

Ne me criez pas dessus si vous ne voulez pas de conainer d&rsquo;injection de dépendances dans votre framework. Si vous ne l&rsquo;aimez pas, ne l&rsquo;utilisez pas. C&rsquo;est votre framework, pas le mien.

C&rsquo;est (déjà) la fin de ma série sur la création d&rsquo;un framework avec les composants Symfony2. Je suis conscient que beaucoup de sujets n&rsquo;ont pas été abordés en détails, mais j&rsquo;espère que cela vous donnera assez d&rsquo;informations pour commencer cotre framework et pour mieux comprendre comment les composants Symfony2 fonctionnent en interne.

Si vous voulez en apprendre plus, je vous recommande fortement de lire le code source du micro-framework Silex, et plus particulièrement de la classe [Application](https://github.com/fabpot/Silex/blob/master/src/Silex/Application.php).

Amusez vous bien !

~~ FIN ~~

**P.S. :** S&rsquo;il y a suffisament d&rsquo;intérêt (contactez l&rsquo;auteur original dans les commentaires de [cette page](http://fabien.potencier.org/article/62/create-your-own-framework-on-top-of-the-symfony2-components-part-12)), je pourrais écrire quelques articles supplémentaires sur des sujets particuliers (l&rsquo;utilisation d&rsquo;un fichier de configuration pour le routage, utiliser les outils de debug de HttpKernel, l&rsquo;utilisation du client embarqué pour simuler un navigateur sont certains des sujets qui me viennent à l&rsquo;esprit par exemple).