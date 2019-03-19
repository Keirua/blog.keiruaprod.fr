---
id: 899
title: Quelques suggestions de livres pour développeurs
date: 2018-11-23T14:32:19+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=899
permalink: /2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/
robotsmeta:
  - index,follow
categories:
  - Non classé
lang: fr
---
J&rsquo;ai récemment eu l&rsquo;occasion de coacher des développeurs débutants. Ça a été l&rsquo;occasion pour moi de faire le point sur des notions de base mal comprises, et peut-être l&rsquo;occasion pour vous d&rsquo;apprendre de choses !

Ma présence touchait à sa fin, et l&rsquo;éventail des sujets qu&rsquo;il restait à aborder est trop grand pour une formation. J&rsquo;ai donc suggéré l&rsquo;achat de quelques livres, que vous trouverez reproduite et étendue ici. En effet, dans une boite précédente, nous avions accès à une petite bibliothèque technique, grâce à laquelle j&rsquo;ai appris plein de choses. J&rsquo;ai profité de mon passage freelance pour garder l&rsquo;habitude de m&rsquo;acheter environ un livre technique tous les 1/2 mois. Si vous ne pouvez/souhaitez pas les acheter vous-même (certains coutent un bras), **peut-être pourrez vous également demander à votre boss de faire l&rsquo;achat de quelques titres ?** Cela profitera à toute l&rsquo;équipe.

Il n&rsquo;y a pas que le travail dans la vie ! Souvent, les développeurs sont des passionnés. C&rsquo;est pourquoi j&rsquo;ai profité de cet article pour conseiller quelques titres qui m&rsquo;ont bien amusé.

Vous trouverez donc des suggestions sur:

  * [comment bosser sur des applications web complexes](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-bosser-sur-des-applications-web-complexes)
  * [comment bosser sur du code legacy](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-bosser-sur-du-code-dentreprise-de-mauvaise-qualité)
  * [comment écrire du code de qualité](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-apprendre-à-écrire-du-bon-code)
  * [des bouquins pour étoffer votre culture technique](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-quelques-bouquins-pour-étoffer-votre-culture-technique)
  * [des bouquins pour vous amuser avec du code](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-quelques-bouquins-pour-le-fun)
  * [des titres non techniques de non-fiction](http://blog.keiruaprod.fr/2018/11/23/quelques-suggestions-de-livres-pour-developpeurs/#user-content-quelques-histoires-de-non-fiction)

<!--more-->

# <a id="user-content-bosser-sur-des-applications-web-complexes" class="anchor" href="#bosser-sur-des-applications-web-complexes" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Bosser sur des applications web complexes

**Designing Data Intensive Applications, Martin Kleppmann**  
<a href="https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321/" rel="nofollow">https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321/</a>

Si vous ne devez acheter qu&rsquo;un bouquin pro, **prenez celui-la** (cette liste commence fort) !

Vous allez apprendre les grandes idées derrière les architectures web complexes solides et maintenables. On ne parle pas du comment configurer une BDD MySQL, mais d&rsquo;à quelles problématiques on va faire face lorsque ça se complexifie: montées en charge, plus de serveurs, etc&#8230; et bien sûr comment les résoudre. Même si on est familier avec les notions de loadbalancing, de message queue, de cdn, que vous avez une vague idée de ce que veut dire NoSQL&#8230; vous apprendrez plein de choses sur le fonctionnement de vos outils (les structures de données utilisées dans les bases de données par ex) et allez structurer vos connaissances concernant les systèmes distribués (réplication, partitionnement de cluster, problématiques de consensus, etc).

Attention, vous n&rsquo;<a href="http://blog.chorip.am/talk/vous-navez-pas-besoin-de-ca" rel="nofollow">aurez probablement pas besoin de tout ça</a> au quotidien, au moins pour démarrer un projet et pendant un long moment ! Faire simple vous rendra de très grands services.

**Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation**  
<a href="https://www.amazon.com/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912" rel="nofollow">https://www.amazon.com/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912</a>

Livrer des applications en continu, c&rsquo;est un élément clé de la qualité logicielle: la mettre en oeuvre va permettre de livrer plus souvent, d&rsquo;avoir des retours plus fréquents des utilisateurs, et de détecter plus finement l&rsquo;introduction de défauts dans l&rsquo;application.  
En contrepartie, cela demande pas mal d&rsquo;ingénierie pour le faire de manière sereine sur des gros projets: il faut monitorer le statut de l&rsquo;application, pouvoir identifier rapidement l&rsquo;apparition de défauts, avoir des tests automatisés avec parfois plusieurs niveaux de granularité, valider la qualité du code qui va être déployé, avoir un système de build du projet, plusieurs environnemens sur lesquels déployer&#8230; pas mal d&rsquo;étapes qui sont souvent manuelles, ou bien où l&rsquo;on trouve des frictions.

Ce bouquin, c&rsquo;est un bon moyen de comprendre comment s&rsquo;articulent tous ces éléments. Il aborde tous les grands principes de l&rsquo;intégration continue, de la gestion de projets aux outils de déploiements en passant par la gestion de configuration. Le but, c&rsquo;est d&rsquo;avoir toutes les cartes en main pour pouvoir mettre en place une stratégie de déploiement continu, en automatisant correctement tout ce qui doit l&rsquo;être, et en sachant pourquoi on le fait.

# <a id="user-content-bosser-sur-du-code-dentreprise-de-mauvaise-qualité" class="anchor" href="#bosser-sur-du-code-dentreprise-de-mauvaise-qualit%C3%A9" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Bosser sur du code legacy

Quand on arrive sur un vieux projet (souvent mal écrit), il y a deux grands problèmes:

  * se repérer, comprendre comment ça fonctionne
  * corriger les défauts fonctionnels tout en améliorant la qualité du code, et en s&rsquo;assurant que l&rsquo;on n&rsquo;introduit pas de régressions

On a tous, à un moment donné, du faire ce genre de choses: corriger un vieux projet pourri. Autour de moi, j&rsquo;ai souvent constaté une approche très primitive de ce genre de choses. Souvent, après avoir mal compris le bout de code à problèmes (souvent inscrit dans des objets/méthodes/domaines trop complexe pour être compris dans leur ensemble), on ajoute un peu de code autour du défaut pour le corriger, et s&rsquo;il y a des régressions on espère que ce sera pour le suivant. Il y a pourtant des méthodes qui permettent d&rsquo;appréhender les problèmes ci-dessus avec un peu plus de sérennité. Je vous conseille les deux livres suivants :

**<a href="https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052" rel="nofollow">Working effectively with legacy code</a>**, Michael Feathers

Une belle boite à outils pour apprendre à travailler dans des vieux projets, avec beaucoup de code, souvent de mauvaise qualité, s&rsquo;y repérer et arriver à changer des choses sans tout casser.

**<a href="https://martinfowler.com/books/refactoring.html" rel="nofollow">Refactoring</a>**, Martin Fowler

Le refactoring, c&rsquo;est un procédé que tous les dévelopeurs mettent en oeuvre à mesure que leur compréhension du domaine évolue, ou bien que le projet grandit. On en parle déja chez Feathers, mais pour Fowler, c&rsquo;est une idée clé de l&rsquo;agilité: améliorer ou corriger du code mal fichu, de manière itérative, permet aussi bien de corriger du vieux code que d&rsquo;améliorer rapidement du code nouveau. Une nouvelle édition est prévue pour fin 2018, avec des exemples en Javascript.

# <a id="user-content-apprendre-à-écrire-du-bon-code" class="anchor" href="#apprendre-%C3%A0-%C3%A9crire-du-bon-code" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Apprendre à écrire du bon code

Quelques questions à se poser, avant de chercher à y répondre plus rigoureusement : c&rsquo;est quoi du code de bonne qualité, qu&rsquo;est ce qui le caractérise, et comment écrire de manière consistante du code qui respecte ces règles ?

J&rsquo;ai du mal à vous conseiller des lectures papier. Vous avez peut-être déjà vu les titres qui suivent car ils sont populaires, mais pourtant leurs lectures ne m&rsquo;ont pas satisfaites:

  * **Code Complete** propose plein de bons conseils, mais&#8230; un peu trop. Avec 750 pages je ne vois pas du tout comment faire un lecture efficace de ce livre. Si vous le lisez en entier vous n&rsquo;en retiendrez rien. Si vous le lisez occasionnellement, penserez vous à lire un chapitre de temps en temps et à mettre en oeuvre ses conseils ? Ça n&rsquo;a pas été mon cas.
  * **The Clean Coder**, c&rsquo;est l&rsquo;inverse. 250 pages, mais une fois la table des matières lue, vous n&rsquo;apprendrez plus grand chose. C&rsquo;est pourtant un des livres fondateur du mouvement des artisans développeurs (software craftsmanship). Il se concentre plus sur l&rsquo;état d&rsquo;esprit du « bon » développeur (avec, par ailleurs, des idées très arrêtées et parfois très discutables, par exemple sur le temps que vous devriez consacrer à votre veille) que sur le code en lui même.

Un bouquin qui m&rsquo;a aidé à comprendre les idées derrière les implémentations de plusieurs framework web, c&rsquo;est **<a href="https://www.amazon.com/Patterns-Enterprise-Application-Architecture-Martin/dp/0321127420" rel="nofollow">Patterns of Enterprise Application Architecture</a>**, de Martin Fowler. Une sorte de dictionnaire du développement d&rsquo;entreprise, pour apprendre les structures qu&rsquo;on trouve un peu partout, et surtout les différences entre des idées proches (ex: data mapper chez Doctrine, active record chez Eloquent). Une version basique du <a href="https://www.martinfowler.com/eaaCatalog/" rel="nofollow">catalogue</a> est diponible en ligne.

A part ça, n&rsquo;hésitez pas à regarder de temps à autre comment sont structurées les librairies que vous utilisez fréquemment, et à vous tenir au courant des conventions récentes dans votre langage. Pour PHP, **<a href="https://eilgin.github.io/php-the-right-way/" rel="nofollow">PHP : the right way</a>** en fait la synthèse par exemple.

# <a id="user-content-quelques-bouquins-pour-étoffer-votre-culture-technique" class="anchor" href="#quelques-bouquins-pour-%C3%A9toffer-votre-culture-technique" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Quelques bouquins pour étoffer votre culture technique

The Pragmatic Bookshelf a deux séries de livres que j&rsquo;ai adoré. Bruce Tate a écrit **<a href="https://pragprog.com/book/btlang/seven-languages-in-seven-weeks" rel="nofollow">Seven Languages in Seven Weeks</a>** puis, suite au succès de ce premier livre, il a écrit une suite, **Seven More Languages in Seven Weeks**.

Dans ces deux livres, il présente au total 14 langages de programmation. Il y a des points communs, mais chacun a des particularités ou s&rsquo;articule autour d&rsquo;un paradigme. Le premier se lance dans des langages connus, mais je suis certain que vous n&rsquo;avez pas écrit du code dans tous ces langages :

  * Ruby
  * Io
  * Prolog
  * Scala
  * Erlang
  * Clojure
  * Haskell

L&rsquo;idée c&rsquo;est quand même de parler des concepts (paradigmes) derrière tous ces langages, plus que vous rendre opérationnel en quelques pages (mais les exercices vont vous apprendre à devenir autonomes, par ex en allant chercher des infos dans la documentation).

Le second livre s&rsquo;aventure sur des langages moins connus, et continue à les utiliser pour parler de différents paradigmes (fonctionnels, prototypal, gestion d&rsquo;échec, calcul scientifique, programmation logique, théorie des types):

  * Lua
  * Factor
  * Elm
  * Elixir
  * Julia
  * miniKanren
  * Idris

**<a href="https://pragprog.com/book/rwdata/seven-databases-in-seven-weeks" rel="nofollow">Seven Databases In Seven Weeks</a>** reprend cette logique d&rsquo;explorer plusieurs technos pour en expliquer les idées clé, mais côté base de données. Je pensais m&rsquo;ennuyer sur celles que je connaissais, mais le chapitre d&rsquo;intro sur PostgreSQL (que j&rsquo;ai utilisé dans plusieurs projet.) allait déjà au dela de mes connaissances. Au programme, du SQL, du NoSQL, des time series, des bases de données orienté graphe, des stores clé/valeur&#8230;:

  * PostgreSQL
  * Riak
  * HBase
  * MongoDB
  * CouchDB
  * Neo4J
  * Redis

Si vous aimez le style, il y a eu d&rsquo;autres titres dans le même genre chez cet éditeur que je n&rsquo;ai pas lus, comme **Seven Concurrency Models in Seven Weeks** ou **Seven Web Frameworks in Seven Weeks**.

# <a id="user-content-quelques-bouquins-pour-le-fun" class="anchor" href="#quelques-bouquins-pour-le-fun" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Quelques bouquins pour le fun

**<a href="http://www.mazesforprogrammers.com/" rel="nofollow">Mazes for Programmers</a>**

J&rsquo;ai su que j&rsquo;allais lire ce livre après en avoir lu la quatrième de couverture: « Remember when programming was fun? »

Ici, rien de compliqué, pas d&rsquo;objectif, on prend ce qu&rsquo;on souhaite au milieu d&rsquo;une multitude d&rsquo;algorithmes pour la génération et le rendu de labyrinthes en 2 et 3 dimensions. Je n&rsquo;ai pas réécrit tous les algorithmes, mais:

  * quand je l&rsquo;ai fait et que le labyrinthe s&rsquo;affiche correctement pour la première fois, on est vraiment, pleinement satisfait
  * simplement comprendre un algorithme qui parait complexe procure une grande satisfaction en soi.

**Nature of code**

Plein de techniques vaguement inspirées de la nature: moteur physique, fractales, systèmes de particules, etc. Très chouette.

Ce livre est disponible gratuitement <a href="https://natureofcode.com/book/" rel="nofollow">en ligne</a> (et honnêtement, j&rsquo;ai pris la version papier pour soutenir l&rsquo;auteur, mais la version web est plus pratique à lire. Elle contient d&rsquo;ailleurs des animations qui ne rendent pas bien sur papier)

**Raytracing in a Weekend**

<a href="http://in1weekend.blogspot.com/2016/01/ray-tracing-in-one-weekend.html" rel="nofollow">Peter Shirley</a> a écrit 3 livres sur le <a href="https://fr.wikipedia.org/wiki/Ray_tracing" rel="nofollow">raytracing</a>, une technique de rendu graphique qui sert (en gros ! pas taper !) pour le rendu des images d&rsquo;effets spéciaux et dans les films d&rsquo;animation.

  * Raytracing in One Weekend
  * Raytracing: The Next Weekend
  * Raytracing: The Rest Of Your Life

Comme leurs noms l&rsquo;indiquent, le but est d&rsquo;apprendre progressivement, mais rapidement au début, à concevoir son propre moteur de rendu. C&rsquo;est très ludique, ça se lit vit, on apprenl pleir de choses sur la 3D quand on est pas dans le domaine, et c&rsquo;est un super projet pour apprendre en même temps un nouveau langage.

Shirley a récemment rendu open source son livre et les code des projets, vous pourrez les trouver sur [Github](https://github.com/petershirley) ou sur <a href="http://www.realtimerendering.com/raytracing/" rel="nofollow">Real-Time Rendering</a>

Dans le même esprit, mais qui va beaucoup plus loin (j&rsquo;ai vite été largué faute d&rsquo;assiduité), le fantastique **<a href="http://www.pbr-book.org/" rel="nofollow">Physically-Based Rendering</a>** est également disponible en version web. Il peut vous occuper quelques années.

Je n&rsquo;ai pas encore lu, mais on m&rsquo;a vivement conseillé le titre de Fabien Sanglard <a href="http://fabiensanglard.net/Game_Engine_Black_Book_Release/index.php" rel="nofollow"><strong>Game Engine Black Book : Wolfenstein 3D</strong></a>. Au départ, Fabien a publié sur son site de longues revues de code de projets connus: <a href="http://fabiensanglard.net/quakeSource/index.php" rel="nofollow">Quake</a>, <a href="http://fabiensanglard.net/prince_of_persia/index.php" rel="nofollow">Prince Of Persia</a>, <a href="http://fabiensanglard.net/doom3/index.php" rel="nofollow">Doom 3</a>, <a href="http://fabiensanglard.net/git_code_review/index.php" rel="nofollow">git</a> et la liste continue. C&rsquo;était déja hyper intéressant et on apprend plein de choses sur la structure et les astuces de projets qui ont marqué l&rsquo;histoire, jetez-y un oeil ! Après plusieurs années de travail, il a publié le premier titre d&rsquo;une série papier encore plus détaillée sur les moteurs 3D, en commençant par Wolfenstein 3D.

# <a id="user-content-quelques-histoires-de-non-fiction" class="anchor" href="#quelques-histoires-de-non-fiction" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Quelques histoires de non fiction

Les titres qui suivent racontent des histoires réelles

  * **<a href="https://www.amazon.com/Countdown-Zero-Day-Stuxnet-Digital/dp/0770436196" rel="nofollow">Countdown to Zero Day: Stuxnet and the Launch of the World&rsquo;s First Digital Weapon</a>**. Une enquête autour du ver Stuxnet, qui a servi a casser les centrifugeuses d&rsquo;uranium Iranien afin de ralentir leur accès à l&rsquo;arme nucléaire. C&rsquo;est raconté autour de deux axes: le contenu absolument ahurissant du virus (qui contient des trésors d&rsquo;ingéniosité et de complexité), et ce qui se passe « dans le monde réel » autour du développement du nucléaire irannien. On se croirait dans un polar !
  * **<a href="https://www.amazon.fr/Ghost-Wires-Adventures-Worlds-Wanted/dp/0316212180" rel="nofollow">Ghost in The Wires</a>**. Autre histoire dingue, la bio de la période hacker du célèbre Kevin Mitnick, avant qu&rsquo;il ne se fasse arrêter pour de bon. On a du mal à tout croire (après tout, son expertise, c&rsquo;est le mensonge), mais on se laisse quand même porter. Certaines techniques d&rsquo;ingénierie sociale qu&rsquo;il met en oeuvre pour ses hacks sont encore utilisées aujourd&rsquo;hui.
  * **<a href="https://www.amazon.fr/Masters-Doom-Created-Transformed-Culture/dp/0812972155" rel="nofollow">Masters of Doom</a>**, l&rsquo;histoire derrière le développement de Doom par Carmack et son équipe au début des années 90. **<a href="https://www.amazon.fr/Creativity-Inc-Overcoming-Unseen-Inspiration/dp/055384122X/" rel="nofollow">Creativity, Inc</a>** raconte la même chose chez Pixar.

Il y aurait encore plein de titres à citer&#8230; mais voici de quoi vous occuper quelques temps. N&rsquo;hésitez pas à me conseiller les votres !