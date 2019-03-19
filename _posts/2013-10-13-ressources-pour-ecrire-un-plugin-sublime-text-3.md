---
id: 676
title: Ressources pour écrire un plugin Sublime Text 3
date: 2013-10-13T10:53:55+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=676
permalink: /2013/10/13/ressources-pour-ecrire-un-plugin-sublime-text-3/
keywords:
  - python, sublime text 3, st3, formatSQL, plugin
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - formatSQL
  - plugin
  - python
  - st3
  - sublime text 3
---
La semaine dernière, j&rsquo;ai réécrit pour Sublime Text 3 l&rsquo;extension FormatSQL, qui me servait régulièrement dans la version 2, mais qui n&rsquo;est plus compatible. L&rsquo;objectif : prendre une chaine SQL mal formatée, et la formater de manière lisible. Le code final de mon petit plugin est [sur Github](https://github.com/Keirua/stsqlformat).

J&rsquo;ai eu étonnamment beaucoup de mal à comprendre comment démarrer. La plupart des bouts de code que j&rsquo;ai trouvé sur les net, y compris sur le site officiel, ne fonctionnent que sous Sublime Text 2, et n&rsquo;étaient pas compatibles.

### Démarrer

Pour démarrer, c&rsquo;est en fait très simple, encore faut-il le savoir : en cliquant sur **Tools -> new Plugin**, on obtient le code minimal d&rsquo;un plugin, point de départ que je ne trouvais pas.

<code lang="python">&lt;br />
import sublime, sublime_plugin&lt;/p>
&lt;p>class ExampleCommand(sublime_plugin.TextCommand):&lt;br />
	def run(self, edit):&lt;br />
		self.view.insert(edit, 0, "Hello, World!")&lt;br />
</code>

C&rsquo;est du python, ST3 embarque la version 3.3, d&rsquo;où l&rsquo;origine de conflits pour de nombreux packages, qui utilisent des librairies qui ne fonctionnent plus en python 3.3.

### Exécuter le plugin

Quand on enregistre ce fichier, on est déjà positionné dans le bon répertoire (chez moi : ~/.config/sublime-text-3/Packages/User). On sauvegarde example.py, et sans redémarrer, on peut utiliser le nouveau plugin, de 2 manières :

**Depuis la console :**  
on l&rsquo;ouvre avec ctrl+\`, et on tape view.run_command(&lsquo;example&rsquo;). Le plugin s&rsquo;exécute !  
**Depuis un nouveau binding :**  
On crée un nouveau raccourci, en allant dans Preferences -> Key bindings &#8211; User, où l&rsquo;on ajoute :  
<code lang="javascript">&lt;br />
{ "keys": ["ctrl+alt+f"], "command": "example" }&lt;br />
</code>  
Maintenant, à chaque fois que l&rsquo;on appuiera sur ctrl+alt+f, notre plugin s&rsquo;executera.

### Et maintenant, à vous de jouer !

  * La **documentation** de l&rsquo;API est un peu spartiate, en particulier si comme moi vous n&rsquo;avez jamais écrit de python (avec quelques exemples, ca passerait mieux quand même) : [https://www.sublimetext.com/docs/3/api_reference.html](https://www.sublimetext.com/docs/3/api_reference.html "Sublime text 3 API reference")
  * Vous pourrez trouver pas mal d&rsquo;**exemples** en regardant le code de sublime directement sur Github : <https://github.com/cj/sublime/tree/master/Default> (delete\_word.py, duplicate\_line.py&#8230;).
  * Un article détaille pas mal de choses plus en détails sur **comment aller plus loin** (menu, vrai packaging de votre plugin&#8230;) : <http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/>
  * En cas de problème, j&rsquo;ai trouvé quelques réponses sur le **forum** de développement de plugin : <http://www.sublimetext.com/forum/viewforum.php?f=6>

Bon courage !