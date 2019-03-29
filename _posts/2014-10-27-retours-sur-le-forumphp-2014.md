---
id: 745
title:
  - Retours sur le ForumPHP 2014
date: 2014-10-27T07:14:20+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=745
permalink: /2014/10/27/retours-sur-le-forumphp-2014/
description:
  - Petit compte rendu du ForumPHP 2014.
robotsmeta:
  - index,follow
categories:
  - Développement Web
tags:
  - conférence
  - forum php
  - web
lang: fr
---
Le [Forum PHP](http://afup.org/pages/forumphp2014/ "Forum PHP 2014"), c&rsquo;était la semaine dernière et c&rsquo;était super bien. Petit compte rendu pour les absents, les liens ramènent vers la page joind.in des conférences.

## La théorie, une vision de l&rsquo;avenir du web

Plusieurs conférences étaient un peu théoriques, dans le sens où elles présentaient une vision du développement et des pratiques qui gravitent autour de manière idéale. Même si le monde réel est plus mitigé, celles auxquelles j&rsquo;ai pu assister valaient le coup, et je vous les recommande.  
[Sebastian Bergman](https://joind.in/talk/view/11936 "Sebastian Bergman, a state of mind") (créateur, entre autres, de phpunit), expliquait qu&rsquo;il y a 4 grands problèmes à faire des applications : la présentation, la persistance, les problématiques bas niveau, et la logique métier. Aujourd&rsquo;hui, on gère à peu prêt correctement les 3 premiers grâce -entre autre- aux framework, il y a maintenant plein de choses à faire mieux pour améliorer et rendre pérenne la plus importante, **la logique métier**. Même si la conférence en elle même était un peu passe partout, j&rsquo;ai trouvé le rappel d&rsquo;idées qu&rsquo;on considère implicites pertinent.  
[William Durand](https://joind.in/talk/view/11953) et son analyse des pratiques de **tests automatisés** m&rsquo;a mis sur le cul. Thésard sur la question, son état de l&rsquo;art et sa vision d&rsquo;où les tests se dirigent et doivent se diriger donnaient vraiment envie de mieux maîtriser la question. Sa présentation contient un paquet de mots-clés et de librairies qui devraient gagner en popularité.  
[Francois Zaninotto](https://joind.in/talk/view/11955), dans un discours façon homme politique (une idée originale bien menée) présentait une vision selon laquelle les framework full stack vont décliner pour laisser place à **plus de micro framework, de micro services, d&rsquo;API**. L&rsquo;idée, à terme, étant de se rapprocher d&rsquo;une philosophie à la unix (faire des applications/services ayant un but unique mais le faisant très bien). L&rsquo;avenir n&rsquo;est plus à des mono-technologies, mais à l&rsquo;usage de techno adaptées à des besoins précis : CMS en PHP, api en node, applis mobiles qui consomme ces API. Ce sera entre autre possible grâce à l&rsquo;interopérabilité permise par l&rsquo;utilisation d&rsquo;HTTP, et des groupes de discussion comme php-fig.

Je vous encourage à regarder les conférences lorsqu&rsquo;elles seront disponibles car il est bien évidemment très difficile de résumer en quelques mots ces conférences riches en idées.

## La pratique, c&rsquo;est à dire la théorie avec du retard et du pragmatisme

J&rsquo;ai beaucoup apprécié la vision théorique de ces présentations, mais j&rsquo;ai aussi beaucoup apprécié les retours d&rsquo;expérience de plusieurs boites présentes. Cela permet de situer l&rsquo;état de l&rsquo;industrie par rapport aux visions théoriques, et car cela m&rsquo;a permis de voir que ce nous faisons dans ma boite tient autant la route que ce qui se fait ailleurs. Au delà du côté « c&rsquo;est bon pour l&rsquo;ego », cela m&rsquo;a surtout permis de voir que où nous n&rsquo;avons pas de réponses, d&rsquo;autres sont tout autant dans le brouillard que nous.

La conclusion ? En théorie, on sait faire beaucoup de choses depuis longtemps. En pratique, le temps que les choses soient intégrées dans l&rsquo;industrie il faut beaucoup de temps, et pas mal de compromis (« The only sure thing about computer science: [everything is a tradeoff](http://dev-human.com/entries/2014/09/06/the-right-way/ "Everything is a tradeoff")« , comme le disent certains, et qui se généralise probablement très bien).

[Maison du monde](https://joind.in/talk/view/11945) parlait des **problèmes de régression** de leur site e-commerce. Intégrer l&rsquo;automatisation de la qualité par des tests ne s&rsquo;est pas fait sans mal, pose de vrais questions d&rsquo;organisation et est, chez eux, un enjeu permanent.

Les développeurs de [L&rsquo;express](https://joind.in/talk/view/11944) expliquaient l&rsquo;état de leurs recherches sur **l&rsquo;automatisation de déploiement d&rsquo;environnement de développements grâce à puppet, chef et amazon**. Ces outils permettent de gagner en automatisation, et ont une forte valeur ajoutée, mais laisse encore des questions et ont chez eux un coup d&rsquo;adoption élevé. Répliquer la configuration exacte de prod est compliqué (notamment quand on souhaite également répliquer la base de données quand elle est conséquente, pour reproduire des bugs complexes sans avoir à le faire directement en prod par exemple). Ils n&rsquo;ont pas de solution pour reproduire les problèmes d&rsquo;assets (images, uploads) dans les environnements de développement de manière systématique sans avoir à dire « t&rsquo;inquiète, ça marchera en prod ».

[Maxime Valette](https://joind.in/talk/view/11959), fondateur de **Viedemerde**, expliquait comment ils ont (sur)vécu à l&rsquo;explosion de viedemerde.fr à ses débuts, à cheval entre les besoins de communication pour répondre aux journalistes, et les besoins démentiels d&rsquo;infrastructure auxquels ils n&rsquo;étaient pas du tout préparé (en pour lesquels le temps possible de mise en place d&rsquo;une solution se chiffrait en heures). Bref ça a plus parlé de survie que de qualité, mais cela montrait clairement que la qualité de code n’empêche pas du tout un site de survivre à des très gros volumes de visite (comme le dit Jeff Atwood, [hardware is cheap](http://blog.codinghorror.com/hardware-is-cheap-programmers-are-expensive/)).

## Les vieux de la vieille

C&rsquo;est assez inévitable avec un langage qui a plus de 15 ans et qui est le plus déployé dans le monde, des présentations sur les CMS les plus répandus présentaient leur situation courante et l&rsquo;avenir.  
Je ne suis pas utilisateur, mais ça a permis de voir que là où **[EzPublish](https://joind.in/talk/view/11958)** et **Drupal** ont récemment fait le choix de la refonte pour tenir dans le temps, **[WordPress](https://joind.in/talk/view/11947)** préfère conserver la rétrocompatibilité en ne touchant pas au core. On verra bien ce que cela donnera dans les années à venir : wordpress a le volume, les autres ont maintenant une meilleure qualité de code, mais ça n&rsquo;est pas forcément pertinent et nécessaire pour mieux pénétrer le marché&#8230;

## Les API à l&rsquo;honneur

**Les micro services et API** avaient le vent en poupe lors du forum. Plusieurs conférences en parlaient et il y a notamment eu 2 retours d&rsquo;expérience sur le sujet, l&rsquo;une faite par [les gens d&rsquo;Elao](https://joind.in/talk/view/11944) expliquant tous les problèmes qu&rsquo;ils ont eu et auquel on peut s&rsquo;attendre d&rsquo;être confrontés un jour ou l&rsquo;autre lorsqu&rsquo;on cherche à mettre en place une architecture d&rsquo;api orientée micro services. La présentation était assez macro, et présentait les problématiques de communication, d&rsquo;infrastructure, de sécurité, de monitoring, de cache&#8230;  
L&rsquo;autre, présentée par quelqu&rsquo;un de l&rsquo;équipe [d&rsquo;Arte](https://joind.in/talk/view/11962) rentrait plus dans les détails, avec quelques bouts de code sur comment ils avaient pu résoudre certains problèmes. Les deux donnaient des idées à des niveaux différents et sont complémentaires.

## De nouveaux usages

Les conférences parlaient aussi de « nouveaux » usages, des usages pas encore tout à fait répandus dans la communauté.

Je parle beaucoup d&rsquo;API, quelqu&rsquo;un de chez Lemonde est venu expliquer comment ils ont intégré du **[nodeJS](https://joind.in/talk/view/11964)** dans leur pile applicative lors de la refonte de leur CMS, notamment pour exposer une API consommé par une application javascript monopage.

J&rsquo;ai beaucoup aimé sa remarque « Considérez vous comme des développeurs avant d&rsquo;être des développeurs PHP ». Merci ! Il faudrait l&rsquo;imprimer en immense et l&rsquo;afficher dans toutes les boites. Ca marche également avec « vous êtes des développeurs avant d&rsquo;être des développeurs web ». Cette idée a l&rsquo;air simple mais en pratique, c&rsquo;est parce que des gens ont regardé ce qu&rsquo;il se faisait ailleurs, notamment dans les applis clients lourd, que les bonnes pratiques du génie logiciel (tests automatisés, injection de dépendances par exemple) ont fini par arriver dans le monde du PHP. Ca a toutefois mis beaucoup de temps et PHP (et le web en général) continue d&rsquo;avoir du retard. Bref, cette conférence était l&rsquo;application directe de l&rsquo;idée de Francois Zaninotto, selon laquelle nous arrivions sur plus d’interopérabilité grâce à HTTP, et à l&rsquo;utilisateur d&rsquo;outils spécifiques pour des besoins précis.

Une autre série d&rsquo;outils que j&rsquo;ai pu découvrir, ce sont **les outils d&rsquo;analyse de code**. **[Scrutinizer](https://joind.in/talk/view/11940)**, ainsi que qu&rsquo;**Insight** de SensioLabs permettent de voir le code qui ne respecte pas des règles élémentaires (le passage de paramètres get directement dans les requêtes SQL, donc source d&rsquo;injection par exemple), même dans des configurations complexes. Leur force, c&rsquo;est leur utilisation en SaaS, intégrée avec Github, qui ouvre des perspectives intéressantes.

Une conférence présentait également une idée assez intéressante: l&rsquo;utilisation de **[diffbot](https://joind.in/talk/view/11948)** pour concevoir des API pour ses propres besoins. Basé sur du **scraping** de page intelligent, on peut se créer sa propre API pour des sites qui n&rsquo;en proposent pas, par exemple pour sortir de manière automatique la liste des articles publiés par une personne sur un site éditorial, pour par la suite automatiser des tâches (en faisant des graphes de fréquence de publication) de suivi.

J&rsquo;ai eu l&rsquo;impression que ça n&rsquo;a pas intéressé grand monde, peut-être l&rsquo;intérêt pour les développeurs est moins immédiat que dans d&rsquo;autres sujet. C&rsquo;est pourtant hyper disruptif et je suis convaincu que ça va gagner en popularité d&rsquo;ici peu avec les avancées et les nouveaux besoins amenés par le big data (ça y est, moi aussi je me mets à parler comme un chef de projet d&rsquo;agence digitale).

## La conférence en elle même

La conférence a bien marché, l&rsquo;organisation était top. Les speakers, pour beaucoup très connus dans la communauté étaient évidemment très compétents. Les sujets étaient généralement pointus, ce qui permet de ramener plusieurs idées et pas mal de motivation pour faire mieux chez soi&#8230;

Une seule conférence m&rsquo;a franchement déçue, celle de [Dayle Reese](https://joind.in/talk/view/11961). Il devait parler de Laravel, mais après avoir parlé 15mn de lui s&rsquo;est trouvé à court de temps. J&rsquo;y suis allé pour découvrir la philosophie de ce framework controversé (et, ironiquement, qui semble pratiquer le culte de la personnalité derrière son gourou, Taylor Otwell), je ne suis pas plus avancé, et n&rsquo;ai aucune envie de creuser plus la question, dommage.

Au niveau du fonctionnement, il y avait simultanément deux conférences, ce qui permettait de choisir les thématiques qui nous intéressaient (ou, parfois, de devoir faire un choix terrible !). L&rsquo;horloge était bien gérée par l&rsquo;équipe d&rsquo;organisation, il n&rsquo;y a presque pas eu de retards et c&rsquo;était vraiment bien pour ne pas louper de présentation. Une gestion rigoureuse du temps n&rsquo;est pas la norme dans les conférences alors que c&rsquo;est pourtant essentiel, c&rsquo;était donc cool d&rsquo;avoir bien géré ça.

Le seul bémol, c&rsquo;est le manque de places parfois pour certaines conférences. Il fallait arriver en avance pour certaines conférence afin d&rsquo;avoir une place assise, pour des histoires de sécurité, le personnel du beffroi était intransigeant sur la question. C&rsquo;est d&rsquo;autant plus dommage pour la table ronde finale, seul événement à ce moment là&#8230; il n&rsquo;y avait pas de places pour tout le monde, et arrivant parmi les derniers, l&rsquo;accès à la salle m&rsquo;a été refusé car il ne restait plus de places assises. Dommage pour moi. Même si c&rsquo;est un signe positif pour l’événement qui marche très bien et pour la communauté qui n&rsquo;a pas fini de faire des trucs sympa, vu le prix des places c&rsquo;est pas super cool.

Evidemment, cet article bien trop long met de côté la moitié des conférences, et ne parle pas des ateliers vu que je n&rsquo;ai participé à aucun d&rsquo;entre eux. Et si le sujet des API m&rsquo;a marqué car il m&rsquo;intéresse, il est probable que chacun soit revenu avec des idées différentes. Quoi qu&rsquo;il en soit, c&rsquo;était très chouette et si vous n&rsquo;y étiez pas, je vous conseille de regarder les [slides des présentations](https://joind.in/event/view/2091). Si vous n&rsquo;en pouvez plus d&rsquo;attendre les vidéos officielles, rabattez vous sur la video officieuse du [karaoké slideshow](https://www.youtube.com/watch?v=rToQ34KHP60&list=PLuT_8P4VHn_pwZ-MKnOks4CLsm-i07Qib&index=1) 🙂