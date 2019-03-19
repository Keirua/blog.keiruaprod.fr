---
id: 666
title:
  - "L'héritage de contrôleurs avec AngularJS "
date: 2013-09-24T07:25:50+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=666
permalink: /2013/09/24/lheritage-de-controleurs-avec-angularjs/
keywords:
  - javascript, angularJS, inheritance, héritage, controller, contrôleur
description:
  - "Comment effectuer de l'héritage de contrôleurs en javascript avec AngularJS"
robotsmeta:
  - index,follow
categories:
  - AngularJS
  - Astuce
  - Bonnes pratiques
  - Javascript
tags:
  - AngularJS
  - controleur
  - controller
  - héritage
  - inheritance
  - javascript
---
Lorsque l&rsquo;on souhaite écrire du code concis, l&rsquo;héritage permet de gagner du temps en factorisant le code dans une classe dont plusieurs vont hériter, et se partager les fonctionnalités.

Dans une application [AngularJS](http://angularjs.org/ "AngularJS"), il est donc régulièrement nécessaire de faire hériter dans un contrôleur les fonctionnalités d&rsquo;un contrôleur de base. Je ne parle pas ici d&rsquo;imbrication, c&rsquo;est-à-dire d&rsquo;un « gros » contrôleurs dont une sous partie du DOM est gérée par un ou plusieurs autres contrôleurs, en charge de fonctionnalités restreintes localement. Je vais parler d&rsquo;héritage au sens objet du terme, bien que cette notion soit un peu floue en JavaScript (j&rsquo;entends déjà les puristes du fond qui hurlent, mais ça n&rsquo;est pas l&rsquo;objet de cet article).

L&rsquo;héritage de contrôleurs est par exemple utile pour une application de type CRUD, où les divers contrôleurs vont vouloir réaliser des opérations similaires sur différents modèles, avec des particularités pour chacun d&rsquo;entre elles. On va donc vouloir mettre l&rsquo;essentiel des fonctionnalités partagées dans un contrôleur de base, et fournir le comportement spécifique dans les fils.

Voici comment je fais pour faire hériter des propriétés, des méthodes, le scope et ce qu&rsquo;il surveille d&rsquo;un contrôleur de base vers des contrôleurs fils. Tout part d&rsquo;un contrôleur de base.

<code lang="javascript">&lt;br />
var BaseController = function($scope, DataStorage) {&lt;br />
    this.scope = $scope;&lt;br />
    this.DataStorage = DataStorage;&lt;br />
    this.scope.pageNb = 1;&lt;/p>
&lt;p>    var me = this;&lt;br />
    this.scope.$watch ('pageNb', function() {&lt;br />
        me.getList();&lt;br />
        me.scope.isAllselected = false;&lt;br />
    });&lt;/p>
&lt;p>    this.scope.displayCreationPopup = _.bind (this.displayCreationPopup, this);&lt;br />
    this.scope.hideCreationPopup    = _.bind (this.hideCreationPopup, this);&lt;/p>
&lt;p>    this.scope.showCreationPopup    = false;&lt;br />
}&lt;/p>
&lt;p>BaseController.prototype.displayCreationPopup = function (){&lt;br />
    this.scope.showCreationPopup = true;&lt;br />
}&lt;/p>
&lt;p>BaseController.prototype.hideCreationPopup = function (){&lt;br />
    this.scope.showCreationPopup = false;&lt;br />
}&lt;br />
</code>

Plusieurs choses sont à noter :  
&#8211; Je définis les propriété (objets et fonctions) à faire hériter dans le prototype. Le prototype définit toutes les propriété communes à toutes les instances de BaseController. C&rsquo;est donc très bien pour nous dans le cas présent, mais il faut faire attention à ce que l&rsquo;on met dedans, ce n&rsquo;est pas toujours ce que l&rsquo;on va vouloir.  
&#8211; Bien qu&rsquo;il s&rsquo;agisse d&rsquo;un contrôlleur, on ne l&rsquo;enregistre pas via angular.module(&#8230;).controller. En effet, c&rsquo;est notre classe abstraite, elle ne contient pas le code métier que l&rsquo;on souhaite exécuter tel quel, et ne contient pas à proprement parler de code complet.  
&#8211; D&rsquo;ailleurs, dans $scope.$watch, on fait appel à la méthode getList() qui n&rsquo;est pas définie ! Je la définis plus tard, dans les contrôlleurs fils. Mais afin d&rsquo;éviter de la duplication de code, comme tous les controlleurs font appel à getList lors d&rsquo;un changement de numéro de page, le code métier correspondant est écrit ici.  
&#8211; Je fournis le $scope en paramètres du contrôlleur de base, et un service de stockage. Comme le code n&rsquo;est pas exécuté tel quel, DataStorage n&rsquo;a pas besoin d&rsquo;être un vrai service (en fait, il n&rsquo;a même pas besoin d&rsquo;être défini). Tous ce dont on a besoin, c&rsquo;est d&rsquo;avoir une variable dans laquelle appeler des méthodes. En java ou autre, on aura un type plus précis sur cette variablee, afin d&rsquo;éviter de pouvoir y mettre n&rsquo;importe quoi. Dans les divers classes filles, nous injecterons un vrai service, dépendant du contrôlleur dont nous avons besoin afin d&rsquo;exécuter la logique métier.

Et maintenant, le code métier d&rsquo;un exemple de classe fille.

<code lang="javascript">&lt;br />
// On hérite le contrôleur de celui de base.&lt;br />
var NewsController = function($scope, NewsStorage, $injector) {&lt;br />
    $injector.invoke(BaseController, this, {$scope: $scope, DataStorage:NewsStorage});&lt;/p>
&lt;p>    this.scope.getList    = _.bind (this.getList, this);&lt;br />
    this.getList();&lt;br />
}&lt;br />
NewsController.prototype = Object.create (BaseController.prototype);&lt;/p>
&lt;p>// Une fonction quelconque de récupération de liste de news&lt;br />
// Exemple de ce qu'on pourrait avoir avec de l'asynchrone type requête Ajax :&lt;br />
NewsController.prototype.getList = function (){&lt;br />
    var me = this;&lt;br />
    this.scope.displayLoader = true;&lt;br />
    this.NewsStorage.getList (this.scope.pageNb, function(result){&lt;br />
            me.scope.news = result.data.news;&lt;br />
            me.scope.nbPages = result.data.nbPages;&lt;br />
            me.scope.displayLoader = false;&lt;br />
        }&lt;br />
    );&lt;br />
}&lt;/p>
&lt;p>// On injecte le contrôleur dans l'application&lt;br />
var module = angular.module ('myApp.controllers', ['common.controllers', 'common.stores', 'myApp.stores']);&lt;br />
module.controller('NewsController', [&lt;br />
    '$scope',&lt;br />
    'NewsStorage',&lt;br />
    '$injector',&lt;br />
    NewsController&lt;br />
]);&lt;br />
</code>

Les 2 lignes importantes d&rsquo;un point de vue de l&rsquo;héritage sont  
**$injector.invoke(BaseController, this, {$scope: $scope, DataStorage:NewsStorage});  
** et  
**NewsController.prototype = Object.create (BaseController.prototype);  
**  
La première injecte les données présentes dans le $scope du père (en lui fournissant au passage les bons services). Elle fournit aussi tout ce qui s&rsquo;y rattache : on conserve le $scope.$watch par l&rsquo;héritage.  
La seconde ligne étend le prototype, c&rsquo;est à dire qu&rsquo;elle duplique les méthodes dans le contrôlleur fils. Oui, c&rsquo;est du javascript, pas du C++ ou du Java hein, l&rsquo;héritage reste ici une notion un peu abstraite (haha).

Cette fois ci, le contrôleur News est bien injecté dans l&rsquo;application. On le configure, et on lui donne les bons services, c&rsquo;est eux qui sont fournis au père.  
On implémente la méthode getList(), que l&rsquo;on peut imaginer faire un appel ajax ou dans un cache quelconque (applicatif ou localstorage, soyons fous) pour récupérer les données nécessaires.

Vu que les méthodes sont héritées, depuis la vue, on peut donc appeler showCreationPopup() et hideCreationPopup(). On peut également utiliser les propriété du scope, et rajouter les nôtres.

Vous pouvez au passage remarquer que je bind régulièrement mes fonctions via la librairie underscore sur l&rsquo;objet this. Cela permet de ne pas perdre l&rsquo;objet contrôlleur lorsque les appels se font depuis angular, qui utilise comme objet d&rsquo;appel le $scope local et non le contrôlleur. Dans cet exemple, tous les bindings ne sont pas nécessaires, mais quand je fais un hideCreationPopup() depuis une vue, c&rsquo;est le binding dont je viens de parler qui fait qu&rsquo;on peut changer la valeur de showCreationPopup, et que ce changement se répercute sur la vue.

Cela permet d&rsquo;isoler le code récurrent dans une classe de base afin d&rsquo;en faciliter sa réutilisation, ce qui permet, pour les contrôleurs fils, de n&rsquo;implémenter que la logique spécifique.