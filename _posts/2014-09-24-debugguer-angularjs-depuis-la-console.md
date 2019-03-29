---
id: 740
title:
  - Débugguer AngularJS depuis la console
date: 2014-09-24T12:13:23+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=740
permalink: /2014/09/24/debugguer-angularjs-depuis-la-console/
keywords:
  - javascript, angularJS, debug
description:
  - Astuce pour débugguer AngularJS depuis la console
robotsmeta:
  - index,follow
categories:
  - AngularJS
  - Astuce
  - Javascript
tags:
  - AngularJS
  - debug
  - javascript
lang: fr
---
Quelques astuces testées sur le terrain pour débugguer une application angularJS sans quitter le navigateur.

Dans chrome, on ouvre la console avec **F12** ou **ctrl+maj+j**. Couplé au fait que l&rsquo;on peut modifier le code et le faire rejouer directement depuis les outils pour développeurs, cela permet de débugger/corriger rapidement son code sans avoir à recharger la page systématiquement, ce qui est parfois très pratique.

## Récupérer un service

Des fois un service en cours de développement ne marche pas comme il faut et c&rsquo;est pas toujours marrant de devoir recharger la page à chaque modification pour déclencher à nouveau l&rsquo;appel en question et le débugger. Par contre, on peut récupérer le service avec la méthode ci-dessous, modifier en direct la méthode depuis l&rsquo;onglet « sources » de chrome dev tools, et lancer l&rsquo;exécution à la main de la méthode réticente.

<code lang="javascript">&lt;br />
var service = angular.element('body').injector().get('myService');&lt;br />
service.maMethodeARelancer("plop");&lt;br />
</code>

A mettre entre toutes les mains. Depuis que j&rsquo;ai découvert ça, je ne peux plus m&rsquo;en passer.

## Récupérer un scope local

Des fois on a besoin de récupérer le scope sous un contrôleur, que ce soit pour voir le contenu d&rsquo;une variable à un instant particulier. Pour ce cas d&rsquo;usage, la plupart du temps le débuggueur est plus pratique.  
Par contre, quand on veut appeler une action de controlleur présente dans le scope, c&rsquo;est très pratique.

Il faut connaitre le sélecteur DOM de l&rsquo;élément du DOM dans lequel se trouve le scope auquel ou souhaite accéder.  
<code lang="javascript">&lt;br />
var scope = angular.element('[ui-view=panel-communication]').scope()&lt;br />
</code>  
Ensuite, on peut accéder aux propriétés accessibles dans ce scope, et appeler les méthodes que l&rsquo;on souhaite.

<code lang="javascript">&lt;br />
scope.unMethodeARelancer("pouet")&lt;br />
scope.UnAttributQueJePeuxRegarderPlusFacilementDansLeDebuggueur&lt;br />
</code>

## Débugger les directives

Il est parfois d&rsquo;accéder au scope local à la directive, qui ont un don assez fou pour ne pas contenir les valeurs que l&rsquo;on croit, les rendant particulièrement pénibles à débugger.

<code lang="javascript">&lt;br />
var localScope = angular.element('[ui-view=panel-communication]').localScope()&lt;br />
</code>

Certains directives ont un contrôleur, auquel on peut accéder, ce qui est un luxe qui peut vous faire gagner pas mal de temps et vous économiser nombre de dolipranes.  
<code lang="javascript">&lt;br />
var controller = angular.element('[ui-view=panel-communication]').controller()&lt;br />
</code>

Bon courage !