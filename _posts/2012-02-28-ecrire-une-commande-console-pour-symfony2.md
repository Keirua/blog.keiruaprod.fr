---
id: 305
title: Ecrire une commande console pour Symfony2
date: 2012-02-28T18:05:50+00:00
author: Keirua
layout: post
guid: http://keiruaprod.fr/blog/?p=305
permalink: /2012/02/28/ecrire-une-commande-console-pour-symfony2/
robotsmeta:
  - index,follow
categories:
  - Symfony2
---
Aujourd&rsquo;hui, nous allons voir comment créer nos propres commandes console pour Symfony2. Si vous utilisez déjà ce framework, vous en avez probablement déjà utilisé quelques unes. S&rsquo;il vous est arrivé de lancer une console et d&rsquo;y taper par exemple  
<code lang="bash">&lt;br />
php app/console doctrine:schema:update&lt;br />
</code>  
ou bien  
<code lang="bash">&lt;br />
php app/console cache:clear&lt;br />
</code>  
alors vous avez utilisé le système de commandes console de Symfony2. Ces commandes sont très utiles, et permettent de simplifier pas mal de choses. La première commande permet de mettre à jour une entité qui a été modifié du côté de la base de données, et la seconde permet de vider le cache. Mais comment faire pour écrire nos propres commandes si l&rsquo;on souhaite nous aussi automatiser des tâches pénibles, récurrentes ou difficiles à réaliser à la main ?  
<!--more-->

  
Dans l&rsquo;exemple qui va suivre, nous allons écrire une commande console pour automatiser la création d&rsquo;un contrôleur. La structure est en effet toujours la même, seul change, à peu de choses prêt, le nom du contrôleur avant de pouvoir réellement commencer à coder, bref on souhaite éviter d&rsquo;écrire toujours la même chose et va écrire une commande pour s&rsquo;en occuper pour nous.

Dans cet exemple donc, nous allons automatiser la création d&rsquo;un contrôlleur très simple, qui va dépendre de 3 paramètres :

  * Le nom du bundle dans lequel le placer
  * Le nom du contrôleur à générer
  * Si nous souhaitons ou non que notre contrôleur hérite du contrôleur de base de Symfony2. De nombreuses raisons permettent de motiver l&rsquo;un ou l&rsquo;autre des choix, nous les verrons dans un prochain article.

Rentrons dans le vif du sujet. Commençons par créer le bundle qui va accueillir notre commande, par une commande console dont nous allons par la suite nous inspirer du principe :  
<code lang="bash">&lt;br />
php app/console generate:bundle --namespace=KeiruaProd/CommandBundle&lt;br />
</code>

Une fois le bundle créé, ajoutez dedans un répertoire Command et placez-y un fichier ControllerGeneratorCommand.php. Ce fichier va accueillir le code de notre nouvelle commande. Commençons par y placer le minimum vital pour une commande.

<code lang="php">&lt;br />
<?php
namespace KeiruaProd\CommandBundle\Command;
 
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
 
class ControllerGeneratorCommand extends ContainerAwareCommand
{
    protected function configure()
    {
        $this->setName('keiruaprod:generate');&lt;br />
    }&lt;/p>
&lt;p>	protected function interact(InputInterface $input, OutputInterface $output)&lt;br />
    {&lt;br />
	}&lt;/p>
&lt;p>    protected function execute(InputInterface $input, OutputInterface $output)&lt;br />
    {&lt;br />
    }&lt;br />
}&lt;br />
</code>

On crée une classe ControllerGeneratorCommand, héritée de ContainerAwareCommand, qui contient 3 méthodes. La première, configure, permet de configurer les informations sur la commande. Pour le moment, seul son nom est renseigné, mais c&rsquo;est la dedans que nous allons par la suite configurer les paramètres d&rsquo;entrée de notre fonction, sa description, ainsi qu&rsquo;un message d&rsquo;aide.  
La seconde, interact, permet d’interagir avec l&rsquo;utilisateur. Cela permet de demander à l&rsquo;utilisateur des informations sur les champs s&rsquo;il ne pas pas fait directement en lançant la commande avec des arguments, ou bien de lui demander plus d&rsquo;informations. Les paramètres $input et $output servent à réaliser les entrées/sorties avec la console.  
La dernière méthode, execute, sert à réaliser l&rsquo;action qu&rsquo;est censée réaliser votre commande une fois qu&rsquo;elle dispose de toutes les informations.

A partir de cela, lancez une console et placez-vous dans votre application Symfony, puis faites  
<code lang="bash">&lt;br />
php app/console&lt;br />
</code>  
Cette commande permet de lister les commandes disponibles. Dans la liste, vous pouvez voir que la commande keiruaprod:generate est disponible. Vous pouvez même l&rsquo;exécuter, mais évidemment, il ne se passera rien, car les méthodes interact et execute sont vides. Avant de les remplir, commençons par donner plus d&rsquo;informations dans la méthode configure.

<code lang="php">&lt;br />
protected function configure()&lt;br />
{&lt;br />
	$this->setName('keiruaprod:generate')&lt;br />
			->setDefinition(array(&lt;br />
				new InputOption('controller', '', InputOption::VALUE_REQUIRED, 'Le nom du controller a creer'),&lt;br />
				new InputOption('bundle', '', InputOption::VALUE_REQUIRED, 'Le bundle dans lequel creer le controlleur'),&lt;br />
				new InputOption('basecontroller', '', InputOption::VALUE_REQUIRED, 'S\'il faut ou non heriter du controlleur de base de Symfony2')&lt;br />
			))&lt;br />
			->setDescription('Genere le code de base pour commencer a utiliser un controlleur')&lt;br />
			->setHelp('Cette commande vous permet de facilement generer le code necessaire pour commencer a travailler avec un controlleur. N\'hesitez pas a vous en servir quand vous avez besoin d\'en creer un !')&lt;br />
			;&lt;br />
}&lt;br />
</code>

Nous avons laissé setName, et nous avons appelé d&rsquo;autres méthodes. setDefinition nous permet de definir quelles sont les options de notre commande, leur importance, ainsi qu&rsquo;une description.  
setDescription nous permet de specificier le texte à afficher à côté de notre commande dans la liste fournie par php app/console. Quand à setHelp, je vous laisse le découvrir en tapant dans votre invite de commande  
<code lang="bash">&lt;br />
php app/console keiruaprod:generate --help&lt;br />
</code>  
He oui, notre commande possede un peu plus d&rsquo;explications désormais, et les paramètres utilisés sont décrits à l&rsquo;utilisateur. Sympa non ? Bon, le truc pénible quand même, c&rsquo;est que pour le moment, notre commande ne fait rien.

Créons le modèle des fichiers que nous allons générer dans le fichier Resources/views/ControllerCommande/Controller.php.twig  
<code lang="php">&lt;br />
<?php

namespace {{ namespace }}\Controller;
{% if basecontroller %}
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
{% endif %}

class {{controller}}Controller {% if basecontroller %} extends Controller {% endif %}
{
}
</code>&lt;/p>
&lt;p>Le template est très simple, il ne contient même pas de méthodes à l'intérieur. Ce sera à nous de les ajouter par la suite. Le but désormais va être de générer ce fichier à partir des informations fournies par l'utilisateur. Une bonne partie sont donnés directement en paramètres de la commande, mais ils nous faut par exemple faire quelques opérations pour obtenir le namespace à partir du nom du bundle. Rien de bien compliqué toutefois.&lt;/p>
&lt;p>Avant d'écrire le code de génération, il nous faut lire les informations. En effet, l'utilisateur ne rentre pas nécessairement tous les paramètres directement en arguments de la commande. Nous allons concevoir un générateur intéractif, où l'utilisateur peut, au cours de l'exécution de la commande, spécifier ses paramètres.&lt;br />
Commençons par ajouter les espaces de noms nécessaires au sommet du fichier :&lt;br />
&lt;code lang="php">&lt;br />
use Symfony\Component\Console\Command\Command;&lt;br />
use Symfony\Component\Console\Input\InputOption;&lt;br />
use Symfony\Component\Console\Input\InputArgument;&lt;br />
use Symfony\Component\Console\Input\InputInterface;&lt;br />
use Symfony\Component\Console\Output\OutputInterface;&lt;br />
use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;&lt;br />
use Sensio\Bundle\GeneratorBundle\Command\Helper\DialogHelper;&lt;br />
</code>

puis mettez à jour le code de la fonction interact :  
<code lang="php">&lt;br />
protected function interact(InputInterface $input, OutputInterface $output)&lt;br />
{&lt;br />
	// On affiche quelques infos&lt;br />
	$dialog = $this->getDialogHelper ();&lt;br />
	$output->writeln(array(&lt;br />
		'',&lt;br />
		'      Bienvenue dans le generateur de controlleurs',&lt;br />
		'',&lt;br />
		'Cet outil va vous permettre de generer rapidement votre controlleur',&lt;br />
		'',&lt;br />
	));&lt;/p>
&lt;p>	// On récupère les informations de l'utilisateur&lt;br />
	$controller = $dialog->ask(&lt;br />
					$output,&lt;br />
					$dialog->getQuestion('Nom du controlleur', $input->getOption('controller')),&lt;br />
					$input->getOption('controller')&lt;br />
				);&lt;/p>
&lt;p>	$basecontroller = $input->getOption('basecontroller');&lt;br />
	if (!$basecontroller && !$dialog->askConfirmation($output, $dialog->getQuestion('Voulez vous que le bundle etende le controlleur de base de Symfony2 ?', 'yes', '?'), true)) {&lt;br />
		$basecontroller = false;&lt;br />
	}&lt;/p>
&lt;p>	$bundleName = $dialog->ask(&lt;br />
					$output,&lt;br />
					$dialog->getQuestion('bundle', $input->getOption('bundle')),&lt;br />
					$input->getOption('bundle')&lt;br />
				);&lt;/p>
&lt;p>	// On sauvegarde les paramètres&lt;br />
	$input->setOption('controller', $controller);&lt;br />
	$input->setOption('basecontroller', $basecontroller);&lt;br />
	$input->setOption('bundle', $bundleName);&lt;br />
}&lt;/p>
&lt;p>protected function getDialogHelper()&lt;br />
{&lt;br />
	$dialog = $this->getHelperSet()->get('dialog');&lt;br />
	if (!$dialog || get_class($dialog) !== 'Sensio\Bundle\GeneratorBundle\Command\Helper\DialogHelper') {&lt;br />
		$this->getHelperSet()->set($dialog = new DialogHelper());&lt;br />
	}&lt;/p>
&lt;p>	return $dialog;&lt;br />
}&lt;br />
</code>

La méthode getDialogHelper nous permet d'utiliser le DialogHelper du GeneratorBundle pour utiliser la méthode getQuestion. Si vous avez déjà regardé le code de ce générateur, vous verrez sans doute d'où vient une bonne partie de cet article, car la méthodologie utilisée est en effet la même que pour nous. Les informations obtenues sont stockées dans les options d'entrée ($input->setOption(...)) afin d'être récupérées par la suite dans execute. Nous aurions pû faire autrement (en utilisant une variable membre de la classe par exemple), mais cela permet de centraliser les informations d'entrée.

Il est maintenant temps d'écrire la méthode execute, qui va utiliser les informations fournies par l'utilisateur pour construire le fichier du contrôleur à générer et le sauvegarder au bon endroit dans le bundle spécifié.

<code lang="php">&lt;br />
protected function execute(InputInterface $input, OutputInterface $output)&lt;br />
{&lt;br />
	$dialog = $this->getDialogHelper();&lt;/p>
&lt;p>	if ($input->isInteractive()) {&lt;br />
		if (!$dialog->askConfirmation($output, $dialog->getQuestion('Do you confirm generation', 'yes', '?'), true)) {&lt;br />
			$output->writeln('&lt;error>Command aborted&lt;/error>');&lt;/p>
&lt;p>			return 1;&lt;br />
		}&lt;br />
	}&lt;br />
	// On recupere les options&lt;br />
	$controller = $input->getOption('controller');&lt;br />
	$basecontroller = $input->getOption('basecontroller');&lt;br />
	$bundleName = $input->getOption('bundle');&lt;/p>
&lt;p>	// On recupere les infos sur le bundle nécessaire à la génération du controller&lt;br />
	$kernel = $this->getContainer()->get('kernel');&lt;br />
	$bundle = $kernel->getBundle ($bundleName);&lt;br />
	$namespace = $bundle->getNamespace();&lt;br />
	$path = $bundle->getPath();&lt;br />
	$target = $path.'/Controller/'.$controller.'Controller.php';&lt;/p>
&lt;p>	// On génère le contenu du controlleur&lt;br />
	$twig = $this->getContainer()->get ('templating');&lt;/p>
&lt;p>	$controller_code = $twig->render ('KeiruaProdCommandBundle:ControllerCommand:Controller.php.twig',&lt;br />
		array (&lt;br />
			'controller' => $controller,&lt;br />
			'basecontroller' => $basecontroller,&lt;br />
			'namespace' => $namespace&lt;br />
			)&lt;br />
		);&lt;/p>
&lt;p>	// On crée le fichier&lt;br />
	if (!is_dir(dirname($target))) {&lt;br />
		mkdir(dirname($target), 0777, true);&lt;br />
	}&lt;br />
	file_put_contents($target, $controller_code);&lt;/p>
&lt;p>	return 0;&lt;br />
}&lt;br />
</code>

Dans cette méthode, on vérifie que que l'utilisateur souhaite bien générer un contrôleur. Si c'est le cas, à partir du nom du bundle et grâce au composant HttpKernel (obtenu grâce au service 'kernel'), on obtient les informations sur le namespace du bundle et le chemin dans lequel stocker le fichier que nous allons générer. Ces informations sont fournies au service de template qui se charge de générer le contenu du fichier à l'aide du modèle que nous avons évoqué plus haut. Cela fonctionne comme si nous voulions générer une page HTML avec Twig depuis un controlleur, sauf que pour accéder à Twig nous devons ici utiliser le container de services au lieu de nous en servir directement comme c'est souvent le cas.  
Le code du controlleur est enfin sauvegardé dans le fichier adéquat, le répertoire le contenant étant créé si c'est nécessaire.

On a terminé avec le code, plus qu'à vérifier que ça marche.

Maintenant, nous pouvons lancer notre commande depuis une console. Si l'utilisateur ne fournit pas de paramètres, il lui est demandé de préciser les 3 élémentes nécessaires. Par contre, si certaines valeur sont précisés, il lui est demandé de valider que c'est bien les paramètres qu'il souhaite utiliser.  
Lancez la commande suivante pour tester que notre commande fait bien ce que souhaitons :  
<code lang="bash">&lt;br />
php app/console keiruaprod:generate --controller=Article --basecontroller=yes --bundle=AcmeDemoBundle&lt;br />
</code>  
Après execution, vous pouvez vérifier dans src/Acme/DemoBundle/Controller qu'un nouveau fichier ArticleController.php est désormais présent, et que ce controlleur étend bien la classe Controller du FrameworkBundle.

Et voila ! C'est finalement relativement simple, le code de notre commande est très simpliste et vous pouvez désormais le compléter pour ajouter la possibilité de créer dynamiquement des méthodes, pour créer les routes associées.... quoi qu'il en soit nous avons utilisé plusieurs notions que nous n'avions pas encore abordées sur ce blog, comme le container de services, sur lesquelles je reviendrais plus en détail dans les prochains articles.