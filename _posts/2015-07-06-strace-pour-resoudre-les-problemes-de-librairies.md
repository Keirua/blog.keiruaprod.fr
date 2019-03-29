---
id: 824
title: strace pour résoudre les problèmes de librairies
date: 2015-07-06T11:48:12+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=824
permalink: /2015/07/06/strace-pour-resoudre-les-problemes-de-librairies/
robotsmeta:
  - index,follow
categories:
  - Astuce
lang: fr
---
La semaine dernière, j&rsquo;ai eu un problème avec un exécutable, celui de wkhtmltopdf qui n&rsquo;arrivait pas à générer de PDF et le log n&rsquo;était pas clair. D&rsquo;après certaines indications sur StackOverflow, ca pouvait être du à un problème de version de la librairie libjpeg. On peut le vérifier avec strace, c&rsquo;est un utilitaire qui intercepte et loggue tous les appels systèmes, ce qui permet de voir ce qui se passe en fouillant dans les logs. Je ne connaissais pas cet outil, c&rsquo;était une bonne occasion de découvrir.

La commande à inspecter est la suivante :  
<code lang="bash">&lt;br />
$ ./wkhtmltopdf-amd64 in.html out.pdf&lt;br />
</code>  
On prend un fichier html en entrée, et on chercher à générer à en faire un fichier pdf.

Pour inspecter la trace d&rsquo;exécution avec strace, on fait comme ça :  
<code lang="bash">&lt;br />
$ strace -f -o trace.log ./wkhtmltopdf-amd64 in.html out.pdf&lt;br />
</code>  
L&rsquo;option **-f** permet d&rsquo;enregistrer égalements les appels systèmes des processus fils, **-o** indique un fichier dans lequel stocker les logs.

On peut ensuite chercher à voir quels sont les appels au chargement de libjpeg.so. On trouve vite ce qu&rsquo;on cherche :  
<code lang="bash">&lt;br />
$ cat trace.log |grep libjpeg&lt;br />
18590 open("/usr/lib/x86_64-linux-gnu/libjpeg.so.8", O_RDONLY|O_CLOEXEC) = 3&lt;br />
</code>  
On voit donc que l&rsquo;exécutable cherche à charger libjpeg dans sa version 8 dans un répertoire particulier. En cherchant les installations de libjpeg (**$ locate libjpeg**), j&rsquo;ai pu voir que la version installée sur la machine en question est libjpeg.so.62, ce n&rsquo;est donc pas la bonne version, un problème résolu avec un `apt-get install libjpeg8`. Bref, un problème pas banal mais qui m&rsquo;a permis d&rsquo;apprendre plein de choses 🙂