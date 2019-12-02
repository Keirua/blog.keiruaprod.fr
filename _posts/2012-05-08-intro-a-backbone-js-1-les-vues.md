---
id: 354
title:
  - 'Intro à Backbone.js - #1 : les vues'
date: 2012-05-08T16:17:25+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=354
permalink: /2012/05/08/intro-a-backbone-js-1-les-vues/
archived: true
keywords:
  - Backbone.js, Backbone.view, MVC, template, underscore, jquery
description:
  - "Introduction à l'utilisation de backbone.js et de ses vues"
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Javascript
tags:
  - Backbone.js
  - Backbone.view
  - jQuery
  - MVC
  - Template
  - underscore
---
_Cet article fait partie d&rsquo;une série d&rsquo;articles d&rsquo;introduction à [Backbone.js](http://documentcloud.github.com/backbone/ "Backbone.js"), largement inspirée du tutoriel (en anglais) [Hello Backbone.js](http://arturadib.com/hello-backbonejs/ "Hello Backbone.js"). Les bouts de code du tutoriel original ont été légèrement refactorés._

Backbone.js est une librairie très intéressante, mais un peu difficile à prendre en main. Des questions récurrentes sur le sujet amené à écrire cette petite série d&rsquo;articles. Mon but, c&rsquo;est de vous présenter cette librairie de manière plus simple que l&rsquo;exemple « officiel » [Backbone todos.js](http://documentcloud.github.com/backbone/docs/todos.html), qui est, disons, un peu raide.

Dans cette série donc, on va y aller de manière progressive, comme l&rsquo;on pourrait procéder lors de la conception d&rsquo;une application. Je ne toucherais pas au CSS et mettrais un minimum d&rsquo;HTML, afin de nous concentrer sur Backbone. On va partir de quelque chose de très simple, et le faire évoluer, toujours de manière simple, vers une petite application, en essayant surtout de mettre en place des bonnes pratiques.

<!--more-->

Backbone.js donc, est un framework javascript qui permet de faire du MVC côté client. Je sens que j&rsquo;ai déjà perdu pas mal de monde, donc on va y aller tranquillement.  
MVC, ça veut dire Modèle, Vue, Controlleur. C&rsquo;est un design pattern qui permet de séparer les données, la logique qui effectue les opérations dessus, et leur affichage. C&rsquo;est un framework très à la mode depuis quelques temps car il permet d&rsquo;écrire du javascript plus propre et plus maintenable. En fait, ce framework n&rsquo;ajoute pas énormément de fonctionnalités, vous pourriez très bien faire la même chose sans l&rsquo;utiliser. Mais il apporte une logique de conception et de réflexion qui est très appréciée si vous voulez écrire du code côté client de qualité, plus facilement maintenable et évolutif.

## Structure HTML

Entrons dans le vif du sujet, en écrivant le canvas HTML dans lequel nous allons écrire notre code. Rien d&rsquo;original, on inclue 3 librairies que nous allons utiliser : jQueyr, underscore, et Backbone. jQuery va nous servir à accéder aux divers éléments de la page (à travers ce que l&rsquo;on appelle l&rsquo;arbre DOM), underscore va nous servir à manipuler des modèles, et backbone, ben&#8230; justement, nous allons découvrir son utilité.

<code lang="html">&lt;br />
&lt;html>&lt;br />
&lt;br />
&lt;body>&lt;br />
	<!-- Notre code -->&lt;br />
&lt;/body>&lt;br />
&lt;/html>&lt;br />
</code>

## Notre Hello world

Entre  et , j&rsquo;ai mis un commentaire pour indiquer où placer le bout de code qui arrive.  
Nous allons faire le Hello world de Backbone.js : créer une vue qui affiche « Hello world », façon titre.  
Pour celà, on crée une class AppView, héritée de Backbone.View.  
3 choses sont à noter:  
AppView contient une propriété _el_. Cette propriété référence un objet DOM créé dans le navigateur. Chaque vue en possède un. Nous utilisons jQuery pour affecter cet propriété à l&rsquo;élément _body_.

Dans la méthode _render_, nous utilisons la propriété _el_ pour afficher Hello World directement dans la page, via jQuery. Facile ! 

Enfin, AppView implémente lA méthodes _initialize_. Cette méthode fait office de constructeur: elle est appelée lors de l&rsquo;instanciation (qui a lieu dans la ligne var appView = new AppView();).  
Elle appelle la méthode render pour afficher notre « Hello world », mais appelle également _.bindAll. Cela nous permet de dire que dans la méthode _render_, l&rsquo;élément this correspond à l&rsquo;objet AppView courant. Toutes les méthodes qui veulent utiliser l&rsquo;élément _this_ de cette manière doivent être présentes dans la liste de méthodes de bindAll.

<code lang="javascript">&lt;br />
&lt;br />
</code>

La démo de cet exemple [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part1/part1.htm).

Si on exécute ce bout de code&#8230; Tada ! On a fait un hello world !

## Bonne pratique: utiliser les template

Allons maintenant un peu plus loin. Je vais profiter que le bout de code soit très simple, pour vous parler de template. Ca n&rsquo;est pas nécessaire dans l&rsquo;exemple actuel, mais va nous permettre d&rsquo;aller plus rapidement par la suite, vu qu&rsquo;on va pas mal s&rsquo;en servir, et de commencer à prendre les bonnes habitudes que nous cherchons à avoir. En l&rsquo;occurence, la bonne habitude, c&rsquo;est séparer la logique, les données, et l&rsquo;affichage.  
Dans cet exemple, la logique, c&rsquo;est la méthode render. Elle ne fait rien qu&rsquo;afficher des données, mais elle pourrait contenir des traitements. Par contre, l&rsquo;affichage mélange les données (« Hello world ») avec la manière dont elles doivent être affichées (entre des tags <h1>). On va séparer ça.  
Un template, c&rsquo;est un modèle d&rsquo;affichage. On lui donne un nom, une structure HTML, et plus loin on s&rsquo;en sert dynamiquement pour remplir son contenu avec des données.

Backbone dépend d&rsquo;Underscore, qui propose une solution de templating qui va nous suffire. Sachez qu&rsquo;il en existe de nombreuses autres, tels que [mustachejs](http://mustache.github.com/) ou bien [Handlebarsjs](http://handlebarsjs.com/).

On va donc créer un template, en rajoutant ce bout de code avant la balise <script> de notre Hello world précédent :  
<code lang="html">&lt;br />
&lt;br />
</code>  
Notre template a un _id_ « helloTemplate » qui va nous permettre de récupérer son contenu par la suite. La partie originale, c&rsquo;est  
<%= content %>  
Qui veut dire « affiche moi le contenu de la variable content ». C&rsquo;est quoi content ? c&rsquo;est une variable que nous allons passer en argument au template !

On peut maintenant modifier la méthode _render_. ce que l&rsquo;on va y faire, c&rsquo;est récupérer notre template, lui fournir des données, et afficher le contenu.  
<code lang="javascript">&lt;br />
render: function(){&lt;br />
	var helloTemplate = _.template ($("#helloTemplate").html());&lt;br />
	$(this.el).append(helloTemplate ({'content':'Hello World'}));&lt;br />
}&lt;br />
</code>

Sauvegardez puis lancez votre nouveau bout de code&#8230; et Hello world est toujours affiché, rien n&rsquo;a changé. C&rsquo;est normal, nous avons juste refactoré notre code 🙂

La démo de cet exemple [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part1/part1_2.htm).

A noter que notre donnée, c&rsquo;est ici « Hello world », et qu&rsquo;elle n&rsquo;est pas vraiment séparée de la logique d&rsquo;affichage. Une chose à la fois, on va revenir la dessus dans les parties qui suivent, en parlant du modèle.