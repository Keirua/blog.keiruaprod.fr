---
id: 379
title:
  - 'Intro à Backbone.js - #4 : Séparation des vues'
date: 2012-05-15T06:29:07+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=379
permalink: /2012/05/15/intro-a-backbone-js-4-separation-des-vues/
archived: true
keywords:
  - Backbone.js, Backbone.view, javascript
description:
  - Séparation des vues avec backbone.js
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Javascript
tags:
  - Backbone.js
  - Backbone.view
  - javascript
---
_Cet article fait partie d&rsquo;une série d&rsquo;articles d&rsquo;introduction à [Backbone.js](http://documentcloud.github.com/backbone/ "Backbone.js"), largement inspirée du tutoriel (en anglais) [Hello Backbone.js](http://arturadib.com/hello-backbonejs/ "Hello Backbone.js"). Les bouts de code du tutoriel original ont été légèrement refactorés._

On va reprendre l&rsquo;exemple précédent, et le refactorer, afin de déléguer le rendu de notre modèle dans une vue dédiée. Cela va nous permettre de gagner en flexibilité pour manipuler les données au niveau atomique (au niveau des éléments du modèle), ce que nous ferons par la suite. Du point de vue fonctionnalité par contre, rien ne va changer : nous allons simplement améliorer la qualité du code.  
<!--more-->

## Création d&rsquo;une vue dédiée pour le modèle

Pour commencer, nous allons créer une vue dédiée _ItemView_ pour l&rsquo;affichage de notre modèle. Pour le moment, elle se contente de faire le lien entre notre modèle et son template. Vous pouvez noter que render() renvoit this, ce qui permet de chainer les appels :

<code lang="javascript">&lt;br />
var ItemView = Backbone.View.extend({&lt;br />
tagName: 'li', // name of (orphan) root tag in this.el&lt;br />
initialize: function(){&lt;br />
  _.bindAll(this, 'render'); // every function that uses 'this' as the current object should be in here&lt;br />
},&lt;br />
render: function(){&lt;br />
  $(this.el).html('&lt;span>'+this.model.get('part1')+' '+this.model.get('part2')+'&lt;/span>');&lt;br />
  return this;&lt;br />
}&lt;br />
});&lt;br />
</code>

Maintenant, il faut modifier AppView, car ce n&rsquo;est plus la méthode addItemToView qui est chargée de l&rsquo;affichage des Item. On délègue l&rsquo;affichage à la classe que l&rsquo;on vient de créer.  
<code lang="javascript">&lt;br />
addItemToView :  function (item){&lt;br />
	var itemView = new ItemView({&lt;br />
		model: item&lt;br />
	  });&lt;br />
	$('ul', self.el).append(itemView.render().el);&lt;br />
}&lt;br />
</code>

Une démo de ce code d&rsquo;exemple [est visible ici](http://keiruaprod.fr/hellobackbone-fr/part4/part4.htm).

Et voila ! On peut maintenant ajouter des fonctionnalités à notre ItemView sans toucher au code de l&rsquo;application. C&rsquo;est ce que nous ferons dans la prochaine partie du tutoriel, pour supprimer ou modifier les éléments.