---
id: 297
title: Créez votre propre framework… avec les composants Symfony2 (partie 11)
date: 2012-02-02T06:51:01+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=297
permalink: /2012/02/02/creez-votre-propre-framework-avec-les-composants-symfony2-partie-11-2/
categories:
  - Développement Web
  - Javascript
---
Cet article est la traduction d’un article original de Fabien Potencier, à l’origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/60/create-your-own-framework-on-top-of-the-symfony2-components-part-11).

Si vous deviez utiliser notre framework dès maintenant, vous voudriez probablement permettre de personnaliser les pages d&rsquo;erreur. Actuellement, nous gérons les erreurs 404 et les erreurs 500, mais les réponses sont codées en dur dans le framework lui-même. Les rendre personnalisables n&rsquo;est pas très difficile : on déclenche un nouvel évènement, et quelqu&rsquo;un l&rsquo;écoute. Pour faire ça bien, il faut que l&rsquo;écouteur appelle ensuite un contrôleur. Et si le contrôleur d&rsquo;erreur lève une exception ? Boucle infinie. Il doit y avoir un moyen plus facile, hein ?

Pensez à la classe HttpKernel ! Au lieu de résoudre les mêmes problèmes encore et encore, et réinventer la roue à chaque fois, la classe HttpKernel est une implémentation générique, extensible et flexible de HttpKernelInterface.  
<!--more-->

Cette classe est très similaire à la classe de framework que nous avons écrit jusqu&rsquo;à présent : elle déclenche des évènements à des endroits stratégiques durant la gestion des requêtes, elle utilise un résolveur de contrôleur pour choisir le contrôleur à qui envoyer la requête, et, bonus supplémentaire, elle gère les cas limites et fournit de bons retours lorsqu&rsquo;un problème survient.

Voici le nouveau code du framework :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/Framework.php

namespace Simplex;

use Symfony\Component\HttpKernel\HttpKernel;

class Framework extends HttpKernel
{
}
</code>&lt;/p>
&lt;p>Et le nouveau contrôleur de façade:&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

// example.com/web/front.php

require_once __DIR__.'/../vendor/.composer/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing;
use Symfony\Component\HttpKernel;
use Symfony\Component\EventDispatcher\EventDispatcher;

$request = Request::createFromGlobals();
$routes = include __DIR__.'/../src/app.php';

$context = new Routing\RequestContext();
$matcher = new Routing\Matcher\UrlMatcher($routes, $context);
$resolver = new HttpKernel\Controller\ControllerResolver();

$dispatcher = new EventDispatcher();
$dispatcher->addSubscriber(new HttpKernel\EventListener\RouterListener($matcher));&lt;/p>
&lt;p>$framework = new Simplex\Framework($dispatcher, $resolver);&lt;/p>
&lt;p>$response = $framework->handle($request);&lt;br />
$response->send();&lt;br />
</code>

RouterListener est une implémentation de la même logique que nous avions dans notre framework : elle associe les requêtes entrantes et remplit les attributs de requête avec les paramètres de route.

Notre code est maintenant bien plus concis et étonnamment plus robuste et puissant que jamais. Par exemple, utilisez la classe toute prête ExceptionListener pour rendre la gestion d'erreurs configurable :

<code lang="php">&lt;br />
$errorHandler = function (HttpKernel\Exception\FlattenException $exception) {&lt;br />
	$msg = 'Something went wrong! ('.$exception->getMessage().')';&lt;/p>
&lt;p>	return new Response($msg, $exception->getStatusCode());&lt;br />
});&lt;br />
$dispatcher->addSubscriber(new HttpKernel\EventListener\ExceptionListener($errorHandler);&lt;br />
</code>

ExceptionListener fournit une instance de FlattenException au lieu de lancer une instance d'Exception pour faciliter la manipulation et l'affichage des exceptions. Elle peut prendre n'importe quel contrôleur (valide) comment gestionnaire d'exceptions, vous pouvez donc créer une classe ErrorController au lieu d'utiliser une closure :

<code lang="php">&lt;br />
$listener = new HttpKernel\EventListener\ExceptionListener('Calendar\\Controller\\ErrorController::exceptionAction');&lt;br />
$dispatcher->addSubscriber($listener);&lt;br />
</code>

Le contrôleur d'erreurs, par exemple :

<code lang="php">&lt;br />
<?php

// example.com/src/Calendar/Controller/ErrorController.php

namespace Calendar\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\FlattenException;

class ErrorController
{
	public function exceptionAction(FlattenException $exception)
	{
		$msg = 'Quelquechose ne marche pas ! ('.$exception->getMessage().')';&lt;/p>
&lt;p>		return new Response($msg, $exception->getStatusCode());&lt;br />
	}&lt;br />
}&lt;br />
</code>

Voilà ! Gestion d'erreurs propre et personnalisable sans efforts. Et bien sûr, si votre contrôleur lève une exception, HttpKernel la gèrera correctement.

Dans la partie 2, nous avons parlé de la méthode Response::prepare(), qui permet de nous assurer qu'une réponse correspond à des spécifications HTTP. C'est sans doute une bonne idée de toujours y faire appel avant d'envoyer la réponse au client. C'est ce que fait le ResponseListener :

<code lang="php">&lt;br />
$dispatcher->addSubscriber(new HttpKernel\EventListener\ResponseListener('UTF-8'));&lt;br />
</code>

Celui là était facile également ! Essayons autre chose : vous voulez avoir le support du streaming sans efforts ? Enregistrez un StreamedResponseListener :

<code lang="php">&lt;br />
$dispatcher->addSubscriber(new HttpKernel\EventListener\StreamedResponseListener());&lt;br />
</code>

Et dans votre contrôleur, renvoyez une instance de StreamedResponse au lieu de Response.

Lisez le chapitre sur le [fonctionnement interne de Symfony2](http://symfony.com/doc/current/book/internals.html#events) dans sa documentation pour en savoir plus sur les évènements déclenchés par HttpKernel et en quoi il vous permettent de modifier le déroulement d'une requête.

Créez maintenant un listener qui vous permette de renvoyer une chaine au lieu d'un objet Response :

<code lang="php">&lt;br />
class LeapYearController&lt;br />
{&lt;br />
	public function indexAction(Request $request, $year)&lt;br />
	{&lt;br />
		$leapyear = new LeapYear();&lt;br />
		if ($leapyear->isLeapYear($year)) {&lt;br />
			return 'Oui, c\'est une annee bissextile ! ';&lt;br />
		}&lt;/p>
&lt;p>		return 'Non, ce n\'est pas une annee bissextile.';&lt;br />
	}&lt;br />
}&lt;br />
</code>

Pour implémenter cette fonctionnalité, nous allons écouter l'évènement kernel.view, déclenché juste après que le contrôleur ait été appelé. Son but est de convertir la valeur de retour du contrôleur en une instance appropriée de Response, mais seulement si c'est nécessaire :

<code lang="php">&lt;br />
<?php

// example.com/src/Simplex/StringResponseListener.php

namespace Simplex;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\GetResponseForControllerResultEvent;
use Symfony\Component\HttpFoundation\Response;

class StringResponseListener implements EventSubscriberInterface
{
	public function onView(GetResponseForControllerResultEvent $event)
	{
		$response = $event->getControllerResult();&lt;/p>
&lt;p>		if (is_string($response)) {&lt;br />
			$event->setResponse(new Response($response));&lt;br />
		}&lt;br />
	}&lt;/p>
&lt;p>	public static function getSubscribedEvents()&lt;br />
	{&lt;br />
		return array('kernel.view' => 'onView');&lt;br />
	}&lt;br />
}&lt;br />
</code>

Le code est simple car l'évènement kernel.view est seulement déclenché lorsque la valeur de retour du contrôleur n'est pas une Response et car spécifier la réponse depuis l'évènement stoppe la propagation de l'évènement (notre écouteur ne peut interférer avec les autres écouteurs de vue).

N'oubliez pas de l'enregistrer dans le contrôleur de façade :

<code lang="php">&lt;br />
$dispatcher->addSubscriber(new Simplex\StringResponseListener());&lt;br />
</code>

Si vous oubliez d'enregistrer l'inscription, HttpKernel va lancer une erreur avec le message suivant : "The controller must return a response (Non, ce n'est pas une annee bissextile. given).".

A ce stade, notre framework entier est aussi compact que possible et il est principalement composé d'un assemblage de librairies existantes. Pour l'étendre, il suffit d'enregister des écouteurs d'évènements ou des inscriptions.

Heureusement, vous avez maintenant une meilleure compréhension de pourquoi l'utilisation de HttpKernelInterface est si puissante. Son implémentation par défaut, HttpKernel, vous donne accès sans efforts à des fonctionnalités vraiment sympa. Et comme HttpKernel est en fait le code derrière les framework Symfony2 et Silex, vous avez le meilleur des 2 mondes : un framework personnalisé taillé sur mesure, mais basé sur une architecture bas niveau très solide et bien maintenue qui a déjà prouvée son fonctionnement sur de nombreux sites web; c'est également un code qui a eu un audit de sécurité et a prouvé bien fonctionner à des échelles très différentes.