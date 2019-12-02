---
id: 363
title:
  - 'Intro à backbone.js - #2 : les évènements'
date: 2012-05-09T17:35:32+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=363
permalink: /2012/05/09/intro-a-backbone-js-2-les-evenements/
archived: true
keywords:
  - Backbone.js, backbone, javascript, mvc, évènement, event
description:
  - Introduction à la gestion des évènements dans une vue avec Backbone.js
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Javascript
tags:
  - backbone
  - Backbone.js
  - évènement
  - event
  - javascript
  - MVC
---
_Cet article fait partie d&rsquo;une série d&rsquo;articles d&rsquo;introduction à [Backbone.js](http://documentcloud.github.com/backbone/ "Backbone.js"), largement inspirée du tutoriel (en anglais) [Hello Backbone.js](http://arturadib.com/hello-backbonejs/ "Hello Backbone.js"). Les bouts de code du tutoriel original ont été légèrement refactorés._

Dans cet exemple, nous allons voir comment associer des évènements DOM à une vue.

## Les évènements

Il est possible de faire écouter à nos vues les différents évènements du DOM, et leur faire exécuter des actions en conséquence. Pour celà, il suffit d&rsquo;enregister les évènements dans la propriété _events_ de la vue, en précisant un sélecteur, ainsi que quelle méthode appeler. Exemple très court où l&rsquo;on ajoute un bouton, et lors du clic sur ce bouton on appelle la méthode _btnClick_, qui ouvre une boite de message. J&rsquo;ai enlevé presque tout le code, pour ne garder que l&rsquo;essentiel :  
<!--more-->

  
<code lang="javascript">&lt;br />
&lt;body>&lt;br />
	&lt;button>Cliquez !&lt;/button>&lt;/p>
&lt;p>	&lt;br />
&lt;/body>&lt;br />
</code>

Une démo de cet exemple [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part2/part2.htm "Gestion du clic sur un bouton dans une vue").

Le sélecteur est ici très général : n&rsquo;importe quel clic sur un bouton déclencherait l&rsquo;appel à btnClick. De plus, on référence ici l&rsquo;évènement click, mais de nombreux autres évènements sont disponibles (mouseover, dblclick&#8230;).

## Tout ensemble

On va reprendre un peu tout ce que l&rsquo;on sait pour le moment, pour avoir du code avec des évènements, une vue, et des template. Dans les partie qui vont suivre, nous allons faire évoluer ce bout de code pour ajouter des fonctionnalités, dans l&rsquo;esprit Backbone.js. Ce bout de code crée une page avec un bouton, et une liste vide. Lorsque l&rsquo;on clique sur le bouton, des éléments sont ajoutés dans la liste, et sont affichés.

<code lang="javascript">&lt;br />
&lt;body>&lt;/p>
&lt;div id="item_list">
	&lt;button id='add'>Ajouter un element&lt;/button>&lt;/p>
&lt;ul>&lt;/ul>
&lt;/div>
&lt;p>&lt;/p>
&lt;p>&lt;br />
&lt;/body>&lt;br />
</code>

Une démo de cet exemple [est disponible ici](http://keiruaprod.fr/hellobackbone-fr/part2/part2_2.htm "Notre application, à faire évoluer"). Dans la prochaine partie, on va parler du modèle.