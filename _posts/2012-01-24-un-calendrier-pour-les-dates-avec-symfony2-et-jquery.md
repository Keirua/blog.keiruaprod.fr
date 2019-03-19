---
id: 246
title:
  - Un calendrier pour les dates avec Symfony2 et jQuery
date: 2012-01-24T23:10:43+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=246
permalink: /2012/01/24/un-calendrier-pour-les-dates-avec-symfony2-et-jquery/
keywords:
  - Formulaires, jQuery, jQuery-UI, Symfony2, JavaScript
description:
  - Modification du calendrier par défaut de Symfony2 pour utiliser celui de jQuery
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Javascript
  - Symfony2
tags:
  - Calendrier
  - Formulaires
  - jQuery
  - jQuery-UI
  - Symfony2
---
Par défaut, les champs de formulaires de type « Date » de Symfony2 sont représentés par 3 listes déroulantes. C&rsquo;est très pratique pour du prototypage, mais ce n&rsquo;est pas forcément ce que l&rsquo;on veut proposer à l&rsquo;utilisateur. On peut avoir envie de plutôt utiliser un sélecteur de date de type calendrier, comme on peut le trouver sur n&rsquo;importe quel site de réservation d&rsquo;hôtel ou de billet d&rsquo;avion par exemple.

Nous allons donc voir comment implémenter cette fonctionnalité dans Symfony2 avec jQuery UI. jQuery est une librairie JavaScript qu&rsquo;on ne présente plus, jQuery UI en est une extension qui propose de nombreuses fonctionnalités pour créer des interfaces dynamiques très web 2.0. 

<!--more-->

Avec un petit coup de jQuery UI, avoir un calendrier pour sélectionner une date est très facile :  
<code lang="html">&lt;br />
&lt;html>&lt;br />
	&lt;br />
	&lt;body>&lt;/p>

&lt;p>		&lt;br />
	&lt;/body>&lt;br />
&lt;/html>&lt;br />
</code>

On inclut les fichiers javascript et css nécessaires, on crée un formulaire contenant un champ de texte dont la classe est de type « date » (ça aurait pu être n&rsquo;importe quoi d&rsquo;autre), et on ajoute une ligne de JavaScript pour dire que les champs de texte dont la classe est « date » sont des datepicker, c&rsquo;est à dire des sélecteurs de date.

On va faire la même chose avec Symfony2, en un peu mieux, vu qu&rsquo;au passage on va mettre le calendrier en français. Les 2 problèmes que nous allons chercher à résoudre sont :

  * Comment changer le rendu de notre formulaire pour avoir un affichage différent ?
  * Qu&rsquo;en est-il de la persistence des données ?

Nous allons résoudre les 2 problèmes à la fois : en utilisant un type de données adapté au rendu que l&rsquo;on souhaite, ainsi qu&rsquo;avec des données au même format dans le formulaire et dans la base de données.

Pour résoudre le premier problème, nous allons utiliser le fait que, dans une classe de génération de formulaires (les classes de la forme EntityType, dans le répertoire Forms de votre bundle), il est possible de préciser pas mal d&rsquo;options. Dans cet exemple, on va imaginer que vous voulez sauvegarder une liste de vos inventions géniales et de leurs découvertes. On part de l&rsquo;entité Invention suivante, qui contient un attribut nom (une chaine de caractères) et un dateDecouverte de type DateTime. Quand je dis « ils sont de type », il faut comprendre du côté base de données.  
En voici le code :

<code lang="php">&lt;br />
// src\KeiruaProd\InventionBundle\Entity\Invention.php&lt;br />
<?php

namespace KeiruaProd\ApplicationBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
* KeiruaProd\ApplicationBundle\Entity\Invention
*
* @ORM\Table()
* @ORM\Entity
*/
class Invention
{
    /**
	* @var integer $id
	*
	* @ORM\Column(name="id", type="integer")
	* @ORM\Id
	* @ORM\GeneratedValue(strategy="AUTO")
	*/
    protected $id;

    /**
	* @var string $nom
	*
	* @ORM\Column(name="nom", type="string", length=255)
	*/
    protected $nom;
	
    /**
	* @ORM\Column(name="dateDecouverte", type="datetime")
	*
    * @var \DateTime
	*/
    protected $dateDecouverte;
}
</code>&lt;/p>
&lt;p>N'oubliez pas de faire un petit coup de &lt;/p>
&lt;p>&lt;code lang="bash">&lt;br />
php app/console doctrine:generate:entities KeiruaProd (ou tout autre namespace, bundle ou entité)&lt;br />
php app/console doctrine:schema:update --force&lt;br />
</code>

pour mettre à jour les getters/setters ainsi que la base de données. On est prêt à travailler !

Dans le cas d'un élément de type date, si on ne précise rien, le rendu par défaut est celui avec 3 listes déroulantes, mais l'option 'widget' nous permet de préciser quel élément graphique utiliser.

<code lang="php">&lt;br />
// src\KeiruaProd\InventionBundle\Form\InventionType.php&lt;br />
<?php

namespace KeiruaProd\ApplicationBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilder;

class InventionType extends AbstractType
{
    public function buildForm(FormBuilder $builder, array $options)
    {
        $builder->add('nom')&lt;br />
				->add('dateDecouverte', 'date', array(&lt;br />
												'widget' => 'single_text',&lt;br />
												'input' => 'datetime',&lt;br />
												'format' => 'dd/MM/yyyy',&lt;br />
												'attr' => array('class' => 'date'),&lt;br />
												)&lt;br />
            );&lt;br />
    }&lt;/p>
&lt;p>    public function getName()&lt;br />
    {&lt;br />
        return 'keiruaprod_applicationbundle_inventiontype';&lt;br />
    }&lt;/p>
&lt;p>    public function getDefaultOptions(array $options){&lt;br />
        return array('data_class' => 'KeiruaProd\ApplicationBundle\Entity\Invention');&lt;br />
    }&lt;br />
}&lt;br />
</code>

La partie intéressante, c'est celle qui concerne dateDecouverte. Le second argument du add, "date", indique qu'on veut un champ de type date (du point de vue des éléments de formulaires Symfony2). Un champ de formulaire de type date dans Symfony2, ça peut prendre plusieurs options, comme on peut le voir dans [la documentation correspondante](http://symfony.com/doc/2.0/reference/forms/types/date.html). Ici nous avons spécifié que nous voulons, dans l'ordre:

  * que l'élément graphique soit un champ de texte
  * que la donnée dernière soit associée à un objet DateTime
  * que le format de texte soit du type : 21/01/2012
  * que du côté du HTML, il y ait comme attribut supplémentaire la propriété "class" à "date". Nous reviendrons sur ça plus tard.

Ce sont les propriétés "input" et "format", qui, associées au type "datetime" de la propriété dateDecouverte de l'entité Invention, vont nous permettre de persister les données. A condition de fournir des données au bon format, mais c'est également un aspect sur lequel nous allons revenir bientôt.

Côté contrôleur et route, je vous laisse faire. J'imagine que vous savez créer un formulaire associé à des entités que l'on persiste dans une base de données, si ce n'est pas le cas, je vous invite à regarder la section sur l'ajout de commentaires de mon tutoriel [sur Symblog-fr](http://www.keiruaprod.fr/symblog-fr/docs/maj-des-articles-ajout-de-commentaires.html) sur le sujet.

On a vu le modèle, esquivé le contrôleur, mais qu'est ce qui se passe du côté de la vue ?  
Dans un premier temps, nous voulons utiliser jQuery, et en français. Pour utiliser cette librairie, il nous faut lier les fichiers suivants :  
<code lang="html">&lt;br />
		&lt;br />
		&lt;/p>
&lt;link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/themes/ui-lightness/jquery-ui.css" type="text/css" />
</code>

On inclue jQuery, puis jQuery-UI, et on applique un thème via le fichier CSS. Il en existe des quantités affolantes un peu partout sur le net, vous n'aurez donc pas de mal à trouver quelque chose qui vous plait.

Pour avoir le calendrier en français, il faut également inclure le fichier de langue situé à l'adresse suivante :  
http://jquery-ui.googlecode.com/svn/trunk/ui/i18n/jquery.ui.datepicker-fr.js  
Je vous conseille de le télécharger et de l'inclure via Assetic, car il n'est pas hébergé sur un serveur réellement fait pour être lié à chaud comme nous l'avons fait précédemment.

On y est presque !

Maintenant, une derniere touche de JavaScript pour activer l'utilisation de notre calendrier. Il nous faut préciser que nous voulons associer la classe CSS "date" à un calendrier. Ajoutez ce bout de code dans un fichier JavaScript qui est inclus dans la page où se trouve votre formulaire :  
<code lang="javascript">&lt;br />
$("form input.date").datepicker({&lt;br />
	dateFormat: 'dd/mm/yy',&lt;br />
	firstDay:1&lt;br />
}).attr("readonly","readonly");&lt;br />
</code>

Tout n'est pas obligatoire, car ce bout de code fait un peu plus que ce qui est vraiment nécessaire : il associe la classe CSS "date" au datepicker de jQuery-ui, précise le format de date (c'est important pour pouvoir persister les données). En bonus, le champ date n'est pas modifiable à la main via l'attribut "readonly". Pour modifier la date, il faut passer par le calendrier, ce qui va empêcher des utilisateurs maladroits de fournir des dates incorrectes. Pour plus d'informations, n'hésitez pas à lire la documention de [jQuery](http://docs.jquery.com/Main_Page) et du [calendrier jQuery-UI](http://jqueryui.com/demos/datepicker/)

Et voila ! Nous avons atteint notre objectif, qui était de pouvoir modifier l'affichage de la date pour quelquechose de plus sympa, et pouvoir derrière manipuler les données dans les entités associées. Si vous ne connaissiez pas jQuery ou jQuery-UI, c'est le moment de vous y intéresser : ces librairies permettent énormément de choses côté client qu'il vous est maintenant très facile d'interface avec Symfony2.