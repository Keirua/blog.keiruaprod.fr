---
id: 708
title:
  - Quelques astuces PostgreSQL pour faire des statistiques simples
date: 2014-01-02T22:35:07+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=708
permalink: /2014/01/02/astuces-postgresql-pour-des-statistiques-simples/
keywords:
  - sum case, count, postgresql, statistiques
description:
  - Quelques astuces PostgreSQL pour faire des statistiques simples
robotsmeta:
  - index,follow
categories:
  - Astuce
  - SQL
tags:
  - count
  - postgresql
  - statistiques
  - sum case
---
Même si les bases de données NoSQL ont la côte en ce moment, les bases de données SQL ont encore de beaux jours à vivre devant eux. En effet, dans beaucoup de situations, il est assez facile de sortir des statistiques avec quelques lignes de SQL. Voici quelques astuces que j&rsquo;ai découvert il y a quelques temps, et qui sont très pratiques pour sortir des chiffres.

Assez rapidement, lorsqu&rsquo;on fait du SQL, on a besoin de récupérer le nombre d&rsquo;éléments dans la base qui correspondent à un certain critère. Pour faire des statistiques, comme par exemple extraire le nombre d&rsquo;utilisateurs enregistrés dans la base par exemple. La réponse est classique :

<code lang="sql">&lt;br />
select&lt;br />
	count(u.id) as total&lt;br />
from&lt;br />
	users u&lt;br />
</code>

Ok, c&rsquo;était facile. Et si on veut le nombre d&rsquo;utilisateurs qui ont été créés chaque mois ?

### On peut utiliser un « group by date_trunc »

L&rsquo;astuce, c&rsquo;est d&rsquo;utiliser **date_trunc**. **date_trunc** permet de ne conserver, dans une date, que la partie de la date qui nous intéresse. Si notre date est le 4 janvier 1981 à 17h23, lorsqu&rsquo;on tronque au mois, date_trunc nous renverra le 1 janvier 1981 à 00h00. En combinant cela avec un **group by**, on peut obtenir le nombre d&rsquo;utilisateur qui a été créé mois par mois :

<code lang="sql">&lt;br />
select&lt;br />
	count(u.id) as total,&lt;br />
	date_trunc ('months', u.created_at) as considered_month&lt;br />
from&lt;br />
	users u&lt;br />
group by date_trunc ('months', u.created_at)&lt;br />
order by date_trunc ('months', u.created_at)&lt;br />
</code>

Comme vous l&rsquo;avez compris, le premier paramètre de date_trunc permet de définir où tronquer. En tronquant au jour ou bien à l&rsquo;heure on obtient une granularité plus fine, mais également plus de données, ce qui n&rsquo;est pas toujours ce dont on a besoin.

On obtient des résultats de ce genre, en supposant que nous ayons des utilisateurs entre avril et novembre 2013 :

| total |        considered_month |
| ----- | -----------------------:|
| 3956  | « 2013-04-01 00:00:00 » |
| 3965  | « 2013-05-01 00:00:00 » |
| 3549  | « 2013-06-01 00:00:00 » |
| 3728  | « 2013-07-01 00:00:00 » |
| 8311  | « 2013-08-01 00:00:00 » |
| 6041  | « 2013-09-01 00:00:00 » |
| 6381  | « 2013-10-01 00:00:00 » |
| 3784  | « 2013-11-01 00:00:00 » |

En fait, maintenant, on aimerait bien connaitre, pour chaque mois, le pourcentage d&rsquo;utilisateurs qui s&rsquo;est connecté au moins 3 fois, par rapport au nombre total d&rsquo;utilisateurs créés durant le mois. Ok, c&rsquo;est un exemple tordu, mais c&rsquo;est pour expliquer comment peut faire un pourcentage sur le nombre d&rsquo;éléments d&rsquo;un sous-ensemble de données d&rsquo;un mois concerné par rapport au nombre d&rsquo;éléments de l&rsquo;ensemble de départ.

### La structure sum (case &#8230;) 

L&rsquo;idée, c&rsquo;est d&rsquo;utiliser une structure avec **SUM (case &#8230; )** pour gérer un compteur « à la main ». Dans l&rsquo;exemple ci-dessous, vous pouvez voir qu&rsquo;on compte le nombre d&rsquo;éléments total avec **count**, et qu&rsquo;on compte le nombre d&rsquo;utisateurs ayant 3 connections en incrémentant un compteur nous même via **SUM (case &#8230; )**. Enfin, à la troisième ligne du select on calcule le pourcentage correspondant.

<code lang="sql">&lt;br />
select&lt;br />
	count(u.id) as total,&lt;br />
	sum( case when u.nb_connection > 3 THEN 1 ELSE 0 END) as subset_count,&lt;br />
	sum( case when u.nb_connection > 3 THEN 1 ELSE 0 END)::float * 100/ count(u.id)::float as percentage,&lt;br />
    date_trunc ('months', u.created_at) as considered_month&lt;br />
from&lt;br />
	users u&lt;/p>
&lt;p>group by date_trunc ('months', u.created_at)&lt;br />
order by date_trunc ('months', u.created_at)&lt;br />
</code>

Dans la vraie vie, au lieu de stocker un entier correspondant au nombre de connections, on stockerait plutôt la date de connection dans une table séparée, mais c&rsquo;est pour simplifier.

On obtient des résultats de ce genre :

| total | subset_count |       percentage |        considered_month |
| ----- |:------------:| ----------------:| -----------------------:|
| 3956  |     334      | 8.44287158746208 | « 2013-04-01 00:00:00 » |
| 3965  |     343      | 8.65069356872636 | « 2013-05-01 00:00:00 » |
| 3549  |     628      | 17.6951253874331 | « 2013-06-01 00:00:00 » |
| 3728  |     456      | 12.2317596566524 | « 2013-07-01 00:00:00 » |
| 8311  |     1206     | 14.5108891830105 | « 2013-08-01 00:00:00 » |
| 6041  |     842      |  13.938089720245 | « 2013-09-01 00:00:00 » |
| 6381  |     818      | 12.8193073186021 | « 2013-10-01 00:00:00 » |
| 3784  |     800      | 21.1416490486258 | « 2013-11-01 00:00:00 » |

Il est à noter qu&rsquo;avec PostgreSQL, on pourrait convertir directement le résultat de « u.nb_connection > 3 » entier pour faire la somme de manière plus concise, mais pas forcément plus simple à lire. De plus, l&rsquo;exemple ci-dessus montre qu&rsquo;on peut mettre plusieurs conditions (avec plusieurs « when » à l&rsquo;intérieur du case), ce que la conversion d&rsquo;un boolean ne montre pas forcément. Néanmoins, il est possible d&rsquo;écrire la ligne qui suit : 

<code lang="sql">&lt;br />
select&lt;br />
	count(u.id) as total,&lt;br />
	sum( (u.nb_connection > 3)::integer ) as subset_count,&lt;br />
	...&lt;br />
</code>

Bref, on a vu dans cet articles 2 structures pratiques pour extraire des chiffres à partir de votre base, en utilisant **group by date_trunc** et **sum (case &#8230;)**. Ca a l&rsquo;air de rien car les sommes et les moyennes sont des outils simples, mais ce sont également des outils très pratiques pour étudier l&rsquo;évolution d&rsquo;un business, ou anticiper les évolutions de structure à prévoir.