---
id: 115
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 4)
date: 2012-01-12T18:43:47+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=115
permalink: /2012/01/12/creez-votre-propre-framework-avec-les-composants-symfony2-partie-4/
archived: true
keywords:
  - Framework, Routing, Symfony2
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Framework
  - Routing
  - Symfony2
---
Cet article est la traduction d&rsquo;un article original de Fabien Potencier, à l&rsquo;origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/53/create-your-own-framework-on-top-of-the-symfony2-components-part-4).

Avant de commencer avec le sujet d&rsquo;aujourd&rsquo;hui, commençons par refactorer un peu notre framework actuel pour rendre les templates encore plus lisibles :

<code lang="php">&lt;/p>
&lt;p>// example.com/web/front.php&lt;/p>
&lt;p>require_once __DIR__.'/../src/autoload.php';&lt;/p>
&lt;p>use Symfony\Component\HttpFoundation\Request;&lt;br />
use Symfony\Component\HttpFoundation\Response;&lt;/p>
&lt;p>$request = Request::createFromGlobals();&lt;/p>
&lt;p>$map = array(&lt;br />
	'/hello' => 'hello',&lt;br />
	'/bye'   => 'bye',&lt;br />
);&lt;/p>
&lt;p>$path = $request->getPathInfo();&lt;br />
if (isset($map[$path])) {&lt;br />
	ob_start();&lt;br />
	extract($request->query->all(), EXTR_SKIP);&lt;br />
	include sprintf(__DIR__.'/../src/pages/%s.php', $map[$path]);&lt;br />
	$response = new Response(ob_get_clean());&lt;br />
} else {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

<!--more-->

  
Comme nous extrayons maintenant les paramètres de la requête, simplifions le template hello.php de la manière suivante :

<code lang="html">&lt;br />
<!-- example.com/src/pages/hello.php -->&lt;/p>
&lt;p>Hello 

<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8') ?>&lt;br />
</code>

Maintenant, nous sommes prêts à ajouter de nouvelles fonctionnalités.

Un aspect très important de n&rsquo;importe quel site web est la forme de ses URLs. Grâce à la table des URL, nous avons découplé les URL du code qui génère la réponse associée, mais cela n&rsquo;est pas suffisant. Par exemple, nous pouvons vouloir des chemins dynamiques qui permettent d&#8217;embarquer directement des données dans l&rsquo;URL, au lieu de nous baser sur la chaine de la requête :

`<br />
# Avant<br />
/hello?name=Fabien</p>
<p># Après<br />
/hello/Fabien<br />
` 

Pour supporter cette fonctionnalité, nous allons utiliser le composant Routing de Symfony2. Comme toujours, ajoutez une dépendance dans le fichier composer.json et lancez la commande php composer.phar update pour l&rsquo;installer:

<code lang="javascript">&lt;br />
{&lt;br />
	"require": {&lt;br />
		"symfony/class-loader": "2.1.*",&lt;br />
		"symfony/http-foundation": "2.1.*",&lt;br />
		"symfony/routing": "2.1.*"&lt;br />
	}&lt;br />
}&lt;br />
</code>

A partir de maintenant, nous allons utiliser l&rsquo;autoloader de Composer au lieu de notre autoload.php. Supprimez le fichier autoload.php et remplacez sa référence dans front.php :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

// ...
</code>&lt;/p>
&lt;p>Au lieu d'utiliser un tableau associatif pour stocker la liste des URLs, le composant Routing utilise une instance de RouteCollection :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />
use Symfony\Component\Routing\RouteCollection;&lt;/p>
&lt;p>$routes = new RouteCollection();&lt;br />
</code>

Ajoutons une route qui décrive l'URL /hello/QUELQUECHOSE et ajoutons-en également une simple pour l'URL /bye :

<code lang="php">&lt;br />
use Symfony\Component\Routing\Route;&lt;/p>
&lt;p>$routes->add('hello', new Route('/hello/{name}', array('name' => 'World')));&lt;br />
$routes->add('bye', new Route('/bye'));&lt;br />
</code>

Chaque entrée dans la liste est définie par un nom (hello) et une instance de Route, définie par un modèle de route (\`\`/hello/{name}\`\`) et un tableau de valeurs par défaut pour les attributs de la route (array('name' => 'World')).

Lisez la [documentation officielle](http://symfony.com/doc/current/components/routing.html) du composant Routing pour en apprendre plus sur ses nombreuses fonctionnalités tel que la génération d'URL, les caractéristiques des attributs, le forçage de la méthode HTTP, le chargement via des fichiers de configuration YAML ou XML, la génération de règles de réécriture PHP ou Apache pour améliorer les performances, et bien plus.

A partir des informations présentes dans l'instance de RouteCollection, une instance de l'objet UrlMatcher permet d'associer les URL :  
<code lang="php">&lt;br />
use Symfony\Component\Routing\RequestContext;&lt;br />
use Symfony\Component\Routing\Matcher\UrlMatcher;&lt;/p>
&lt;p>$context = new RequestContext();&lt;br />
$context->fromRequest($request);&lt;br />
$matcher = new UrlMatcher($routes, $context);&lt;/p>
&lt;p>$attributes = $matcher->match($request->getPathInfo());&lt;br />
</code>

La méthode match() prend en paramètres un chemin de requête et renvoie un tableau d'attributs. Vous pouvez remarquer que la route associée est automatiquement stockée dans l'attribut spécial _route :

<code lang="php">&lt;br />
print_r($matcher->match('/bye'));&lt;br />
array (&lt;br />
  '_route' => 'bye',&lt;br />
);&lt;/p>
&lt;p>print_r($matcher->match('/hello/Fabien'));&lt;br />
array (&lt;br />
  'name' => 'Fabien',&lt;br />
  '_route' => 'hello',&lt;br />
);&lt;/p>
&lt;p>print_r($matcher->match('/hello'));&lt;br />
array (&lt;br />
  'name' => 'World',&lt;br />
  '_route' => 'hello',&lt;br />
);&lt;br />
</code>

Même si n'avons pas strictement besoin du contexte de la requête dans nos exemples, c'est utilisé dans la pratique, entre autres pour forcer la méthode HTTP à utiliser.

L'UrlMatcher lance une exception lorsqu'aucune des routes ne correspond :

<code lang="php">&lt;br />
$matcher->match('/not-found');&lt;/p>
&lt;p>// Lance une exception Symfony\Component\Routing\Exception\ResourceNotFoundException&lt;br />
</code>

En ayant ceci en tête, écrivons une nouvelle version de notre framework :  
<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing;

$request = Request::createFromGlobals();
$routes = include __DIR__.'/../src/app.php';

$context = new Routing\RequestContext();
$context->fromRequest($request);&lt;br />
$matcher = new Routing\Matcher\UrlMatcher($routes, $context);&lt;/p>
&lt;p>try {&lt;br />
	extract($matcher->match($request->getPathInfo()), EXTR_SKIP);&lt;br />
	ob_start();&lt;br />
	include sprintf(__DIR__.'/../src/pages/%s.php', $_route);&lt;/p>
&lt;p>	$response = new Response(ob_get_clean());&lt;br />
} catch (Routing\Exception\ResourceNotFoundException $e) {&lt;br />
	$response = new Response('Not Found', 404);&lt;br />
} catch (Exception $e) {&lt;br />
	$response = new Response('An error occurred', 500);&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Il y a quelques nouvelles choses dans le code :

  * Les noms de routes sont utilisés dans les noms de template;
  * Les erreurs 500 sont maintenant gérées correctement;
  * La configuration des Routes a été déplacée dans son propre fichier :
<code lang="php">&lt;br />
<?php
// example.com/src/app.php

use Symfony\Component\Routing;

$routes = new Routing\RouteCollection();
$routes->add('hello', new Routing\Route('/hello/{name}', array('name' => 'World')));&lt;br />
$routes->add('bye', new Routing\Route('/bye'));&lt;/p>
&lt;p>return $routes;&lt;br />
</code>

  * Les attributs de requête sont extraits pour garder les templates simples :
`// example.com/src/pages/hello.php<br />
echo 'Hello '.htmlspecialchars($name, ENT_QUOTES, 'UTF-8');`</ul> 

Nous avons maintnenant une séparation claire entre la configuration (tout ce qui est spécifique à notre application se trouve dans app.php) et le framework (le code générique qui anime notre application est dans front.php).

Avec moins de 30 lignes de code, nous avons un nouveau framework, plus puissant et plus flexible que le précédent. C'est cool !

Utiliser le composant Routing a un gros avantage supplémentaire : la possibilité de générer des URLs à partir des définitions de Route. En utilisant à la fois l'association d'URL et la génération d'URL dans votre code, changer les modèles d'URLs ne devrait pas avoir d'impact. Vous voulez savoir comment utiliser le générateur ? C'est incroyablement facile :

<code lang="php">&lt;br />
use Symfony\Component\Routing;&lt;/p>
&lt;p>$generator = new Routing\Generator\UrlGenerator($routes, $context);&lt;/p>
&lt;p>echo $generator->generate('hello', array('name' => 'Fabien'));&lt;br />
// affiche /hello/Fabien&lt;br />
</code>

Le code parle de lui même; grâce au contexte, vous pouvez même générer des URLs absolues :

<code lang="php">&lt;br />
echo $generator->generate('hello', array('name' => 'Fabien'), true);&lt;br />
// affiche quelque chose comme http://example.com/somewhere/hello/Fabien&lt;br />
</code>

Vous vous inquiétez pour les performance ? Grâce aux définitions de routes, vous pouvez créer une classe de résolution d'URL fortement optimisée qui permet de remplacer la classe par défaut UrlMatcher :

<code lang="php">&lt;br />
$dumper = new Routing\Matcher\Dumper\PhpMatcherDumper($routes);&lt;/p>
&lt;p>echo $dumper->dump();&lt;br />
</code>

Vous voulez encore plus de performances ? Générez un ensemble de règles de réécriture Apache à partir de vos routes :

<code lang="php">&lt;br />
$dumper = new Routing\Matcher\Dumper\ApacheMatcherDumper($routes);&lt;/p>
&lt;p>echo $dumper->dump();&lt;br />
</code>