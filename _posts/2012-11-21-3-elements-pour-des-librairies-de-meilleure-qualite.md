---
id: 493
title:
  - 3 éléments pour des librairies de meilleure qualité
date: 2012-11-21T10:46:54+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=493
permalink: /2012/11/21/3-elements-pour-des-librairies-de-meilleure-qualite/
keywords:
  - Bonnes pratiques, librairies, open source, API, développement
description:
  - 3 principes pour des librairies de meilleure qualité
robotsmeta:
  - index,follow
categories:
  - Bonnes pratiques
tags:
  - API
  - Bonnes pratiques
  - développement
  - librairies
  - open source
---
Lors de la conférence JS.Everywhere à Paris, j&rsquo;ai pu assister à une conférence très intéressante donnée par Rodney Rehm ([@rodneyrehm](https://twitter.com/rodneyrehm)) sur plein de mauvaises choses qui sont présentes un peu partout dans les API Javascript (et jusque dans JQuery). C&rsquo;est intéressant, mais la portée du sujet est bien plus large: les nombreux conseils s&rsquo;appliquent au reste du monde open source, et à l&rsquo;écriture de librairies en général, peu importe le langage. Et c&rsquo;est aussi valable ailleurs que pour le web.

Le problème de nombreuses API, c&rsquo;est qu&rsquo;elles sont diffusées librement, alors que leur code souffre de plusieurs défauts. Sans forcément regarder sous le capot, on se rend compte que de nombreuses choses ne vont dans les méthodes qui sont accessibles dans beaucoup de librairies libres. Il semblerait qu&rsquo;à un moment, elles perdent de vue l&rsquo;idée qu&rsquo;elle peuvent être utilisées par beaucoup de monde, souvent avec des approche du code différentes. La conséquences, c&rsquo;est qu&rsquo;elles deviennent inutilement difficiles d&rsquo;utilisation, les rendant ainsi pénibles et freinant leur adoption.

Pour pallier à celà, 3 idées sont à garder en tête lors du design d&rsquo;une API : **être simple, flexible,** et **robuste**.<!--more-->

## Être simple

Une API simple n&rsquo;est pas forcément une API facile à utiliser. Mais c&rsquo;est, du moins, une API qui est consistante dans son utilisation.  
D&rsquo;une méthode à une autre il ne devrait pas y avoir de surprises dans la notation des noms de fonctions. Si une methode s&rsquo;écrit fooBar(), une autre ne devrait pas être écrite BarFoo().

L&rsquo;ordre des paramètres doit également rester consistant, il ne doit pas changer d&rsquo;une méthode à une autre. C&rsquo;est souvent le cas en PHP :

<code lang="php">&lt;br />
bool in_array ( mixed $needle , array $haystack [, bool $strict = FALSE ] )&lt;br />
string strstr ( string $haystack , mixed $needle [, bool $before_needle = false ] )&lt;br />
</code>

Les quelques développeurs à qui j&rsquo;ai posé la question se posent régulièrement la question de l&rsquo;ordre des paramètres pour ces fonctions, alors que cela n&rsquo;a pas lieu d&rsquo;être. Dans le cas de ces méthodes de recherche, l&rsquo;argument donné en PHP, c&rsquo;est que les fonctions qui gèrent des array ont needle en premier, et les méthodes qui gèrent des string haystack en premier. Si cette séparation était un bon argument, des générations entières de développeurs ne se seraient pas arrachés les cheveux sur la question.

Une fonction ou méthode en devrait pas pas prendre trop d&rsquo;arguments. L&rsquo;exemple donné par Rodney est plutôt parlant, on a tous un jour ou l&rsquo;autre croisé une ligne qui ressemblait à ça :

<code lang="javascript">&lt;br />
event.initMouseEvent(&lt;br />
"click", true, true, window,&lt;br />
123, 101, 202, 101, 202,&lt;br />
true, false, false, false,&lt;br />
1, null);&lt;br />
</code>

Vous avez une idée de ce que fait l&rsquo;avant dernier paramètre, le 1 ? Si vous avez déjà programmé avec des API windows en C++ ou C#, vous savez quel genre d&rsquo;horreur c&rsquo;est. Les paramètres nommés, qui existent en Python, n&rsquo;existent pas en javascript. Par contre, on peut résoudre le problème en fournissant un objet en argument, ce qui rend envisageable d&rsquo;avoir :

<code lang="javascript">&lt;br />
event.initMouseEvent({&lt;br />
type:"click",&lt;br />
canBubble:true,&lt;br />
cancelable:true,&lt;br />
view:window,&lt;br />
detail:123,&lt;br />
screenX:101,&lt;br />
screenY:202,&lt;br />
clientX:101,&lt;br />
clientY:202,&lt;br />
ctrlKey:true,&lt;br />
altKey:false,&lt;br />
shiftKey:false,&lt;br />
metaKey:false,&lt;br />
button:1,&lt;br />
relatedTarget:null});&lt;br />
</code>

De cette manière, on connait au moins le nom du paramètre. Quand on revient quelques semaines plus tard dessus, ou quand le code est repris ou utilisé par quelqu&rsquo;un d&rsquo;autre (ça arrive assez souvent avec une librairie&#8230;), on s&rsquo;arrache moins les cheveux à comprendre ce qui est fait.

## Être flexible

Le développeur d&rsquo;une API ne peut pas penser à tous les cas d&rsquo;utilisation de son outil. D&rsquo;une part car il ne pense pas à tout, d&rsquo;autre part car certaines situations peuvent être en conflit avec d&rsquo;autres et qu&rsquo;il ne peut pas tout gérer. En fait, ce n&rsquo;est de toutes façons pas son rôle.

Être flexible, c&rsquo;est donc rendre son API extensible pour que chacun puisse y trouver son compte. C&rsquo;est un peu le fameux principe [Open/Closed](http://en.wikipedia.org/wiki/Open/closed_principle) de la programmation objet : les fonctionnalités d&rsquo;une classe doit pouvoir être étendues, mais pas modifiées (open for extension, closed for modification).

Pas mal de design patterns existent pour cela. En JS, le plus simple c&rsquo;est de penser à fournir des callback pour surcharger le comportement par défaut. Comme la fonction ajax() de jQuery, qui permet de surcharger le comportement lorsque l&rsquo;envoi est terminé :

<code lang="javascript">&lt;br />
$.ajax({&lt;br />
url: "test.html",&lt;br />
context: document.body&lt;br />
}).done(function() {&lt;br />
$(this).addClass("done");&lt;br />
});&lt;br />
</code>

## Être robuste

Une API robuste, c&rsquo;est une API qui gère correctement les erreurs. Les erreurs que peut avoir une API viennent, pour beaucoup, des paramètres qui lui sont fournis.

Une API doit pouvoir traiter des types ou des valeurs non prévues. Ca n&rsquo;est pas un problème qu&rsquo;elle plante, mais elle ne doit pas le faire silencieusement, car c&rsquo;est un cauchemar à débugger : on a en général confiance dans le code des librairies tierces, et si elles ne lèvent pas d&rsquo;erreurs, au premier abord on ne va pas suspecter que l&rsquo;erreur vient du code tiers.

Bref si une API n&rsquo;est pas capable de gérer une situation, qu&rsquo;elle ne s&rsquo;arrête pas à un simple return au début. Qu&rsquo;elle fasse au moins un log () ou autre afin de prévenir le malheureux développeur d&rsquo;où vient l&rsquo;erreur. Le temps perdu peut être immense.  
Être robuste, c&rsquo;est aussi savoir gérer de nombreux cas. Mais il ne faut pas chercher à gérer à être trop intelligent. Un exemple avec [jQuery.toggle](http://api.jquery.com/toggle/), qui permet d&rsquo;afficher ou masquer un élément :

<code lang="javascript">&lt;br />
.toggle( [duration] [, callback] )&lt;br />
.toggle( [duration] [, easing] [, callback] )&lt;br />
.toggle( showOrHide )&lt;br />
</code>

Grâce à ces différentes signatures, on peut entre autre écrire :

<code lang="javascript">&lt;br />
$("#plop").toggle(400)&lt;br />
$("#plop").toggle("fast");&lt;br />
$("#plop").toggle()&lt;br />
$("#plop").toggle(1)&lt;br />
$("#plop").toggle(true)&lt;br />
</code>

Les 2 premiers sont compréhensibles : on affiche ou cache un élément à la vitesse donnée. Pour le 3ème, là comme ça on ne sait pas trop quelle est la vitesse utilisée. Pour le 4ème, on se demande si l&rsquo;entier est utilisé comme un entier ou comme un booléen. Quand au dernier&#8230; on est en droit de se demander le rôle du booléen. Sans regarder la doc ou le code de toggle, difficile d&rsquo;être sûr de ce qui se fait.

Bref à vouloir trop en faire, on perd inutilement les développeurs qui utilisent les API.

Ces quelques exemples ne sont, en aucun cas, une liste gravée dans le marbre de règles à appliquer dans tous les cas. De plus, les bonnes pratiques de conception ne s&rsquo;arrêtent pas à seulement 3 concepts. Par contre, les avoir à l&rsquo;esprit quand on conçoit du code open source, quel que soit le langage, me semble nécessaire. Si le sujet vous intéresse, vous pourrez trouver plus d&rsquo;exemples dans [l&rsquo;article de Rodney](http://coding.smashingmagazine.com/2012/10/09/designing-javascript-apis-usability/), publié sur SmashingMagazine :

Si vous avez des idées, des remarques, ou des retours d&rsquo;expérience sur le sujet, n&rsquo;hésitez pas à en faire part dans les commentaires.

&nbsp;