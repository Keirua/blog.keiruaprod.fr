---
id: 387
title:
  - 'Intro à Backbone.js – #5 : Modifier/supprimer des éléments'
date: 2012-05-18T08:40:04+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=387
permalink: /2012/05/18/intro-a-backbone-js-5-modifiersupprimer-des-elements/
archived: true
description:
  - "Ajout de fonctionnalités pour la modification/suppression d'éléments à notre application d'apprentissage de Backbone.js"
robotsmeta:
  - index,follow
categories:
  - Javascript
tags:
  - Backbone.js
  - Backbone.view
  - javascript
---
_Cet article fait partie d&rsquo;une série d&rsquo;articles d&rsquo;introduction à [Backbone.js](http://documentcloud.github.com/backbone/ "Backbone.js"), largement inspirée du tutoriel (en anglais) [Hello Backbone.js](http://arturadib.com/hello-backbonejs/ "Hello Backbone.js"). Les bouts de code du tutoriel original ont été légèrement refactorés._

Dans cette dernière partie, nous allons ajouter des actions à la vue de chaque item, sans modifier l&rsquo;application, afin de pouvoir supprimer des éléments ou inverser les valeurs de part1 et part2. Pour cela, nous allons tirer partie du refactoring de la partie précédente, afin d&rsquo;ajouter la code là où cela a du sens.

## Modification de l&rsquo;ItemView

L&rsquo;avantage d&rsquo;avoir une vue dédiée pour l&rsquo;affichage des item (ItemView) comme nous l&rsquo;avons vu dans la partie précédente, c&rsquo;est que l&rsquo;on peut maintenant lui faire gérer la logique spécifique à notre vue. En l&rsquo;occurence, nous allons ajouter la gestion d&rsquo;opérations qui ont lieu au niveau des éléments la liste : la suppression d&rsquo;un élément, ou la modification de l&rsquo;un d&rsquo;entre eux.  
<!--more-->

  
Commencons pour ajouter 2 « boutons » à notre template d&rsquo;item, qui déclencheront les nouvelles actions :  
<code lang="html">&lt;br />
&lt;br />
</code>

Et maintenant, plus qu&rsquo;à écouter les évènements correspondant au clic sur chacun des boutons, et effectuer les opérations correspondantes.  
Il est nécessaire de surcharger Backbone.sync, la méthode de stockage persistant, par une coquille vide, afin d&rsquo;éviter les erreurs, vu que l&rsquo;on appelle model.destroy(); Dans un exemple plus complet, cette méthode est celle qui se charge de persister votre modele, soit dans un localStorage (sorte de stockage des données javascript client, plus évolué que les cookies), soit dans votre base de données, via une requete Ajax vers une page dédiée de votre serveur.

Dans la méthode initialize, on associe les évènements change et remove à nos méthodes d&rsquo;affichage et de suppression de la vue: render affiche notre donnée grâce au template associé au modele, et unrender supprime l&rsquo;élément créé.  
Swap se charge d&rsquo;inversion part1 et part2. l&rsquo;appel de set déclenche l&rsquo;évènenemt « change », qui entraine un réaffichage. Pour la suppression, on utilise la méthode model.destroy pour supprimer l&rsquo;élément de sa collection.

<code lang="javascript">&lt;br />
Backbone.sync = function(method, model, success, error){&lt;br />
	success();&lt;br />
}&lt;/p>
&lt;p>var ItemView = Backbone.View.extend({&lt;br />
	tagName: 'li',&lt;/p>
&lt;p>	events: {&lt;br />
	  'click span.swap':  'swap',&lt;br />
	  'click span.delete': 'remove'&lt;br />
	}, &lt;/p>
&lt;p>	initialize: function(){&lt;br />
	  _.bindAll(this, 'render', 'unrender', 'swap', 'remove');&lt;/p>
&lt;p>	  this.itemTemplate = _.template($('#itemTemplate').html());&lt;/p>
&lt;p>	  this.model.bind('change', this.render);&lt;br />
	  this.model.bind('remove', this.unrender);&lt;br />
	},&lt;/p>
&lt;p>	render: function(){&lt;br />
		$(this.el).html(this.itemTemplate({item:this.model}));&lt;/p>
&lt;p>	  return this;&lt;br />
	},&lt;/p>
&lt;p>	unrender: function(){&lt;br />
	  $(this.el).remove();&lt;br />
	},&lt;/p>
&lt;p>	swap: function(){&lt;br />
	  var swapped = {&lt;br />
		part1: this.model.get('part2'),&lt;br />
		part2: this.model.get('part1')&lt;br />
	  };&lt;br />
	  this.model.set(swapped);&lt;br />
	},&lt;/p>
&lt;p>	remove: function(){&lt;br />
		if (confirm ('Etes vous sur de vouloir supprimer cet element ?'))&lt;br />
			this.model.destroy();&lt;br />
	}&lt;br />
});&lt;br />
</code>

Comme dans les précédents articles, une démo [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part5/part5.htm).

Cette série d&rsquo;articles d&rsquo;introduction a Backbone.js est terminée, et devrait maintenant vous permettre d&rsquo;attaquer plus sereinement le tutoriel « officiel » [Todos.js](http://documentcloud.github.com/backbone/docs/todos.html). Et si vous trouvez que Backbone en fait un peu trop pour vos besoins, peut-être pouvez vous utiliser une autre librairie pour faire du MVC côté client ? Dans ce cas, je vous suggère de jeter un coup d&rsquo;oeil du côté de [TodoMVC](http://addyosmani.github.com/todomvc/), plusieurs tutoriels sur comment faire du MVC avec les framework javascript les plus populaires.