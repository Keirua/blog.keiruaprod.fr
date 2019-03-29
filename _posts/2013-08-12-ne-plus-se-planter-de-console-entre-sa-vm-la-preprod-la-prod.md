---
id: 593
title:
  - Ne plus se planter de console entre sa VM, la préprod, la prod...
date: 2013-08-12T21:07:59+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=593
permalink: /2013/08/12/ne-plus-se-planter-de-console-entre-sa-vm-la-preprod-la-prod/
keywords:
  - Revelation, bash, ubuntu, process, astuce, préprod, serveurs
description:
  - "A l'aide d'un code couleur et de l'applicationRevelation, il est facile de réduire les risques de se tromper de machine lorsque l'on se connecte régulièrement à plusieurs machines via SSH. "
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - astuce
  - bash
  - préprod
  - process
  - Revelation
  - serveurs
  - ubuntu
lang: fr
---
Je travaille en permanence avec plusieurs machines différentes pour me connecter à des serveurs de développement, de préproduction, à ma machine virtuelle ou à des machines de productions. Après avoir oublié plusieurs fois certains mots de passe, puis m&rsquo;être planté une fois ou deux de terminal et avoir lanché des scripts sur la mauvaise machine, j&rsquo;ai commencé à utiliser des codes couleurs pour les différentes machines que j&rsquo;utilise. Et comme il est pénible de changer les codes couleurs à chaque connection, je me suis finalement mis à utiliser **Revelation** pour résoudre les deux problèmes en une fois.

<div id="attachment_600" style="width: 310px" class="wp-caption alignright">
  <img src="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/codes_couleur-300x180.png" alt="L&#039;astuce : une couleur pour chaque machine" width="300" height="180" class="size-medium wp-image-600" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/codes_couleur-300x180.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/08/codes_couleur.png 940w" sizes="(max-width: 300px) 100vw, 300px" />
  
  <p class="wp-caption-text">
    L&rsquo;astuce : une couleur pour chaque machine
  </p>
</div>

Révélation est en effet un gestionnaire de mots de passe, qui sert à les centraliser, et à lancer diverses applications qui les utilisent. Un mot de passe maitre sert à protéger l&rsquo;accès à des personnes non désirées (dans une certaine mesure). Je m&rsquo;en sers donc pour me stocker les mots de pass de connection SSH, et pour me connecter directement aux machines distantes en SSH.

L&rsquo;astuce pour ne pas me tromper de machine, c&rsquo;est que chacune d&rsquo;entre elle a une couleur différente. Rouge (comme danger) pour la machine de production, vert pour une VM, et ainsi de suite. 

Pour faire pareil, il suffit d&rsquo;installer Revelation (apt-get install revelation), puis de faire 3 choses :

## Créer un profil pour les couleurs des différentes machines :

<div id="attachment_598" style="width: 310px" class="wp-caption alignright">
  <img src="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/profils-300x191.png" alt="N&#039;ayez pas peur d&#039;avoir autant de profils que de machine" width="300" height="191" class="size-medium wp-image-598" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/profils-300x191.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/08/profils.png 516w" sizes="(max-width: 300px) 100vw, 300px" />
  
  <p class="wp-caption-text">
    N&rsquo;ayez pas peur d&rsquo;avoir autant de profils que de machine
  </p>
</div>

Faire la manipulation suivante (sur Ubuntu) pour vos différentes machines :  
Ouvrir une console  
Edition -> profils -> nouveau  
On lui **donne un nom** (notez le, il va servir plus tard), et le fait se baser sur un profil déjà plaisant  
Dans l&rsquo;onglet couleur, il suffit de décocher « utiliser les couleurs du thème système », et de choisir des couleurs (de texte et d&rsquo;arrière plan) qui conviennent.

Quand vous avez terminé, vous devriez avoir autant de profils que vous utilisez de machine différente, et chacune d&rsquo;entre elle aura une couleur différente. Vous pouvez remarquer que je nomme mes profils sous la forme profilXXX, histoire de m&rsquo;y retrouver.

## Configurer les raccourcis dans Revelation :

<div id="attachment_599" style="width: 310px" class="wp-caption alignright">
  <a href="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/config_vm.png"><img src="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/config_vm-300x200.png" alt="N&#039;oubliez pas de mettre le nom du profil dans &quot;Domaine&quot;" width="300" height="200" class="size-medium wp-image-599" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2013/08/config_vm-300x200.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2013/08/config_vm.png 581w" sizes="(max-width: 300px) 100vw, 300px" /></a>
  
  <p class="wp-caption-text">
    N&rsquo;oubliez pas de mettre le nom du profil dans « Domaine »
  </p>
</div>

Une fois qu&rsquo;on a les différents profils, il faut ensuite configurer les différentes connection SSH, comme dans l&rsquo;image de droite.  
On crée un nouveau raccourci de type shell, avec le nom de son choix, puis on remplit le nom d&rsquo;hôte, le nom d&rsquo;utilisateur et le mot de passe nécessaire à la connection à son shell.

L&rsquo;astuce pour lancer la connection avec le profil désiré, c&rsquo;est de mettre le nom du profil dans le champ « domaine ». On va ensuite configurer Revelation pour utiliser cette information comme nous le souhaitons.

N&rsquo;oubliez pas de sauvegarder votre configuration Revelation (ctrl+S, ou le gros bouton enregistrer)

## Configurer l&rsquo;utilisation des profils au lancement des connections SSH :

Dernière étape, il faut préciser à Revelation d&rsquo;utiliser nos profils lorsque l&rsquo;on lance un terminal. Pour celà, il suffit d&rsquo;aller dans Editer -> Préférences -> Commandes de lancement, et dans la ligne SSH, de mettre ce qui suit :

<code lang="bash">&lt;br />
gnome-terminal %(--profile=%d%) -x ssh %(-l %u%) %h&lt;br />
</code>

Cette ligne parle d&rsquo;elle même, on lance un terminal avec une connection ssh dont les options sont les paramètres de configuration de la machine donnée, et on choisit le profil correspondant pour le terminal.

Terminé !

L&rsquo;utilisation est simple : on ouvre sa configuration dans revelation, choisit une machine, et le mot de passe est copié dans le presse papier. Sous Ubuntu, on peut le coller avec clic-molette, on appuie sur entrée, et c&rsquo;est bon, on est connecté à sa machine. Et voila, fini les pertes de mot de passe, et fini les commandes lancées sur la mauvaise machine. Merci à Antho pour l&rsquo;astuce !