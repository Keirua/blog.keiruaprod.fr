---
id: 107
title: Créez votre propre framework… avec les composants Symfony2 (partie 3)
date: 2012-01-11T20:34:16+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=107
permalink: /2012/01/11/creez-votre-propre-framework-avec-les-composants-symfony2-partie-3/
keywords:
  - Framework Web, Routing, Symfony2
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
Cet article est la traduction d&rsquo;un article original de Fabien Potencier, à l&rsquo;origine de Symfony2, disponible [ici](http://fabien.potencier.org/article/52/create-your-own-framework-on-top-of-the-symfony2-components-part-3).

Jusqu&rsquo;à présent, notre application était très simple car il n&rsquo;y a qu&rsquo;une seule page. Pour la rendre plus sympa, soyons fous et ajoutons une nouvelle page pour dire au revoir :

<code lang="php">&lt;br />
<?php

// framework/bye.php

require_once __DIR__.'/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();

$response = new Response('Au revoir!');
$response->send();&lt;br />
</code>

Comme vous pouvez le voir, la plupart du code est exactement le même que celui que nous avons écrit pour la première page. Commençons par extraire le code commun, partagé entre toutes les pages. Le partage de code semble une bonne idée pour créer notre premier « vrai » framework !  
<!--more-->

Pour effectuer ce refactoring en PHP, on peut se servir de la création d&rsquo;un fichier à inclure :

<code lang="php">&lt;br />
<?php

// framework/init.php

require_once __DIR__.'/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();
$response = new Response();
</code>&lt;/p>
&lt;p>Voici ceci dans le contexte :&lt;/p>
&lt;p>&lt;code lang="php">&lt;br />


<?php

// framework/index.php

require_once __DIR__.'/init.php';

$input = $request->get('name', 'World');&lt;/p>
&lt;p>$response->setContent(sprintf('Hello %s', htmlspecialchars($input, ENT_QUOTES, 'UTF-8')));&lt;br />
$response->send();&lt;br />
</code>

Quand à la page "Au revoir" :

<code lang="php">&lt;br />
<?php

// framework/bye.php

require_once __DIR__.'/init.php';

$response->setContent('Goodbye!');&lt;br />
$response->send();&lt;br />
</code>

Nous avons effectivement déplacé la plupart du code partagé à un endroit central, mais cela ne semble pas être une très bonne abstraction, pas vrai ? Tout d'abord, nous avons la méthode send() dans toutes les pages, nos pages ne ressemble pas à des templates et nous ne sommes toujours pas capable de tester ce code proprement.

De plus, ajouter une nouvelle page signifie que nous devons créer un nouveau script PHP, dont le nom est disponible à l'utilisateur via l'URL (http://example.com/bye.php): il y a un lien direct entre le nom du script PHP et l'URL client, car c'est le serveur qui s'occupe de dispatcher les requêtes directement... Cela peut être une bonne idée de nous occuper nous même de cela pour une meilleure flexibilité. Cela peut être réalisé facilement en routant toutes nos requêtes client vers un unique script PHP.

Fournir un unique script PHP à l'utilisateur est un design pattern qui s'appelle "[le controlleur de façade](http://symfony.com/doc/current/book/from_flat_php_to_symfony2.html#a-front-controller-to-the-rescue)".

Un tel script pourrait ressembler à celà :

<code lang="php">&lt;br />
<?php

// framework/front.php

require_once __DIR__.'/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();
$response = new Response();

$map = array(
	'/hello' => __DIR__.'/hello.php',&lt;br />
	'/bye'   => __DIR__.'/bye.php',&lt;br />
);&lt;/p>
&lt;p>$path = $request->getPathInfo();&lt;br />
if (isset($map[$path])) {&lt;br />
	require $map[$path];&lt;br />
} else {&lt;br />
	$response->setStatusCode(404);&lt;br />
	$response->setContent('Not Found');&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Et voila le contenu du nouveau script hello.php :

<code lang="php">&lt;br />
<?php

// framework/hello.php

$input = $request->get('name', 'World');&lt;br />
$response->setContent(sprintf('Hello %s', htmlspecialchars($input, ENT_QUOTES, 'UTF-8')));&lt;br />
</code>

Dans le script front.php, $map associe le chemin de l'URL avec les chemins des scripts PHP correspondants.

En bonus, si le client demande un chemin qui n'est pas défini dans cette table de hashage, nous renvoyions une erreur 404 custom; vous avez maintenant le controle de votre site web.

Pour accéder à une page, vous devez maintenant utiliser le script front.php :

  * http://example.com/front.php/hello?name=Fabien
  * http://example.com/front.php/bye

/hello et /bye sont les chemins des pages.

La plupart des serveurs web tel que Apache ou nginx sont capables de réécrire l'URL d'entrée et enlever le script du controlleur de façade de telle sorte que les utilisateurs puissent taper http://example.com/hello?name=Fabien, qui est bien plus jolie.

L'astuce réside donc dans l'utilisation de la méthode Request::getPathInfo() qui renvoie le chemin de la requête en supprimant le nom du script du controlleur de façade, y compris les sous répertoires (si nécessaire)

Vous n'avez même pas besoin de mettre en place un serveur web pour tester le code. A la place, remplacez l'appel à $request = Request::createFromGlobals(); par quelque chose comme $request = Request::create('/hello?name=Fabien'); où l'argument est le chemin d'URL que vous voulez simuler.

Maintenant que le serveur web accède toujours au même script (front.php) pour toutes les pages, nous pouvons sécuriser le code un peu plus en déplace tous les autres fichiers PHP à l'extérieur de la racine du répertoire web :

`<br />
example.com<br />
    +-- composer.json<br />
    ¦   src<br />
    ¦   +-- autoload.php<br />
    ¦   +-- pages<br />
    ¦       +-- hello.php<br />
    ¦       +-- bye.php<br />
    +-- vendor<br />
    +-- web<br />
        +-- front.php<br />
` 

Maintenant, configurez la racine de votre serveur web pour pointer sur web/ et tous les autres fichiers ne seront plus accessibles.

Pour que cette structure fonctionne, vous devrez ajuster certains chemins dans les divers fichiers PHP; ces changement sont laissés en exercice au lecteur.

La dernière chose qui est répétée dans toutes les pages, c'est l'appel à setContent(). Nous pouvons convertir toutes les pages en des templates en faisant des "echo" du contenu à afficher, et en appellant setContent() directement depuis le script du controleur de façade :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

// ...

$path = $request->getPathInfo();&lt;br />
if (isset($map[$path])) {&lt;br />
	ob_start();&lt;br />
	include $map[$path];&lt;br />
	$response->setContent(ob_get_clean());&lt;br />
} else {&lt;br />
	$response->setStatusCode(404);&lt;br />
	$response->setContent('Not Found');&lt;br />
}&lt;/p>
&lt;p>// ...&lt;br />
</code>

Et le script hello.php peut être transformé en un template :  
<code lang="php">&lt;br />
<!-- example.com/src/pages/hello.php -->&lt;/p>
&lt;p>

<?php $name = $request->get('name', 'World') ?>&lt;/p>
&lt;p>Hello 

<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8') ?>&lt;br />
</code>

Nous avons notre framework du jour :

<code lang="php">&lt;br />
<?php

// example.com/web/front.php

require_once __DIR__.'/../src/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();
$response = new Response();

$map = array(
	'/hello' => __DIR__.'/../src/pages/hello.php',&lt;br />
	'/bye'   => __DIR__.'/../src/pages/bye.php',&lt;br />
);&lt;/p>
&lt;p>$path = $request->getPathInfo();&lt;br />
if (isset($map[$path])) {&lt;br />
	ob_start();&lt;br />
	include $map[$path];&lt;br />
	$response->setContent(ob_get_clean());&lt;br />
} else {&lt;br />
	$response->setStatusCode(404);&lt;br />
	$response->setContent('Not Found');&lt;br />
}&lt;/p>
&lt;p>$response->send();&lt;br />
</code>

Ajouter une nouvelle page se fait en 2 étapes : ajouter une entrée dans la map et créer un template PHP dans \`\`src/pages/\`\`. Depuis un template, on obtient les données de la requête via la variable $request et on fournit une réponse adaptée via la variable $response.

Si vous décidez de vous arrêter là, vous pouvez probablement améliorer votre framework entre extrayant la liste des URL depuis un fichier de configuration