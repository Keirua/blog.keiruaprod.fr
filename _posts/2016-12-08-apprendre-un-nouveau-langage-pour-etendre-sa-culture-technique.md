---
id: 832
title: Apprendre un nouveau langage pour étendre sa culture technique
date: 2016-12-08T13:11:25+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=832
permalink: /2016/12/08/apprendre-un-nouveau-langage-pour-etendre-sa-culture-technique/
robotsmeta:
  - index,follow
categories:
  - Bonnes pratiques
---
C&rsquo;est bientôt Noël. Et si vous vous faisiez le cadeau d&rsquo;apprendre quelque chose de radicalement nouveau, comme un nouveau langage de programmation ?

<!--more-->

## <a id="user-content-pourquoi-se-lancer-là-dedans" class="anchor" href="#pourquoi-se-lancer-l%C3%A0-dedans" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Pourquoi se lancer là dedans

Il y a un an, j&rsquo;ai quitté mon travail pour [voyager pendant un an](http://fragmentsdeplanete.fr/). Ce voyage a été l&rsquo;occasion de prendre du recul sur beaucoup de choses dans la vie, dont la place qu&rsquo;occupe mon métier de développeur et la manière dont je le pratique.

J&rsquo;ai fait le constat que je faisais beaucoup de veille, passive comme active, mais essentiellement dans le domaine du web. C&rsquo;est bien pour avoir une bonne vision des possibilités offertes par un écosystème, mais pas suffisant pour avoir un esprit critique acéré. C&rsquo;est une des remarques que l&rsquo;on retrouve dans le très bon article [Hype Driven Development](https://blog.daftcode.pl/hype-driven-development-3469fc2e9b22#.1wywhgns2), publié récemment : les choix techniques sont souvent faits parce que les outils sont cools, un élément clé de décision dans de nombreux projets. Sur le long terme, ces choix se paient par cette vision d&rsquo;un plaisir court-termiste, un plaisir qui disparaît vite lorsque la découverte est passée ou que la technologie devient à sont tour dépassée. Une des solutions que propose l&rsquo;auteur, c&rsquo;est de s&rsquo;entourer des gens avec de fortes compétences techniques, qui connaissent notamment différents paradigmes, outils, méthodes. C&rsquo;est ce genre de personne que j&rsquo;aimerais devenir. Je vais vous parler de ce que j&rsquo;ai commencé : apprendre de nouveaux langages, pour étendre ma culture technique.

## <a id="user-content-apprendre-de-nouveaux-langages--quoi-pourquoi-" class="anchor" href="#apprendre-de-nouveaux-langages--quoi-pourquoi-" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Apprendre de nouveaux langages : quoi, pourquoi ?

On a tous des projets à côté qu&rsquo;on a jamais fait pour x raisons. Apprendre un nouveau langage est un bon moyen de les réaliser, tout en testant les limites du langage. J&rsquo;ai donc commencé à apprendre des langages pour réaliser ces projets que j&rsquo;avais en tête. Nous avons un tous un temps fini que l&rsquo;on peut consacrer à du développement (ou tout projet en général), autant faire des trucs intéressants.

J&rsquo;ai donc appris les langages qui me faisaient envie, dans l&rsquo;optique de me lancer des projets que je souhaitais réaliser. J&rsquo;ai commencé par le **Go**, langage populaire en ce moment, qui a l&rsquo;avantage et l&rsquo;inconvénient d&rsquo;être supporté par Google. J&rsquo;ai appris les bases du langage en lisant et refaisant les exemples du [Go by example](http://gobyexample.com/), que j&rsquo;ai d&rsquo;ailleurs, lors de mon apprentissage, [traduit en français](le-go-par-l-exemple.keiruaprod.fr/). Cette série d&rsquo;exemples permet de rentrer assez vite dans des spécificités du langage, et on progresse rapidement en la suivant.

Comme j&rsquo;avais envie d&rsquo;apprendre comment fonctionne le rendu 3D, j&rsquo;ai réalisé [**un raytracer**](https://github.com/keirua/Vertex). Il s&rsquo;agit d&rsquo;un programme qui calcule le rendu d&rsquo;une scène en 3D en calculant la lumière, les ombres, les reflets&#8230; de manière algorithmique. Go a de bonnes performances, ce qui fait de lui un bon candidat pour ce genre de projets. C&rsquo;était vraiment agréable et motivant de travailler dans quelque chose de vraiment différent de ce que je fais au quotidien. De plus, travailler sur un projet un peu gros m&rsquo;a permis de me faire une idée plus précise du langage : comment on organise un projet, constater dans quelle mesure la librairie standard est fournie (très bien !) et documentée (très mal !), comprendre certains des choix, apprendre à utiliser certains des outils, comme **go perf**, qui permet de profiler le temps d&rsquo;exécution. Le projet ne révolutionnera pas le monde de la 3D, mais je me suis éclaté.

J&rsquo;ai aussi commencé à apprendre le **Python**, langage élégant aimé, entre autres, par ceux qui font du traitement de données, de l&rsquo;apprentissage automatique, des réseaux de neurones. Je l&rsquo;ai appris en faisant les [**« Python Koans »**](https://github.com/gregmalcolm/python_koans), des exercices pour apprendre la syntaxe et les fonctionnalités du langage à travers des tests automatisés, grâce [au TDD](https://en.wikipedia.org/wiki/Test-driven_development#Test-driven_development_cycle). Avant de me lancer dans des projets de machine learning, j&rsquo;utilise aujourd&rsquo;hui ce langage pour découvrir la **cryptographie** grâce aux challenges de [**cryptopals**](http://cryptopals.com/). Le bilan est que ce n&rsquo;est pas si compliqué (la progression des challenges, que ce soit dans la difficulté ou la manière dont sont amenées les choses, est bien réalisée), et je découvre avec plaisir un pan de l&rsquo;informatique que je connais très mal.

Voici les choix que j&rsquo;ai fait, mais bien d&rsquo;autres seraient pertinents : le **haskell**, langage majeur de la programmation fonctionnelle, le **rust** pour sa manière de programmée hyper protégée, le **scala** pour voir l&rsquo;univers Java sous un angle différent&#8230; Les possibilités sont vraiment nombreuses. Prenez ceux qui vous branchent, et faites des trucs qui vous font envie avec.

## <a id="user-content-ne-pas-sarrêter-à-la-première-marche" class="anchor" href="#ne-pas-sarr%C3%AAter-%C3%A0-la-premi%C3%A8re-marche" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Ne pas s&rsquo;arrêter à la première marche

Quelques semaines sur un nouveau langage ne vont pas changer votre vision du métier tout de suite. Pour profiter pleinement de ses enseignements, il va falloir creuser plus le langage, faire des projets non-triviaux, comprendre les raisons des choix dans certaines librairies, peut-être écrire les votres&#8230; Bref, aller au delà de la simple découverte.

Pour le moment, je suis au début de l&rsquo;apprentissage. J&rsquo;ai une connaissance modeste des deux langages que j&rsquo;ai présenté. Il ne faut surtout pas s&rsquo;arrêter là pour avoir une bonne vision des choses. Clément Bouillier proposait il y a quelques semaines [un modèle de maturité](http://www.devcrafting.com/en/blog/2016/11-learn-new-language-platform/), inspiré par la pyramide des besoins de Maslow, pour décrire les différentes étapes de l&rsquo;apprentissage d&rsquo;un nouveau langage :

  1. Connaître la syntaxe élémentaire du langage
  2. Connaître les outils associés, les frameworks et les librairies
  3. Connaitre les pratiques
  4. Savoir faire des choix contextuels/délibérés : outils, frameworks, librairies, méthodes 

La première étape, c&rsquo;est de savoir survivre : connaître les types de base, les mots-clés (for, if, etc.), les fonctions les plus classiques de la librairie standard. Un fois qu&rsquo;on a cela, on progresse dans sa connaissance des outils, et de ce qu&rsquo;il y a autour du langage. En même temps (l&rsquo;idée de pyramide montre ici ses limites), on progresse dans les idiomes du langage. A terme, on maîtrise le langage quand on est capable de faire des choix argumentés entre les différentes possibilités en fonction du contexte.

Un autre moyen d&rsquo;apprendre, c&rsquo;est de d&rsquo;écrire et enseigner ses découvertes aux autres. Je me rends compte en en parlant que je n&rsquo;ai rien écrit sur python et Go sur ce blog, mais quand j&rsquo;ai appris Symfony il y a quelques années, les divers articles écrits sur le sujet m&rsquo;ont permis de mettre en forme ce que j&rsquo;apprenais et d&rsquo;être plus rigoureux dans ce que je retenais. Et cela a ouvert des horizons professionnels très intéressants auxquels je n&rsquo;avais pas pensé au départ (réalisation de formations, propositions de missions, rencontres, etc)

J&rsquo;ajouterais qu&rsquo;apprendre un langage de programmation est un moyen parmi tant d&rsquo;autres d&rsquo;élargir votre culture technique. Ce n&rsquo;est certainement pas la seule pour développer vos compétences ! En vous lançant dans quelque chose d&rsquo;encore plus différent (faire des pâtisseries, apprendre à dessiner, [construire des murs](http://gb-prod.fr/2016/06/12/artisan-developpeur.html)&#8230;), vous trouverez des connections avec votre métier. Ne vous forcez pas à apprendre des choses qui vous rebutent ceci-dit : faites le simplement car c&rsquo;est passionnant, et les pièces du puzzle finiront par s&rsquo;assembler sans que vous en preniez conscience.