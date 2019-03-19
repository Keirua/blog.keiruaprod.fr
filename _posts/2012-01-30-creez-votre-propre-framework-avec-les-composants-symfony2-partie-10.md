---
id: 230
title:
  - Créez votre propre framework… avec les composants Symfony2 (partie 10)
date: 2012-01-30T06:16:50+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=230
permalink: /2012/01/30/creez-votre-propre-framework-avec-les-composants-symfony2-partie-10/
description:
  - Tutoriel sur les dessous des composants de Symfony2
robotsmeta:
  - index,follow
categories:
  - Symfony2
tags:
  - cache HTTP
  - Framework
  - Symfony2
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/59/create-your-own-framework-on-top-of-the-symfony2-components-part-10).Créez votre propre framework&#8230; avec les composants Symfony2 (partie 10)

Dans la conclusion de la seconde partie de cette série, j&rsquo;ai parlé d&rsquo;un des grands avantages de l&rsquo;utilisation des composants Symfony2 : **l&rsquo;interopérabilité** entre les tous framework et les applications qui les utilisent. Faisons un grand pas en avant dans cette direction en faisant implémenter à notre framework HttpKernelInterface :

<code lang="php">&lt;br />
namespace Symfony\Component\HttpKernel;&lt;/p>
&lt;p>interface HttpKernelInterface&lt;br />
{&lt;br />
	/**&lt;br />
	 * @return Response une instance de Response&lt;br />
	 */&lt;br />
	function handle(Request $request, $type = self::MASTER_REQUEST, $catch = true);&lt;br />
}&lt;br />
</code>  
<!--more-->

  
HttpKernelInterface est, sans doute le bout de code le plus important du composant HttpKernel (sérieusement). Les framework et applications qui implémentent cette interface sont complètement interopérables. De plus, cela apporte également beaucoup de fonctionnalités intéressantes sans aucun effort.

Mettez à jour votre framework pour qu&rsquo;il implémente cette interface :

<code lang="php">&lt;br />
<?php

// example.com/src/Framework.php

// ...

use Symfony\Component\HttpKernel\HttpKernelInterface;

class Framework implements HttpKernelInterface
{
	// ...

	public function handle(Request $request, $type = HttpKernelInterface::MASTER_REQUEST, $catch = true)
	{
		// ...
	}
}
</code>&lt;/p>
&lt;p>Même si ce changement a l'air trivial, il nous apporte beaucoup ! Parlons d'un des apports les plus impressionnants : le support transparent du &lt;a href="http://symfony.com/doc/current/book/http_cache.html">cache HTTP&lt;/a>.&lt;/p>
&lt;p>La classe HttpCache implémente un proxy inverse complet, écrit en PHP; Il implémente HttpKernelInterface et s'articule autour d'une autre instance de HttpKernelInterface :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />
// example.com/web/front.php&lt;/p>
&lt;p>$framework = new Simplex\Framework($dispatcher, $matcher, $resolver);&lt;br />
$framework = new HttpKernel\HttpCache\HttpCache($framework, new HttpKernel\HttpCache\Store(__DIR__.'/../cache'));&lt;/p>
&lt;p>$framework->handle($request)->send();&lt;br />
</code>

C'est tout ce que cela demande pour ajouter le support du cache HTTP à notre framework. C'est pas fabuleux ?

Configurer le cache doit être fait à travers les headers du cache HTTP. Par exemple, pour mettre en cache une réponse 10 secondes, utilisez la méthode Response::setTtl() :

<code lang="php">&lt;br />
// example.com/src/Calendar/Controller/LeapYearController.php&lt;/p>
&lt;p>public function indexAction(Request $request, $year)&lt;br />
{&lt;br />
	$leapyear = new LeapYear();&lt;br />
	if ($leapyear->isLeapYear($year)) {&lt;br />
		$response = new Response('Oui, c\'est une année bissextile !');&lt;br />
	} else {&lt;br />
		$response = new Response('Non, ce n\'est pas une année bissextile.');&lt;br />
	}&lt;/p>
&lt;p>	$response->setTtl(10);&lt;/p>
&lt;p>	return $response;&lt;br />
}&lt;br />
</code>

Si, comme moi, vous lancez le framework depuis la ligne de commande en simulant des requêtes ("Request::create('/is\_leap\_year/2012')"), vous pouvez facilement débugger les instances des réponses en affichant leur contenu sous forme de chaine de caractères ("echo $response;"), car cela affiche tous les headers ainsi que le contenu de la réponse.

Pour nous assurer que cela fonctionne correctement, ajoutez un nombre aléatoire au contenu de la réponse et vérifiez que ce nombre ne change que toutes les 10 secondes :

<code lang="php">&lt;br />
$response = new Response('Oui, c\' est une année bissextile ! '.rand());&lt;br />
</code>

Lorsque vous réalisez le déploiement dans l'environnement de production, continuez d'utiliser le proxy inverse de Symfony2 (très bien pour les hébergements partagés) ou encore mieux, utilisez en un d'encore plus efficace tel que [Varnish](https://www.varnish-cache.org/).

utiliser les headers de cache HTTP pour gérer le cache de notre application est très puissant et vous permet de configurer aux petits oignons votre stratégie de mise en cache, car vous pouvez utiliser à la fois l'expiration et le modèle de validation des spécifications HTTP. Si vous n'êtes pas à l'aise avec ces concepts, je vous recommande fortement de lire le chapitre sur le [cache HTTP](http://symfony.com/doc/current/book/http_cache.html) de la documentation de Symfony2.

La classe de réponse contient plusieurs autres méthodes qui nous permettent de configurer le cache HTTP très facilement. "setCache()" est une des plus puissantes, car elle délègue les stratégies de mise en cache les plus courantes dans un simple tableau :

<code lang="php">&lt;br />
$date = date_create_from_format('Y-m-d H:i:s', '2005-10-15 10:00:00');&lt;/p>
&lt;p>$response->setCache(array(&lt;br />
	'public'        => true,&lt;br />
	'etag'          => 'abcde',&lt;br />
	'last_modified' => $date,&lt;br />
	'max_age'       => 10,&lt;br />
	's_maxage'      => 10,&lt;br />
));&lt;/p>
&lt;p>// c'est l'équivalent du code suivant :&lt;br />
$response->setPublic();&lt;br />
$response->setEtag('abcde');&lt;br />
$response->setLastModified($date);&lt;br />
$response->setMaxAge(10);&lt;br />
$response->setSharedMaxAge(10);&lt;br />
</code>

Lorsque vous utilisez le modèle de validation, la méthode isNotModified() vous permet de facilement réduire le temps de réponse en court-cicuitant la génération de la réponse dès que possible :

<code lang="php">&lt;br />
$response->setETag('ce_que_vous_calculez_comme_etag');&lt;/p>
&lt;p>if ($response->isNotModified($request)) {&lt;br />
	return $response;&lt;br />
}&lt;br />
$response->setContent('Contenu calculé de la réponse');&lt;/p>
&lt;p>return $response;&lt;br />
</code>

Utiliser le cache HTTP c'est bien, mais que faire si l'on ne peut mettre en cache la page entière ? Et si vous pouviez mettre en cache tout sauf la barre latérale, qui est plus dynamique que le reste du contenu ? Les [Edge Side Includes](http://en.wikipedia.org/wiki/Edge_Side_Includes) (ESI) peuvent nous venir en aide ! Au lieu de générer le tout le contenu en une fois, les ESI nous permettent de délimiter la région d'une page comme contenu de l'appel à une sous-requête :

<code lang="html">&lt;br />
Ceci est le contenu de votre page&lt;/p>
&lt;p>Est-ce que 2012 est bissextile ? &lt;esi:include src="/leapyear/2012" />&lt;/p>
&lt;p>Autre contenu&lt;br />
</code>

Pour que les tags ESI soient supportés dans le HttpCache, vous devez lui fournir une instance de la classe "ESI". La classe ESI extrait automatiquement les tags ESI et réalise les sous-requêtes pour les convertir en contenu approprié :

<code lang="php">&lt;br />
$framework = new HttpKernel\HttpCache\HttpCache(&lt;br />
	$framework,&lt;br />
	new HttpKernel\HttpCache\Store(__DIR__.'/../cache'),&lt;br />
	new HttpKernel\HttpCache\ESI()&lt;br />
);&lt;br />
</code>

Pour que les ESI fonctionne, il vous faut un proxy inverse qui les supporte, comme celui de Symfony2. [Varnish](https://www.varnish-cache.org/) est la meilleure alternative et est open-source.

Lorsque l'on utilise des stratégies de mise en cache complexe et/ou beaucoup de tags ESI, il peut être difficile de comprendre pourquoi et quand une ressource doit être mise en cache. Pour faciliter le débuggage, vous pouvez activer le mode de débug :

<code lang="php">&lt;br />
$framework = new HttpCache($framework, new Store(__DIR__.'/../cache'), new ESI(), array('debug' => true));&lt;br />
</code>

Le mode de début ajoute un header X-Symfony-Cache à chaque réponse pour décrire ce que la couche de cache a fait :

`<br />
X-Symfony-Cache:  GET /is_leap_year/2012: stale, invalid, store</p>
<p>X-Symfony-Cache:  GET /is_leap_year/2012: fresh<br />
` 

HttpCache supporte de nombreuses autres fonctionnalités d'extensions de contrôle de cache, comme par exemple "stale-while-revalidate" et "stale-if-error" telle qu'elles ont été définies dans la RFC 5861.

Avec l'ajout de cette simple interface, notre framework peut maintenant bénéficier de nombreuses fonctionnalités embarquées dans le composant HttpKernel; La mise en cache HTTP est l'une des plus importante, car elle peut faire décoller les performances de votre application !