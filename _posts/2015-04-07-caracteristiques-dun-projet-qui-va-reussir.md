---
id: 788
title:
  - "Caractéristiques d'un projet qui va réussir"
date: 2015-04-07T08:01:04+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=788
permalink: /2015/04/07/caracteristiques-dun-projet-qui-va-reussir/
keywords:
  - gestion de projet, agile
description:
  - Elements de gestion de projet pour ne pas se planter
robotsmeta:
  - index,follow
categories:
  - Entreprenariat
tags:
  - agile
  - gestion de projet
lang: fr
---
J&rsquo;ai eu l&rsquo;occasion de participer à plusieurs projets, le plus souvent de développement. Ils ont eu des durées et des importances variées. Certains se sont cassés la figure d&rsquo;une manière ou d&rsquo;une autre, et d&rsquo;autres se sont très bien passés. Ces expériences m&rsquo;ont permis de constater quelques unes des caractéristiques de projets qui marchent bien. Cela n&rsquo;est pas valable que pour du développement, cela marche pour vraiment n&rsquo;importe quel type de projet.

Quand je parle de réussir, je ne m&rsquo;intéresse ici qu&rsquo;à la **réalisation technique du projet**. C&rsquo;est mon métier. Ce n&rsquo;est pas le seul, et souvent d&rsquo;autre éléments sont en jeu, l&rsquo;aspect commercial par exemple. en sont un autre et je ne suis pas la bonne personne pour en parler.

## Deux manières de procéder

<div>
  Il y a plusieurs manières de lire cette liste :
</div>

  * **Lancement d&rsquo;un projet** : elle peut servir de **checklist**
  * **Projet en cours** : risquez-vous d&rsquo;aller dans le mur ? Vous pourrez peut-être **corriger le tir**.
  * **Projet terminé** : permet d&rsquo;en faire une **rétrospective**, où l&rsquo;on peut identifier quels éléments du projet étaient fragiles

## Caractéristiques clé

### Facile à comprendre

Les projets sont souvent rangés dans une application de gestion de projet (cela peut être un simple fichier google doc partagé, ou bien dans Jira, Trello&#8230;).

**Le titre du projet, ou bien la définition macro du besoin doivent être clairs**. Au premier contact avec un projet, ce qui se fait souvent par un titre assez succin, on doit savoir de quoi il retourne.  
Si ce n&rsquo;est pas le cas, c&rsquo;est en général mauvais signe : « Ce qui se conçoit bien s&rsquo;énonce clairement ». Si l&rsquo;initiateur du projet ne fait pas l&rsquo;effort de présenter son projet clairement ou si le projet est flou car le projet lui même n&rsquo;est pas encore abouti, il risque d&rsquo;y avoir des problèmes de communication rapidement.

### Le périmètre fonctionnel est clair

**Il ne doit pas y avoir d’ambiguïté sur ce qui doit être réalisé**. Cela peut être lié au problème précédent (préférer « Concevoir l&rsquo;interface de gestion des messages privés entre utilisateurs » à « Outils de discussions interne »).

Lorsque le titre ne suffit pas à préciser ce qui doit être fait, il faut aller plus loin : texte de description, maquettes, documents de spécification&#8230; Tout dépend du projet et de l&rsquo;autonomie dont dispose (en théorie, et surtout en réalité) l&rsquo;équipe.

### Les actions à réaliser sont listées de manière exhaustives et précise

Avant de commencer à faire quoi que ce soit, on doit **savoir ce qu&rsquo;il faut faire**; c&rsquo;est un travail collaboratif ! Seul, on a vite fait d&rsquo;oublier une tâche qui va s&rsquo;avérer importante par la suite, en minorer le temps nécessaire ou l&rsquo;importance. Tous les acteurs du projet doivent contribuer à lister ce qui doit être fait, et **réfléchir à leur faisabilité**.

Certaines actions ne seront pas forcément réalisables immédiatement (ex: la migration d&rsquo;un module dans un nouveau framework nécessite la refonte du modèle de base de données). Il faut trouver des solutions (ex: bridge temporaire avec l&rsquo;ancien modèle, et initiation d&rsquo;un projet plus globale de refonte du modèle).

Cette étape est cruciale car on a vite fait d&rsquo;omettre des éléments clés qui peuvent remettre en cause le temps effectif de réalisation, ainsi que les choix techniques mis en places.

### Les livrables sont définis précisément

Livrer un site responsive, ce n&rsquo;est pas la même chose que livrer un site ET une application mobile. Cela peut sembler évident, mais ca ne l&rsquo;est pas. Penser à **lever les ambiguïtés et les non-dits sur ce qu&rsquo;il faut rendre en fin de projet**.

### Les experts et les ressources matérielles sont accessibles

Dans n&rsquo;importe quel projet on a besoin d&rsquo;avoir accès à des personnes et des ressources. Les personnes vont par exemple avoir une expertise métier nécessaire à la conception du produit (ou plutôt à l&rsquo;avant projet, ce qui peut être considéré comme un projet en soit).

Les ressources matérielles nécessaires doivent également être fournies ou disponibles. Cela peut être :

  * Les accès aux différents serveurs nécessaires (base de donnée, accès SSH)
  * Les licences nécessaires (IDE, applicatifs, outils SaaS&#8230;)
  * Les applicatifs sont correctement configurés. Si ce n&rsquo;est pas le cas, on doit avoir la possibilité de le faire. Le temps nécessaire devra alors être anticipé et alloué pour cela
  * &#8230;

Quoi qu&rsquo;il en soit, il faut **savoir à l&rsquo;avance de quoi on aurait besoin** et pouvoir **y avoir accès lorsque c&rsquo;est nécessaire**.

### Une date butoire réaliste

Ha, les estimations&#8230; On ne va pas se mentir, les estimations, c&rsquo;est de la magie noire et personne ne peut prédire précisément le temps que va prendre la réalisation d&rsquo;un projet.

C&rsquo;est pourtant un indicateur clé qu&rsquo;il ne faut pas négliger. Elle doit être réaliste : si on laisse 15 jours pour faire quelque chose qui prend de toute évidence 2 mois, on va dans le mur en niant l&rsquo;évidence (c&rsquo;est plus courant qu&rsquo;on ne le croit).  
La pertinence d&rsquo;une date butoire est difficile à évaluer _a priori_, mais **on peut mesurer sa dérive en cours de projet**. A mi-projet, on peut tenter d&rsquo;estimer si on est encore dans les clous ou si on est déjà foutus. Si on a de l&rsquo;avance (c&rsquo;est plus rare que l&rsquo;inverse), en profiter pour améliorer la qualité.

### Découper en milestones

Si le projet est long, il peut devenir pertinent de le découper à l&rsquo;aide de milestones, des dates clés auxquelles on va vérifier un certain nombre de choses (livrables intermédiaires). On peut alors considérer chaque milestone comme un sous projet, qui doit alors avoir les mêmes caractéristiques que le reste (date butoire réaliste, livrables précisément définis, etc.)

### Pas d&rsquo;interruptions

Nous, les humains, sommes très mauvais pour faire deux choses à la fois. Quand on travaille sur un projet, c&rsquo;est mieux de se concentrer sur celui ci plutôt que d&rsquo;essayer d&rsquo;en développer plusieurs à la fois. **Passer d&rsquo;une tâche à l&rsquo;autre est une catastrophe pour la concentration**. Quand on est sur un projet, cela veut dire, autant que possible : pas de debug d&rsquo;un autre projet, pas de R&D en parallèle du projet&#8230;

Cela n&#8217;empêche pas de le faire, et c&rsquo;est d&rsquo;ailleurs ce qui arrive assez souvent. Dans ce cas, le temps nécessaire à la réalisation des diverses tâches et projets doit être clairement défini et alloué dans ce sens.

### Eviter de changement

Les caractéristiques décrites ici s&rsquo;insèrent très bien dans une méthodologie agile, qui prône une réactivité presque totale au changement. D&rsquo;une itération à l&rsquo;autre, ce qui est conçu peut être jeté pour faire complètement autre chose que ce qui était prévu au départ. C&rsquo;est une bonne chose (pas forcément toujours bonne à entendre pour le développeur qui conçoit l&rsquo;application, certes), car elle permet d&rsquo;assurer que le produit réalisé est bien le bon.

Par contre, **il faut un peu de rigueur** pour utiliser cette méthodologie correctement, et ne pas interrompre ou altérer un sprint à tout bout de champ. Ajouter de nouvelles tâches, ou modifier les tâches existantes est le meilleur moyen d&rsquo;aller dans le mur en croyant bien faire. Rapidement, cela peut réduire à néant tout ce qui a été précieusement préparé (périmètre fonctionnel, livrables attendus, date butoire qui devient difficile à respecter, etc.), tout en faisant baisser la qualité du résultat ainsi que la motivation des parties prenantes.

## Tout est communication

Finalement, toutes ces remarques gravitent autour de **la problématique de la communication**. N&rsquo;importe qui devrait pouvoir comprendre les caractéristiques du projet, et en comprendre les tenants et aboutissants. Il ne doit pas y avoir de non-dits, ou d&rsquo;idées tacites qui ne soient pas exprimées, explicitées, clarifiées, couchées sur papier.

Ce qui est clair pour quelqu&rsquo;un ne l&rsquo;est souvent pour plusieurs personnes que quand elles en ont discuté et se sont mises d&rsquo;accord à grand coup de schéma. Noter le résultat permet d&rsquo;y revenir plus tard.

Vous constaterez probablement qu&rsquo;il n&rsquo;y a rien de fou dans cette liste et probablement pas d&rsquo;idée nouvelle. Comme souvent en management ou en gestion de projet, il est question de **bon sens**. Bien que tout le monde croit en avoir, trop souvent les les projets en manquent d&rsquo;une manière ou d&rsquo;une autre. La clé d&rsquo;un projet qui démarre bien, c&rsquo;est finalement **la rigueur** avec laquelle il est décrit.