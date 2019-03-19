---
id: 800
title:
  - Les checkboxes avec AngularJS
date: 2015-04-06T11:40:03+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=800
permalink: /2015/04/06/les-checkboxes-avec-angularjs/
keywords:
  - angularJS, checkbox, checklist-model, directive,
description:
  - Les checkboxes avec AngularJS
robotsmeta:
  - index,follow
categories:
  - AngularJS
tags:
  - AngularJS
  - checkbox
  - checklist-model
  - directive
---
Gérer les cases à cocher avec **[angularJS](https://angularjs.org/ "AngularJS")** est un peu plus compliqué que les autres associations. On ne peut pas simplement utiliser ng-model, il faut gérer la possibilité que plusieurs cases soient cochées et cela nécessite d&rsquo;implémenter cette logique métier.

Nous allons voir comment le faire **à la main**, puis à l&rsquo;aide de la directive **checklist-model**.

### Gérer la checkbox « à la main »

Le moyen le plus simple, c&rsquo;est d&rsquo;avoir un tableau des différentes possibilités, de boucler dessus. Pour chaque case à cocher, lors d&rsquo;un clic on va déclencher une action de contrôleur. On va également tester si la case est cochée ou non via une autre action de contrôleur. 

<code lang="html">&lt;/p>
&lt;ul class="checkboxes">
&lt;li ng-repeat="(key, text) in availableTypes">
        &lt;label>&lt;br />
            &lt;input type="checkbox"
                name="filterType"
                ng-click="toggleTypeSelection({{ key }})"
                ng-checked="isTypeChecked({{ key }})">&lt;br />
                {{ text }}&lt;br />
        &lt;/label>
    &lt;/li>
&lt;/ul>
&lt;p></code>

Il faut donc dans le contrôleur plusieurs choses :

  * Une liste des différentes possibilités (**availableTypes**)
  * La propriété qui va stocker le modèle (**types**) 
  * Une méthode pour dire si une case est cochée ou non (**isTypeChecked**)
  * Une méthode pour cocher les cases (**toggleTypeSelection**)

Le javascript associé contient donc ces quatres choses :

<code lang="javascript">&lt;br />
$scope.types = [];&lt;/p>
&lt;p>$scope.availableTypes = {&lt;br />
    'apple': 'Pomme',&lt;br />
    'peach': 'Peche',&lt;br />
    'pear':  'Poire'&lt;br />
}&lt;/p>
&lt;p>// Dit si une case est cochée&lt;br />
// en testant si le tableau types contient la propriété testée.&lt;br />
$scope.isTypeChecked = function(typeName){&lt;br />
    return $scope.types.indexOf(typeName) > -1;&lt;br />
}&lt;/p>
&lt;p>// Coche ou décoche une case&lt;br />
// en ajoutant ou supprimant une propriété du tableau types&lt;br />
$scope.toggleTypeSelection = function(typeName){&lt;br />
    if ($scope.isTypeChecked(typeName)) {&lt;br />
        var index = $scope.types.indexOf(typeName);&lt;br />
        $scope.types.splice(index, 1);&lt;br />
    }&lt;br />
    else {&lt;br />
      $scope.types.push(typeName);&lt;br />
    }&lt;br />
}&lt;br />
</code>

### Factorisation grâce à checklist-model

En fait, on se rend assez vite compte que les deux actions de contrôleur sont toujours les mêmes. Pour éviter de devoir la réécrire à chaque fois, on peut donc les **factoriser**, dans une directive ou un service. Plutôt que de le faire soi-même, il existe une directive, **[checklist-model](http://vitalets.github.io/checklist-model/ "checklist-model")** qui fait cela.

Le code HTML fait la même taille, mais la philosophie est différente. **checklist-model** devient l&rsquo;équivalent du classique ng-model, et **checklist-value** va devenir la propriété à ajouter au tableau types lorsque la case est cochée ou non. La directive peut également savoir si une case est cochée, en testant si le tableau du modèle contient cette propriété.

<code lang="html">&lt;/p>
&lt;ul class="checkboxes">
&lt;li ng-repeat="(key, text) in availableTypes">
        &lt;label>&lt;br />
            &lt;input type="checkbox"
                checklist-model="types"
                checklist-value="key">&lt;br />
                {{ text }}&lt;br />
        &lt;/label>
    &lt;/li>
&lt;/ul>
&lt;p></code>

Le contrôleurs devient beaucoup plus simple. Il n&rsquo;y a plus besoin d&rsquo;implémenter les logique d&rsquo;actions au clic, et pour tester si une case est cochée, c&rsquo;est géré par la directive. Il suffit de déclarer les différents tableaux :

<code lang="javascript">&lt;br />
$scope.types = [];&lt;/p>
&lt;p>$scope.availableTypes = {&lt;br />
    'apple': 'Pomme',&lt;br />
    'peach': 'Peche',&lt;br />
    'pear':  'Poire'&lt;br />
}&lt;br />
</code>