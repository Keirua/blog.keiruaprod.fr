---
id: 658
title:
  - Corriger le raccourci de partage de vue de SublimeText
date: 2013-09-25T06:57:18+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=658
permalink: /2013/09/25/corriger-le-raccourci-de-partage-de-vue-de-sublimetext/
keywords:
  - SublimeText, Sublime Text, astuce, partage de vue, astuce
description:
  - Comment corriger le raccourci de partage de vue de Sublime Text, qui ne fonctionne pas sur les claviers AZERTY.
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - astuce
  - configuration
  - Sublime Text
  - SublimeText
lang: fr
---
Une fonctionnalité très sympa de Sublime Text est pouvoir partager son écran en 2 (**View -> Layout -> Columns: 2** par exemple).

Quand on a un écran un peu grand, cela permet par exemple de comparer des bouts de code quand on débuggue, ou pour adapter un exemple trouvé sur le net. Si l&rsquo;écran est petit, **ctrl+k, ctrl+b** permet de masquer ou afficher la barre latérale le temps de faire ce que l&rsquo;on souhaite.

Sur un clavier Azerty, le raccourci pour partager l&rsquo;écran ne fonctionne pas (avec les produits Apple, il semble que ce soit OK). Le coupable ? Le raccourci. Il faut appuyer sur **alt + maj + 2**. Hors pour faire 2&#8230; il faut appuyer sur Maj. Sur nos claviers, l&rsquo;éditeur de texte le plus sympa que je connaisse est donc perdu. La solution ? Redéfinir les touches nécessaires pour le binding en question. Allez dans **Preferences -> Key bindings &#8211; User**, et configurez les touches de la manière suivante :

<code lang="javascript">&lt;br />
[&lt;br />
    { "keys": ["alt+2"],&lt;br />
        "command": "set_layout",&lt;br />
        "args":&lt;br />
        {&lt;br />
            "cols": [0.0, 0.5, 1.0],&lt;br />
            "rows": [0.0, 1.0],&lt;br />
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]&lt;br />
        }&lt;br />
    },&lt;br />
    {&lt;br />
        "keys": ["alt+1"],&lt;br />
        "command": "set_layout",&lt;br />
        "args":&lt;br />
        {&lt;br />
            "cols": [0.0, 1.0],&lt;br />
            "rows": [0.0, 1.0],&lt;br />
            "cells": [[0, 0, 1, 1]]&lt;br />
        }&lt;br />
    }&lt;br />
]&lt;br />
</code>

Ici j&rsquo;ai seulement redéfini les associations de touches pour découper l&rsquo;écran en 2 verticalement avec **alt + 1** et **alt + 2**. C&rsquo;est le seul que j&rsquo;utilise, mais si vous voulez la liste complète (pour découper en 3, 4 parties, horizontalement comme verticalement), vous pouvez chercher la commande set_layout dans Preferences -> Key bindings &#8211; Default.

## One more thing&#8230;

Un autre raccourci que je vous recommande d&rsquo;ajouter au même endroit que le précédent. Si comme moi vous travaillez sur des gros projets, et naviguez dans l&rsquo;arborescence à grand coup de cltr+p, vous avez du vous rendre compte qu&rsquo;on a vite fait de ne plus savoir dans quel répertoire se trouve le fichier avec lequel on travaille.

<code lang="javascript">&lt;br />
    { "keys": ["ctrl+alt+r"], "command": "reveal_in_side_bar" }&lt;br />
</code>

A tout moment, appuyez sur **ctrl+alt+r** pour sélectionner le fichier courant dans la barre latérale et le mettre en surbrillance, et ainsi le retrouver dans l&rsquo;arborescence. Des packages (notamment **SyncedSideBar**) permettent de faire cela, mais leur comportement ne me plait pas.

Ha, et tant que vous y êtes, jetez un oeil dans **Preferences -> Settings &#8211; Default**, et prenez 10mn pour adapter les paramètres de configuration à vos besoins dans Preferences -> Settings &#8211; User. Ces quelques détails peuvent vous changer la vie !