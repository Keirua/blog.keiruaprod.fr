---
id: 421
title:
  - Redirection après login sous Symfony2
date: 2012-07-26T13:19:01+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=421
permalink: /2012/07/26/redirection-apres-login-sous-symfony2/
keywords:
  - Php, symfony2, FOSUserBundle, redirection, event
description:
  - Redirection après login sous Symfony2 avec FOSUserBundle
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - event
  - FOSUserBundle
  - Php
  - redirection
  - Symfony2
---
Vous connaissez sans doute [FOSUserBundle](https://github.com/FriendsOfSymfony/FOSUserBundle), un des bundle les plus connus et utilisés de Symfony2. Il permet de gérer l&rsquo;enregistrement et l&rsquo;authentification de vos utilisateurs de manière très simple, ce qui permet de se concentrer sur le code métier des applications.

La [documentation](https://github.com/FriendsOfSymfony/FOSUserBundle/tree/master/Resources/doc) du bundle est très complète et bien fournie, mais ne couvre pas un détail : lorsqu&rsquo;un utilisateur se connecte dans votre application (avec son login/mot de passe par exemple), si l&rsquo;authentification réussit, alors l&rsquo;utilisateur est redirigé vers la page d&rsquo;accueil. 

Mais cela n&rsquo;est pas forcément ce que l&rsquo;on souhaite ! On peut vouloir qu&rsquo;il soit redirigé ailleurs, par exemple vers sa page de profil. Et quand c&rsquo;est comme ça, on fait comment ? C&rsquo;est ce que je vais vous expliquer.  
<!--more-->

  
Si ce problème n&rsquo;est pas indiqué dans la documentation du bundle, c&rsquo;est car l&rsquo;authentification est en fait gérée par symfony, et non par le bundle. Cela n&rsquo;en reste pas moins un problème. Dustin Dobervich a proposé une première solution, [il y a un bon moment](http://www.dobervich.com/2011/05/19/more-sophisticated-symfony2-login-redirection/). Cette solution a depuis [été améliorée](http://www.dobervich.com/2011/10/13/login-redirection-revisited/), mais je vais vous présenter les 2, car elles permettent de mieux comprendre comment fonctionne le framework en interne.

Si vous avez lu ma traduction des articles de Fabien Potencier sur les composants du framework, vous savez que moteur interne interne de Symfony2 utilise beaucoup les évènements. Il est possible « d&rsquo;écouter » ces évènements, afin de réagir lorsqu&rsquo;ils arrivent. Pour cela, on crée ce qu&rsquo;il s&rsquo;appelle un listener.

En ce qui nous concerne, la solution initiale proposée par Dustin consiste à écouter 2 évènements : security.interactive_login et kernel.response. Le premier évènement est créé après que l&rsquo;authentification ai réussie. Le second est généré lorsqu&rsquo;une réponse, n&rsquo;importe laquelle, est créée. 

Intuitivement, il suffit donc de réaliser une redirection lors du second évènement. Mais si nous faisons cela sans conditions, n&rsquo;importe quelle page va nous rediriger vers la page de profil, car notre évènement va se déclencher à chaque fois.  
Pour palier à celà, notre pouvons définir un flag qui indiquera, grâce à l&rsquo;évènement security.interactive_login, lorsqu&rsquo;il faudra ou non effectuer une redirection.

Cette solution fonctionne, et je vous invite à regarder le code proposé dans [l&rsquo;article original](http://www.dobervich.com/2011/05/19/more-sophisticated-symfony2-login-redirection/) pour voir son implémentation (la problématique est légèrement différente). L&rsquo;inconvénient, c&rsquo;est qu&rsquo;on écoute l&rsquo;évènement kernel.response en permanence, ce qui ne sert à rien : exécuter du code inutilement n&rsquo;est jamais une bonne chose. En effet, la condition « cette réponse fait-elle suite à une connection réussie ? » échoue la plupart du temps, car les utilisateurs ne passent pas leur temps à se connecter. Bref niveau performances c&rsquo;est pas terrible (même si ça n&rsquo;est pas forcément critique), et niveau conception c&rsquo;est pas fou non plus.

Pour pallier à celà, nous n&rsquo;allons écouter en permanence que l&rsquo;évènement security.interactive_login, qui n&rsquo;est pas déclenché très souvent, et uniquement quand nous en avons besoin. Lorsque cela arrive, nous allons demander d&rsquo;écouter l&rsquo;évènement kernel.response qui va arriver grâce au dispatcher d&rsquo;évènements, afin de déclencher la redirection uniquement lorsque nous en avons besoin.

Nous allons créer notre listener dans KeiruaProd\FooBundle\Listener\LoginRedirectionListener.php, et y mettre le code suivant.

<code lang="php">&lt;br />
<?php
namespace KeiruaProd\FooBundle\Listener;
 
use Symfony\Component\HttpKernel\Event\FilterResponseEvent;
use Symfony\Component\Security\Http\Event\InteractiveLoginEvent;
use Symfony\Component\Routing\Router;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\EventDispatcher\EventDispatcher;
use Symfony\Component\HttpKernel\KernelEvents;
 
class LoginRedirectionListener
{   
    private $router;
    private $dispatcher;
 
    public function __construct(Router $router, EventDispatcher $dispatcher)
    {
		// On enregistre les services dont on a besoin
        $this->router = $router;&lt;br />
        $this->dispatcher = $dispatcher;&lt;br />
    }&lt;/p>
&lt;p>	public function onSecurityInteractiveLogin(InteractiveLoginEvent $event)&lt;br />
    {&lt;br />
		// On demande a écouter une fois l'évènement kernel.response&lt;br />
        $this->dispatcher->addListener(KernelEvents::RESPONSE, array($this, 'redirectUserToProfilePage'));&lt;br />
    }&lt;/p>
&lt;p>    public function redirectUserToProfilePage(FilterResponseEvent $event)&lt;br />
    {&lt;br />
		// on effectue la redirection&lt;br />
		$response = new RedirectResponse($this->router->generate('KeiruaProdFooBundle_myprofile'));&lt;br />
        $event->setResponse($response);&lt;br />
    }&lt;br />
}&lt;br />
</code>

Ce code fait tout ce qui a été décrit plus haut : il demande à écouter le message kernel.response lorsque la méthode onSecurityInteractiveLogin est appelée. redirectUserToProfilePage se charge de rediriger l&rsquo;utilisateur vers sa page de profil. A noter au passage l&rsquo;utilisation du service de routage et du dispatcher d&rsquo;évènements, que nous allons devoir injecter.

C&rsquo;est bien beau tout ça, mais pour le moment, ce code n&rsquo;est pas executé, car il n&rsquo;y a aucune raison que la méthode onSecurityInteractiveLogin soit appelée. Il faut maintenant la reférencer, afin que symfony appelle lorsque c&rsquo;est nécessaire. Il suffit de créer un service grâce à un fichier KeiruaProd\FooBundle\Ressources\config\loginlistener.xml, qui contient ce qui suit :

<code lang="xml">&lt;br />
<?xml version="1.0" ?>&lt;br />
&lt;container xmlns="http://symfony.com/schema/dic/services"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">
    &lt;parameters>
        &lt;parameter key="kernel.listener.keiruaprod.login.class">&lt;/parameter>
    &lt;/parameters>
    &lt;services>&lt;br />
        &lt;service id="kernel.listener.keiruaprod.login" class="KeiruaProd\HabitsBundle\Listener\LoginRedirectionListener" scope="request">&lt;/p>
&lt;p>			&lt;tag name="kernel.event_listener" event="security.interactive_login" method="onSecurityInteractiveLogin" />&lt;/p>
&lt;p>            &lt;argument type="service" id="router" />&lt;br />
            &lt;argument type="service" id="event_dispatcher" />&lt;br />
        &lt;/service>&lt;br />
    &lt;/services>&lt;br />
&lt;/container>&lt;br />
</code>

Ce fichier de configuration crée un service, que nous allons par la suite injecter dans le container de services.

Les tags permettent de préciser que ce service écoute les évènements, de dire lesquels et de préciser quelle méthode appeler. Il y a un paquet de noms de tags, référez vous à [la documentation](http://symfony.com/doc/current/reference/dic_tags.html) pour en savoir plus. En l&rsquo;occurence on crée un listener qui, lors de l&rsquo;évènement security.interactive_login, demande à appeler la méthode « onSecurityInteractiveLogin ». La section « argument » permet de préciser les arguments à passer au constructeur. Ici nous fournissons au constructeur le service de routage, référencé par son identifiant « router », ainsi que le service de dispatcher d&rsquo;évènements. Au passage, si vous cherchez le nom d&rsquo;un service, n&rsquo;oubliez pas la commande app/console container:debug !

Nous avons configuré notre service. Plus qu&rsquo;à le référencer dans l&rsquo;application !

Ajoutez, dans la section imports de votre fichier app/config.yml une ligne du genre :  
<code lang="yaml">&lt;br />
imports:&lt;br />
    - { resource: "@KeiruaProdFooBundle/Resources/config/loginlistener.xml" }&lt;br />
</code>

Et voila ! Mission accomplie, on est maintenant capable de rediriger l&rsquo;utilisateur vers sa page de profil quand il se connecte, que ce soit via FOSUserBundle ou par une autre méthode.