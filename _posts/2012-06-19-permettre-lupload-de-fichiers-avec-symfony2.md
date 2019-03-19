---
id: 392
title:
  - "Permettre l'upload de fichiers avec Symfony2"
date: 2012-06-19T16:09:10+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=392
permalink: /2012/06/19/permettre-lupload-de-fichiers-avec-symfony2/
keywords:
  - symfony2, doctrine2, upload
description:
  - "Introduction à l'upload de fichiers avec Symfony2"
robotsmeta:
  - index,follow
categories:
  - Développement Web
  - Symfony2
tags:
  - doctrine2
  - Symfony2
  - upload
---
Permettre à l&rsquo;utilisateur d&rsquo;uploader des fichiers est une tâche qui revient régulièrement. Cela peut par exemple permettre à l&rsquo;utilisateur de mettre en ligne sa photo de profil, ou encore si vous proposez une solution d&rsquo;hébergement de documents, lui permettre de stocker des fichiers pdf importants.

Dans cet article, nous allons prendre l&rsquo;exemple de la mise en ligne d&rsquo;une photo de profil pour vos utilisateurs, et regarder comment implémenter cette fonctionnalité avec Symfony2. Le code utilisé est inspiré de [la page du cookbook](http://symfony.com/doc/current/cookbook/doctrine/file_uploads.html) associée à ce sujet, mais je vais essayer de détailler un peu plus la procédure afin de faciliter sa compréhension.

<!--more-->

### Mise à jour des entités

Pour faire le lien entre le fichier uploadé et l&rsquo;entité auquel il est associé, il est nécessaire de mettre à jour l&rsquo;entité concernée. Notre but est de permettre aux utilisateurs d&rsquo;uploader une photo de profil. Je vais donc supposer que nous avons déjà une entité User qui se charge de la gestion des utilisateurs (au passage, [FOSUserBundle](https://github.com/FriendsOfSymfony/FOSUserBundle) est un très bon bundle pour tout ce qui est création d&rsquo;utilisateurs et authentification, mais c&rsquo;est une autre histoire). 

Dans notre entité User, nous allons rajouter un champ vers le chemin du fichier, pictureName, ainsi qu&rsquo;un élément file, qui est présent dans l&rsquo;entité mais n&rsquo;est pas persisté : il est nécessaire pour créer l&rsquo;élément de formulaire, et va nous permettre de manipuler le fichier physique sur le serveur. Une annotation permet de préciser la taille maximale du fichier qu&rsquo;il est possible de mettre en ligne, ici 500Ko.  
Nous allons également rajouter plusieurs méthodes qui serviront par la suite pour connaitre le chemin vers notre image (dont le code vient directement du cookbook déjà évoqué). 

Notez bien la méthode getUploadDir : cette méthode va permettre de centraliser le nom du répertoire dans lequel uploader les fichiers, et nous éviter de trimballer une chaine de caractères. Elle veut également dire que tous nos fichiers seront uploadés dans le répertoire /web/uploads/pictures de votre application.

N&rsquo;oubliez pas le use !

<code lang="php">&lt;br />
use Symfony\Component\Validator\Constraints as Assert;&lt;/p>
&lt;p>class User&lt;br />
{&lt;br />
    // ... Code de votre entité d'utilisateur&lt;/p>
&lt;p>    /**&lt;br />
     * @ORM\Column(type="string", length=255, nullable=true)&lt;br />
     */&lt;br />
    public $pictureName;&lt;/p>
&lt;p>	/**&lt;br />
     * @Assert\File(maxSize="500k")&lt;br />
     */&lt;br />
    public $file;&lt;/p>
&lt;p>    public function getWebPath()&lt;br />
    {&lt;br />
        return null === $this->pictureName ? null : $this->getUploadDir().'/'.$this->pictureName;&lt;br />
    }&lt;/p>
&lt;p>    protected function getUploadRootDir()&lt;br />
    {&lt;br />
        // le chemin absolu du répertoire dans lequel sauvegarder les photos de profil&lt;br />
        return __DIR__.'/../../../../web/'.$this->getUploadDir();&lt;br />
    }&lt;/p>
&lt;p>    protected function getUploadDir()&lt;br />
    {&lt;br />
        // get rid of the __DIR__ so it doesn't screw when displaying uploaded doc/image in the view.&lt;br />
        return 'uploads/pictures';&lt;br />
    }&lt;/p>
&lt;p>	public function uploadProfilePicture()&lt;br />
	{&lt;br />
		// Nous utilisons le nom de fichier original, donc il est dans la pratique&lt;br />
		// nécessaire de le nettoyer pour éviter les problèmes de sécurité&lt;/p>
&lt;p>		// move copie le fichier présent chez le client dans le répertoire indiqué.&lt;br />
		$this->file->move($this->getUploadRootDir(), $this->file->getClientOriginalName());&lt;/p>
&lt;p>		// On sauvegarde le nom de fichier&lt;br />
		$this->pictureName = $this->file->getClientOriginalName();&lt;/p>
&lt;p>		// La propriété file ne servira plus&lt;br />
		$this->file = null;&lt;br />
	}&lt;/p>
&lt;p>	// Reste de votre entité&lt;br />
}&lt;br />
</code>

On met à jour les accesseurs et la base de données via un app/console generate:entities et app/console doctrine:schema:update &#8211;force, et on est prêt pour la suite.

### Création de la page d&rsquo;upload

Pour pouvoir uploader la photo de profil, il est nécessaire d&rsquo;avoir un formulaire. Nous allons en créer un minimaliste, uniquement pour mettre à jour la photo de profil. Créez un fichier IdentityPictureType.php dans KeiruaProd/ApplicationBundle/Form (enfin, remplacez par le nom de votre bundle), et copiez-y le code suivant : 

<code lang="php">&lt;br />
<?php

namespace KeiruaProd\ApplicationBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilder;

class IdentityPictureType extends AbstractType
{
    public function buildForm(FormBuilder $builder, array $options)
    {
        $builder
            ->add('file')&lt;br />
        ;&lt;br />
    }&lt;br />
    public function getName()&lt;br />
    {&lt;br />
        return 'keiruaprod_applicationbundle_identitypicturetype';&lt;br />
    }&lt;br />
}&lt;br />
</code>

Nous avons créé un formulaire ultra basique, qui ne contient qu&rsquo;un champ de sélection de fichiers. Faisons un template très simple également. Je l&rsquo;ai mis dans ressources/views/Profile/preferences.html.twig. N&rsquo;oubliez pas {{ form_enctype(form) }} :

<code lang="html">&lt;br />
{% if user.pictureName %}&lt;br />
	&lt;img src="{{ asset(user.getWebPath()) }}" />&lt;br />
{% else %}&lt;br />
	Pas d'image de profil chargée !&lt;br />
{% endif %}&lt;/p>
&lt;h1>Charger une image de profil&lt;/h1>

&lt;p></code>

Et maintenant, il est temps de créer notre méthode dans un contrôleur pour gérer l&rsquo;affichage et l&rsquo;upload.

<code lang="php">&lt;br />
<?php
namespace KeiruaProd\ApplicationBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use KeiruaProd\ApplicationBundle\Form\IdentityPictureType;

class VotreController extends BaseController
{	
	public function preferencesAction (){
		$usr = $this->getUser();&lt;/p>
&lt;p>		$form = $this->createForm(new IdentityPictureType(), $usr);&lt;/p>
&lt;p>		if ($this->getRequest()->getMethod() === 'POST') {&lt;br />
			$form->bindRequest($this->getRequest());&lt;br />
			if ($form->isValid()) {&lt;br />
				$em = $this->getDoctrine()->getEntityManager();&lt;/p>
&lt;p>				$usr->uploadProfilePicture();&lt;/p>
&lt;p>				$em->persist($usr);&lt;br />
				$em->flush();&lt;/p>
&lt;p>				$this->redirect($this->generateUrl('KeiruaProdApplicationBundle_profile'));&lt;br />
			}&lt;br />
		}&lt;/p>
&lt;p>		return $this->render('KeiruaProdApplicationBundle:Profile:preferences.html.twig',&lt;br />
				array (&lt;br />
					'user' => $usr,&lt;br />
					'form' => $form->createView()&lt;br />
					)&lt;br />
				);&lt;br />
	}&lt;br />
}&lt;br />
</code>

Ce code suppose que vous avez créé une route « KeiruaProdApplicationBundle_profile », et que vous avez associés l&rsquo;action preferencesAction à une route. Si vous l&rsquo;exécutez, cela fonctionne : le formulaire, bien que très basique, est affiché, il permet de sélectionner un fichier, et de le mettre en ligne. Lorsque l&rsquo;utilisateur a chargé une image, grâce à la fonction twig asset(), le chemin correct vers l&rsquo;image est utilisé et l&rsquo;image est affichée.

Bien évidemment, cette présentation de l&rsquo;upload, ainsi que l&rsquo;implémentation proposée, est très simpliste : si 2 utilisateurs uploadent un fichier du même nom, ils vont utiliser la même photo de profil, et le premier va perdre sa photo de profil. Il est donc nécessaire de rendre propres les noms de fichiers utilisés (par exemple en utilisant l&rsquo;id de l&rsquo;entité auxquels ils sont associés). Il peut également être une bonne idée d&rsquo;intégrer l&rsquo;upload dans le cycle de vie de l&rsquo;entité pour ne pas avoir à appeler la méthode uploadProfilePicture lorsque l&rsquo;on va persister l&rsquo;entité, mais c&rsquo;est un autre sujet que je vous invite à étudier dans le [cookbook](http://symfony.com/doc/current/cookbook/doctrine/file_uploads.html).