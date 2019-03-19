---
id: 372
title:
  - 'Intro à Backbone.js - #3 : le modèle'
date: 2012-05-10T06:26:32+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=372
permalink: /2012/05/10/intro-a-backbone-js-3-le-modele/
keywords:
  - Backbone.js, backbone, model, Backbone.Model, MVC, Javascript
description:
  - "Intro à Backbone.js, et à l'utilisation du modèle"
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Javascript
tags:
  - backbone
  - Backbone.js
  - Backbone.Model
  - javascript
  - model
  - MVC
---
_Cet article fait partie d&rsquo;une série d&rsquo;articles d&rsquo;introduction à [Backbone.js](http://documentcloud.github.com/backbone/ "Backbone.js"), largement inspirée du tutoriel (en anglais) [Hello Backbone.js](http://arturadib.com/hello-backbonejs/ "Hello Backbone.js"). Les bouts de code du tutoriel original ont été légèrement refactorés._

Dans cette partie, nous allons voir comment créer une collection de modèles pour stocker les données, et les associer à une vue.

## Le modèle

Les choses sérieuses commencent. Nous allons créer notre premier modèle. Un modèle, c&rsquo;est dont une structure de donnée qui représente les informations que l&rsquo;on va manipuler. Dans la partie précédente, nous n&rsquo;avons pas créé de modèle matériellement : lors d&rsquo;un clic, nous avons ajouté un élément au DOM, mais nous n&rsquo;avons pas vraiment de trace de ce qui est fait. Si nous souhaitons par la suite manipuler les données, les choses peuvent devenir un peu compliquées.  
Afin de garder un trace de ce que nous manipulons, nous allons créer un modèle qui représente les éléments de la liste que nous avions affiché précédemment. Afin de rester simple, nous allons faire que chaque élément contienne 2 propriétés, part1 et part2, qui stockeront chacunes un mot.

Accrochez vous bien, ça va aller très vite :  
<code lang="javascript">&lt;br />
var Item = Backbone.Model.extend({&lt;br />
  });&lt;br />
</code>  
<!--more-->

  
Normalement, vous devriez trouver que ce bout de code est un peu vide. Où sont part1 et part2 ? Il n&rsquo;y a pas besoin de les déclarer. En javascript, il n&rsquo;y a pas besoin de déclarer les variables. On pourrait très bien créer une instance d&rsquo;Item et affecter la propriété part1 directement, cela ne sera pas un souci. On pourrait même aller chercher directement les données via de l&rsquo;ajax et remplir une liste&#8230; tiens, c&rsquo;est ce que font pas mal de gens. Mais je dérive; pour le moment, on va quand même affecter des valeurs par défaut à part1 et part2:

<code lang="javascript">&lt;br />
var Item = Backbone.Model.extend({&lt;br />
	defaults: {&lt;br />
	  part1: 'Hello',&lt;br />
	  part2: 'world '&lt;br />
	}&lt;br />
  });&lt;br />
</code>

Si c&rsquo;est nécessaire, vous pouvez également rajouter une méthode initialize, qui comme pour les vues, embarque de la logique lors de l&rsquo;instanciation.

## Manipuler les propriétés du modèle

Il est très facile d&rsquo;accéder aux propriétés. Il faut pour cela utiliser les méthodes get et set, dont l&rsquo;utilisation est résumée dans l&rsquo;exemple qui suit. get renvoit la valeur associée à une propriété, et set permet d&rsquo;affecter une ou plusieurs valeurs.  
<code lang="javascript">&lt;br />
var myItem = new Item();&lt;br />
myItem.set({part1 : "Salut"});&lt;br />
alert( myItem.get("part2") );&lt;br />
</code>

## La collection

Un collection, c&rsquo;est tout simplement une liste d&rsquo;objets correspondant au modèle donné. Ca va nous permettre de manipuler notre liste. On crée une collection spéficique en référencant le modèle d&rsquo;éléments auquel elle est associée, comme vous pouvez le voir :

<code lang="javascript">&lt;br />
var List = Backbone.Collection.extend({&lt;br />
	model: Item&lt;br />
  });&lt;br />
</code>

## L&rsquo;application

Je mets tout à la fois, car au fond, peu de choses changent.

<code lang="javascript">&lt;br />
var AppView = Backbone.View.extend({&lt;br />
	el: $('div#item_list'),&lt;br />
	events: {&lt;br />
	  'click button#add': 'addItem'&lt;br />
	},&lt;/p>
&lt;p>	initialize: function(){&lt;br />
	  _.bindAll(this, 'render', 'addItem', 'addItemToView'); // Toutes les fonction qui utilisent 'this' en tant que l'objet courant doivent être présentes ici&lt;br />
	  this.collection = new List();&lt;br />
	  this.collection.bind('add', this.addItemToView); // On enregistre une méthode à appeler lors de l'évènement 'add'&lt;/p>
&lt;p>	  this.itemTemplate = _.template($('#itemTemplate').html());&lt;br />
	  this.counter = 0;&lt;br />
	  this.render();&lt;br />
	},&lt;br />
	render: function(){&lt;br />
	  var self = this;&lt;br />
	  _(this.collection.models).each(function(item){&lt;br />
		addItemToView(item);&lt;br />
	  }, this);&lt;br />
	},&lt;/p>
&lt;p>	addItem: function(){&lt;br />
	  this.counter++;&lt;br />
	  var item = new Item();&lt;br />
	  item.set({&lt;br />
		part2: item.get('part2') + this.counter&lt;br />
	  });&lt;br />
	  this.collection.add(item); // On ajoute un élément -> déclenche un evenement "add"&lt;br />
	},&lt;/p>
&lt;p>	addItemToView :  function (item){&lt;br />
		$('ul', self.el).append(this.itemTemplate({'item': item}));&lt;br />
	}&lt;br />
  });&lt;br />
</code>

Une démo de cet exemple [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part3/part3.htm "Demo du modele dans Hello backbone").

Pour commencer, on fait pointer la propriété el de notre vue sur le _div_ contenant notre liste.

La gestion dest évènements fonctionne d&rsquo;une manière un peu particulière. Il est en effet possible d&rsquo;écouter les évènements qui altère notre collection. Vous pouvez noter que dans initialize, on instancie une liste, et qu&rsquo;on associe l&rsquo;évènement _add_ de la collection à la méthode addItemToView :  
<code lang="javascript">&lt;br />
this.collection.bind('add', this.addItemToView);&lt;br />
</code>  
Cela veut dire que lorsque notre liste déclenche un évènement _add_, il faut appeler la méthode addItemToView. Quand la liste va-t-elle déclencher un évènement add ? Lorsque l&rsquo;on appelle la méthode&#8230; add sur la collection. Et ceci arrive lorsque l&rsquo;on clique sur le bouton, qui appelle alors la méthode addItem. 

Vous pouvez également remarquer que dans la méthode render, on sauvegarder dans la variable self une référence vers this. En effet _.each, qui nous permet d&rsquo;itérer sur la liste, prend en arguement la méthode à appliquer à chacun des éléments de la liste. A l&rsquo;intérieur de cette méthode, l&rsquo;objet this correspond à la fonction dynamique, et non à l&rsquo;objet correspondant à la vue, d&rsquo;où la nécessité de le sauvegarder pour s&rsquo;en servir.

Le reste, c&rsquo;est du code déjà vu.