---
id: 91
title:
  - Créez votre propre framework... avec les composants Symfony2 (partie 2)
date: 2012-01-11T00:01:05+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=91
permalink: /2012/01/11/creez-votre-propre-framework-avec-les-composants-symfony2-partie-2/
keywords:
  - Framework web, HttpFoundation, Symfony2
description:
  - Tutoriel sur les dessous des composants Symfony2
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - Framework web
  - HttpFoundation
  - Symfony2
---
Cet article est la traduction d&rsquo;un article original de Fabien Potencier, à l&rsquo;origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/51/create-your-own-framework-on-top-of-the-symfony2-components-part-2).

Avant de plonger dans le refactoring du code, je voudrais revenir en sur les raisons pour lesquels vous pourriez vouloir utiliser un framework plutôt qu&rsquo;une bonne vieille application PHP. Pour parler de pourquoi l&rsquo;utilisation d&rsquo;un framework utilisant les composants Symfony2 est une meilleure idée que celle d&rsquo;en créer un de zéro.

Je ne parlerais pas des bénéfices évidents de l&rsquo;utilisation d&rsquo;un framework lorsque l&rsquo;on travaille sur de grosses applications avec beaucoup de développeurs; Internet propose déjà beaucoup de ressources à ce sujet.  
<!--more-->

  
Même si l' »application » que nous avons écrit hier était très simple, elle souffre de quelques problèmes :

<code lang="php">&lt;br />
<?php

// framework/index.php

$input = $_GET['name'];

printf('Hello %s', $input);
</code>&lt;/p>
&lt;p>Tout d'abord, si le paramètre de la requête name ne se trouve pas dans la chaine de l'URL de requête, il va y avoir un warning PHP; corrigeons donc ce problème :&lt;/p>
&lt;p>&lt;code lang="php">

<?php

// framework/index.php

$input = isset($_GET['name']) ? $_GET['name'] : 'World';

printf('Hello %s', $input);
</code>&lt;/p>
&lt;p>Ensuite, cette application n'est pas sécurisée. C'est dingue non ? Même ce simple bout de code PHP est vulnérable à l'un des problèmes de sécurité les plus répandus sur Internet : XSS (Cross-Site Scripting). Voici une version plus sûre :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

$input = isset($_GET['name']) ? $_GET['name'] : 'World';

header('Content-Type: text/html; charset=utf-8');

printf('Hello %s', htmlspecialchars($input, ENT_QUOTES, 'UTF-8'));
</code>&lt;/p>
&lt;p>Comme vous l'avez peut-être remarqué, sécuriser son code avec htmlspecialchars est pénible et source d'erreurs. C'est l'une des raisons pour laquelle utiliser un moteur de template tel que &lt;a href="http://twig.sensiolabs.com/">Twig&lt;/a>, qui propose un échappement automatique par défaut, peut être une bonne idée; l'échappement explicite y est d'ailleurs moins pénible, grâce à l'usage plus simple du filtre e.&lt;/p>
&lt;p>Comme vous pouvez vous en rendre compte, le code tout simple que nous avions écrit au départ n'est plus si simple si l'on veut éviter les erreurs PHP et rendre le code sécurisé.&lt;/p>
&lt;p>En plus de la sécurité, ce code n'est même pas facilement testable. Même s'il n'y a pas grand chose à tester, cela me dérange que l'écriture de tests unitaires pour le plus simple bout de PHP ne soit pas naturel et même plutôt laid. Voici une tentative de test unitaire PHPUnit du code précédent :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

// framework/test.php

class IndexTest extends \PHPUnit_Framework_TestCase
{
    public function testHello()
    {
        $_GET['name'] = 'Fabien';

        ob_start();
        include 'index.php';
        $content = ob_get_clean();

        $this->assertEquals('Hello Fabien', $content);&lt;br />
    }&lt;br />
}&lt;br />
</code>

Si votre application était un peu plus grosse, nous aurons aurions pu trouver encore plus de problèmes. Si cela vous intéresse, lisez l'article [Symfony2 versus Flat PHP](http://symfony.com/doc/2.0/book/from_flat_php_to_symfony2.html) de la documentation de Symfony2.

A ce stade, si vous n'êtes pas convaincus que la sécurité et les tests sont en effet 2 très bonnes raisons pour arrêter d'écrire du code d'une ancienne manière et plutôt adopter un framework (quoi que cela puisse signifier dans ce contexte), vous pouvez arrêter la lecture de cette série d'articles et retourner à ce que vous étiez en train de coder avant.

Bien sûr, utiliser un framework devrait vous apporter plus que de la sécurité et de la testabilité, mais la chose la plus importante à garder à l'esprit c'est qu'un framework doit vous permettre d'écrire du code de meilleure qualité et plus rapidement.

### Débuts de POO avec le composant HttpFoundation

Écrire du code pour le web, cela consiste principalement à intéragir avec de l'HTTP. Les principes fondamentaux d'un framework doivent donc être liés aux [spécifications HTTP](http://tools.ietf.org/wg/httpbis/).

Les spécifications HTPS décrivent comment un client (un navigateur, par exemple) intéragissent avec un serveur. (notre application, via un serveur web). Le dialogue entre un client et un serveur est spécifié par des messages bien définis, des requêtes et des réponses : le client envoit une requ^ête au serveur, et à partir de cette requête le serveur envoit une réponse..

En PHP, la requête est représentée par les variables globales ($\_GET, $\_POST,  
$\_FILE, $\_COOKIE, $_SESSION...) et la réponse est générée par des fonctions (echo, header, setcookie, ...).

La première étape vers un meilleur code se trouve probablement dans l'approche objet; c'est le principal but du composant [HttpFoundation](http://symfony.com/doc/current/components/http_foundation.html) de Symfony2 : remplacer les variables globales et les fonctions de PHP par une couche objet.

Pour utiliser ce composant, ouvrez le fichier composer.json et ajoutez-y une dépendance :  
<code lang="javascript">&lt;br />
{&lt;br />
    "require": {&lt;br />
        "symfony/class-loader": "2.1.*",&lt;br />
        "symfony/http-foundation": "2.1.*"&lt;br />
    }&lt;br />
}</code>

Ensuite, lancez la commande update de composer:

<code lang="bash">&lt;br />
$ php composer.phar update&lt;br />
</code>

Enfin, ajoutez le code nécessaire à l'autoloading du composant à la fin du fichier autoload.php :

<code lang="php">&lt;br />
<?php

// framework/autoload.php

$loader->registerNamespace('Symfony\\Component\\HttpFoundation', __DIR__.'/vendor/symfony/http-foundation');&lt;br />
</code>

Maintenant, réécrivons notre application pour utiliser les classes Request et Response :

<code lang="php">&lt;br />
<?php

// framework/index.php

require_once __DIR__.'/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();

$input = $request->get('name', 'World');&lt;/p>
&lt;p>$response = new Response(sprintf('Hello %s', htmlspecialchars($input, ENT_QUOTES, 'UTF-8')));&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

La méthode createFromGlobals() crée un objet Request à partir des valeurs actuelles des variables globales de PHP.

la méthode send() renvoit l'objet Response au client (d'abord l'entête HTTP, puis le contenu).

Avant l'appel à send(), nous aurions dû ajouter un appel à la méthode prepare() (en faisant $response->prepare($request);) pour nous assurer que notre Response est bien conforme aux spécifications HTTP. Par exemple, si nous devions appeler la page avec la méthode HEAD, elle aurait enlevé le contenu de la réponse.

La différence principale avec le code précédent est que vous avez un contrôle total des messages HTTP. Vous pouvez créer n'importe quel requête, et vous êtes en charge d'envoyer la réponse que vous voulez quand vous le voulez.

Nous n'avons pas explicitement précisé le header Content-Type dans le code réécrit, car le charset par défaut de l'objet Response est UTF-8.

Avec la classe Request, vous avez toutes les informations sur la requête au bout des doigts grâce à cette simple API :

<code  lang="php">&lt;br />
<?php
// l'URI demandée (par ex. /about) sans les paramètres de requête
$request->getPathInfo();&lt;/p>
&lt;p>// Récupérer les variables GET et POST respectivement&lt;br />
$request->query->get('foo');&lt;br />
$request->request->get('bar', 'valeur par defaut si bar n existe pas');&lt;/p>
&lt;p>// Récupérer la variable SERVER&lt;br />
$request->server->get('HTTP_HOST');&lt;/p>
&lt;p>// Récupérer une instance d'un objet UploadedFile identifié par foo&lt;br />
$request->files->get('foo');&lt;/p>
&lt;p>// Récupérer la valeur d'un COOKIE&lt;br />
$request->cookies->get('PHPSESSID');&lt;/p>
&lt;p>// Récupérer le header d'une requête HTTP, avec des clés normalisées, en minusucule&lt;br />
$request->headers->get('host');&lt;br />
$request->headers->get('content_type');&lt;/p>
&lt;p>$request->getMethod();    // GET, POST, PUT, DELETE, HEAD&lt;br />
$request->getLanguages(); // Un tableau des languages que le client accepte&lt;br />
</code>

Vous pouvez également simuler une requête :

<code lang="php">&lt;br />
$request = Request::create('/index.php?name=Fabien');&lt;br />
</code>

Avec la classe Response, vous pouvez facilement personnaliser la réponse :

<code lang="php">&lt;br />
<?php

$response = new Response();

$response->setContent('Hello world!');&lt;br />
$response->setStatusCode(200);&lt;br />
$response->headers->set('Content-Type', 'text/html');&lt;/p>
&lt;p>// configuration du header du cache HTTP&lt;br />
$response->setMaxAge(10);&lt;br />
</code>

Pour débugguer une réponse, faites-en un cast vers un string; celà va vous donner la représentation HTTP de la réponse (header et contenu).

Pour finir, ces classes, comme toutes celles du code de Symfony2, ont été [auditées](http://symfony.com/blog/symfony2-security-audit) d'un point de vue sécurité par une société indépendante. De plus, être un projet open-source signifie également que d'autres programmeurs partout dans le monde en ont lu le code et ont déjà résolu des problèmes de sécurité potentiels. C'est quand la dernière fois que vous avez eu un audit de code professionnel pour du code maison ?

Même quelque chose d'aussi simple que l'obtention de l'adresse IP du client peut ne pas être sécurisé :

<code lang="php">&lt;br />
<?php

if ($myIp == $_SERVER['REMOTE_ADDR']) {
    // Le client est connu, donc on lui accorde quelques privilièges supplémentaires
}
</code>&lt;/p>
&lt;p>Cela marche parfaitement jusqu'à ce que vous ayiez un proxy inverse devant le serveur de production; à ce moment là, vous devrez changer votre code pour qu'il marche à la fois sur la machine de développement (où il n'y a pas de proxy) et sur votre serveur :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

if ($myIp == $_SERVER['HTTP_X_FORWARDED_FOR'] || $myIp == $_SERVER['REMOTE_ADDR']) {
    // Le client est connu, donc on lui accorde quelques privilièges supplémentaires
}
</code>&lt;/p>
&lt;p>Utiliser la méthode Request::getClientIp() vous aurait fourni le comportement attendu dès le premier jour, et aurait couvert le cas de proxy qui s'enchainent :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

$request = Request::createFromGlobals();

if ($myIp == $request->getClientIp()) {&lt;br />
    // Le client est connu, donc on lui accorde quelques privilièges supplémentaires&lt;br />
}</code>

Et il y a un bénéfice de plus : c'est sécurisé par défaut. Qu'est ce que j'entends par sécurisé ? On ne peut pas faire confiance à la valeur de $\_SERVER['HTTP\_X\_FORWARDED\_FOR'] car elle peut être manipulée par l'utilisateur lorsqu'il n'y a pas de proxy. Du coup, si vous utilisez ce code en production sans proxy, il est très facile d'abuser votre système. Ce n'est pas le cas avec la méthode getClientIp() car vous devez explicitement faire confiance à ce header en appelant trustProxyData() :

<code lang="php"><?php

Request::trustProxyData();

if ($myIp == $request->getClientIp(true)) {&lt;br />
    // Le client est connu, donc on lui accorde quelques privilièges supplémentaires&lt;br />
}</code>

La méthode getClientIp() marche donc de manière sûre dans toutes les circonstances. Vous pouvez l'utiliser dans vos projets, quelle qu'en soit la configuration, et elle se comportera correctement. C'est l'un des buts de l'utilisation d'un framework. Si vous deviez écrire un framework de zéro, vous devriez penser à toutes ces choses par vous même. Pourquoi ne pas plutôt utiliser une technologie qui marche déjà ?

Si vous voulez en apprendre plus sur le composant HttpFoundation, vous pouvez jeter un oeil à l'[API](http://api.symfony.com/2.0/Symfony/Component/HttpFoundation.html) ou lire sa [documentation détaillée](http://symfony.com/doc/current/components/http_foundation.html) sur le site web de Symfony.

Croyez le ou non, mais nous avons notre premier framework. Vous pouvez vous arrêter là si vous le souhaitez. En général, simplement utiliser le composant HttpFoundation de Symfony2 vous permet déjà d'écrire du code meilleur et plus testable. Cela vous permet également d'écrire plus rapidement car beaucoup de problèmes que vous rencontrez quotidiennement on déjà été résolus pour vous.

En fait, des projets tels que Drupal on déjà adopté (pour la version 8 à venir) le composant HttpFoundation; s'il marche pour eux, il marchera probablement pour vous. Ne réinventez pas la roue.

J'ai presque failli oublier de vous parler d'un des bénéfices ajoutés: utiliser le composant HttpFoundation est le début d'une meilleure interopérabilité entre les framework et les applications qui les utilisent (à ce jour [Symfony2](http://symfony.com), [Drupal 8](http://drupal.org/), [phpBB 4](http://www.phpbb.com), [Silex](http://silex.sensiolabs.org/), [Midgard CMS](http://www.midgard-project.org/), [Zikula](http://zikula.org) ...).gard CMS</a>, [Zikula](http://zikula.org) ...).