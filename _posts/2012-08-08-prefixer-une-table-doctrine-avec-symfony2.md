---
id: 468
title: Préfixer une table Doctrine avec Symfony2
date: 2012-08-08T15:26:32+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=468
permalink: /2012/08/08/prefixer-une-table-doctrine-avec-symfony2/
robotsmeta:
  - index,follow
archived: true
categories:
  - Développement Web
  - Symfony2
---
<div id="attachment_469" style="width: 201px" class="wp-caption alignright">
  <a href="http://www.doctrine-project.org/"><img class="size-full wp-image-469" title="Logo doctrine" src="https://keiruaprod.fr/blog/wp-content/uploads/2012/08/doctrine_logo.png" alt="" width="191" height="53" /></a>
  
  <p class="wp-caption-text">
    Doctrine, l&rsquo;ORM de base de Symfony2
  </p>
</div>

Préfixer une table de base de données est, de manière générale, une mauvaise pratique. Souvent parce que cela signifie qu&rsquo;on cherche à faire cohabiter 2 applications différentes sur une même base de données, ce qui n&rsquo;est pas une bonne chose du point de vue architecture et séparation des responsabilités (SoC, [Separation of Concerns](http://aspiringcraftsman.com/2008/01/03/art-of-separation-of-concerns/)). Dans ce cas, il est largement accepté d&rsquo;avoir chaque application sur une base séparée, et c&rsquo;est d&rsquo;une manière générale la méthode préconisée.

Maintenant, il arrive des cas où il est utile de pouvoir préfixer ses tables. Par exemple parce que c&rsquo;est la convention requise, ou bien parce que les 2 applications sont 2 parties d&rsquo;un même tout (par exemple une application Symfony pour le coeur métier, et un [WordPress](www.wordpress.com) pour la partie blog). Préfixer les tables permet alors d&rsquo;éviter les collisions de noms.

<!--more-->

C&rsquo;est tellement une mauvaise pratique que ce qui est un paramètre de configuration dans WordPress n&rsquo;est même pas disponible de base avec Doctrine, l&rsquo;ORM livré de base avec Symfony2. On a pas forcément l&rsquo;envie ni la capacité de renommer tous les noms de tables soi-même (ce qui ne serait pas non plus une bonne chose). De plus celà veut dire qu&rsquo;à chaque fois qu&rsquo;on voudra rajouter une table il ne faudra pas oublier de la prefixer, bref c&rsquo;est le début des emmerdes.  
Quand on doit quand même avoir un système de prefixes de table à peu près viable, on fait comment ? On rajoute a fonctionnalité soi-même.

La fonctionnalité n&rsquo;est donc pas supportée de base avec Doctrine, mais ils proposent [une solution](http://docs.doctrine-project.org/projects/doctrine-orm/en/2.0.x/cookbook/sql-table-prefixes.html) dans un cookbook, avec du code prêt à l&#8217;emploi. Il ne nous reste qu&rsquo;à l&rsquo;intégrer, et on est bon. Mais comment ?

L&rsquo;exemple de la doc nous dit qu&rsquo;il faut créer un listener d&rsquo;évènements, qui se greffe sur l&rsquo;appel de la méthode loadClassMetaData.  
Un petit coup d&rsquo;oeil à la documentation sur [le sujet](http://symfony.com/doc/current/cookbook/doctrine/event_listeners_subscribers.html) nous indique qu&rsquo;il suffit de créer un service, et de le tagger doctrine.event_subscriber. C&rsquo;est bon, ya plus qu&rsquo;à.

C&rsquo;est ce qu&rsquo;on va faire, en modifiant notre fichier FooBundle/config/services.yml:  
<code lang="yaml">&lt;br />
parameters:&lt;br />
    keiruaprodfoo.doctrine.prefix: kp_foo_&lt;/p>
&lt;p>services:&lt;br />
    keiruaprodfoo.doctrineprefix_subscriber:&lt;br />
        class: KeiruaProd\FooBundle\DoctrineExtensions\TablePrefixSubscriber&lt;br />
        arguments: [%keiruaprodfoo.doctrine.prefix%]&lt;br />
        tags:&lt;br />
            - { name: doctrine.event_subscriber }&lt;br />
</code>

Maintenant, reste à créer notre classe. Comme le montre toujours [la même doc](http://docs.doctrine-project.org/projects/doctrine-orm/en/2.1/reference/events.html#the-event-system), pour faire un subscriber d&rsquo;évènements il faut que notre classe hérite de \Doctrine\Common\EventSubscriber. C&rsquo;est ce qu&rsquo;on va faire. On crée un fichier FooBundle/DoctrineExtensions\TablePrefixSubscriber, dont le contenu va beaucoup ressembler à celui de la documentation de départ :

<code lang="php">&lt;br />
<?php

namespace KeiruaProd\FooBundle\DoctrineExtensions;
use \Doctrine\ORM\Event\LoadClassMetadataEventArgs;

class TablePrefixSubscriber implements \Doctrine\Common\EventSubscriber
{
    protected $prefix = '';

    public function __construct($prefix)
    {
        $this->prefix = (string) $prefix;&lt;br />
    }&lt;/p>
&lt;p>	public function loadClassMetadata(LoadClassMetadataEventArgs $eventArgs)&lt;br />
    {&lt;br />
        $classMetadata = $eventArgs->getClassMetadata();&lt;br />
        $classMetadata->setTableName($this->prefix . $classMetadata->getTableName());&lt;br />
        foreach ($classMetadata->getAssociationMappings() as $fieldName => $mapping) {&lt;br />
            if ($mapping['type'] == \Doctrine\ORM\Mapping\ClassMetadataInfo::MANY_TO_MANY) {&lt;br />
                $mappedTableName = $classMetadata->associationMappings[$fieldName]['joinTable']['name'];&lt;br />
                $classMetadata->associationMappings[$fieldName]['joinTable']['name'] = $this->prefix . $mappedTableName;&lt;br />
            }&lt;br />
        }&lt;br />
    }&lt;/p>
&lt;p>	public function getSubscribedEvents()&lt;br />
    {&lt;br />
        return array('loadClassMetadata');&lt;br />
    }&lt;br />
}&lt;/p>
&lt;p></code>

La seule différence avec le code original, c&rsquo;est que comme on hérite de EventSubscriber, il faut implémenter getSubscribedEvents(), qui donne la liste des évènements auxquels on s&rsquo;inscrit.

Maintenant, on en a fini avec le code. Au niveau fonctionnel, ça dépend. Si on vient de démarrer un nouveau projet et qu&rsquo;aucune base n&rsquo;a été créé, pas de soucis. Les nouvelles tables auront le préfixe précisé quand elles seront créés.  
Maintenant si on a déjà des tables, attention. Si vous mettez à jour le schéma de base de données (via app/console doctrine:schema:update &#8211;force), bien evidemment seul le schéma est mis à jour. Il faudra sans doute réinsérer vos données factices dans la base, ou avoir une copie de la base initiale. Quoi qu&rsquo;il en soit, celà doit s&rsquo;intégrer dans votre process de migrations&#8230; Peut être utiliserez vous [DoctrineMigrationsBundle](http://knpbundles.com/doctrine/DoctrineMigrationsBundle), dont j&rsquo;avais parlé [il y a un bon moment](http://keiruaprod.fr/symblog-fr/docs/maj-des-articles-ajout-de-commentaires.html "Modèle de commentaires, dépôts et migrations") déjà ?