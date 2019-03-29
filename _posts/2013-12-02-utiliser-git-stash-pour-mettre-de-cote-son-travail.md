---
id: 696
title:
  - Utiliser git stash pour mettre de côté son travail
date: 2013-12-02T13:23:58+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=696
permalink: /2013/12/02/utiliser-git-stash-pour-mettre-de-cote-son-travail/
keywords:
  - git, stash, git stash, best practices, versionning
description:
  - Tutoriel ou cours sur comment utiliser git stash afin de pouvoir mettre de côté son travail pour le reprendre ultérieurement
robotsmeta:
  - index,follow
categories:
  - Astuce
tags:
  - best practices
  - git
  - git stash
  - stash
  - versionning
lang: fr
---
Bien que j&rsquo;utilise git depuis un bon moment, j&rsquo;ai longtemps été effrayé par l&rsquo;usage de **git stash**, par peur de perdre du travail. A tort, car elle se révèle finalement très simple d&rsquo;utilisation, et très pratique. Cette commande (to stash = réserver) permet de mettre de côté toutes les modifications en cours sans les commiter, pour pouvoir les reprendre plus tard.

Dans ma manière de travailler, c&rsquo;est utile quand je travaille seul comme quand je travaille avec des collègues. Voici deux cas d&rsquo;utilisation récents :

  * Je travaille sur une fonctionnalité avec un collègue. Il a besoin d&rsquo;un correctif sur un bout de code que j&rsquo;ai écrit avant pour pouvoir continuer à travailler. Je travaille sur une branche &lsquo;feature&rsquo;, et doit donc revenir sur la branche &lsquo;dev&rsquo;, dernière version stable de ma branche de développement, pour y apporter un correctif. Dans ma branche &lsquo;feature&rsquo; actuelle, je suis en plein milieu d&rsquo;un développement, je ne peux absolument pas lui fournir ce nouveau code à moitié terminé, ni faire un commit du code au milieu de son développement pour changer de branche. Je dois donc mettre le code sur lequel je travaille actuellement de côté, pour le reprendre par la suite. 
  * Je travaille sur une fonctionnalité seul, en javascript par exemple. Lors de mon développement, je me rends compte qu&rsquo;avant de pouvoir finir ce que j&rsquo;ai commencé, je dois changer quelque chose ailleurs dans le code (sur la partie PHP qui va exposer une API par exemple). Comme j&rsquo;aime avoir des commits unitaires et fonctionnellement séparés, je préfère avoir les modifications de l&rsquo;API en PHP dans un commit, et celles du JS qui l&rsquo;utilise ensuite. Comme j&rsquo;ai déjà commencé à travailler sur le JS, je dois mettre mon code de côté. 

Ce que j&rsquo;ai longtemps fait dans ces situations, c&rsquo;est de faire un commit temporaire. J&rsquo;ajoutais mes fichiers modifiés, et je laissais un commentaire du type « temporary commit, edit later ». Plus tard, lorsque je revenais sur le code en question, et que le travail terminé, j&rsquo;éditais mon commit via **git commit &#8211;amend**. Cette commande permet d&rsquo;éditer le dernier commit en ajoutant/supprimer des fichiers, et en changeant le message de commit. Attention, c&rsquo;est à utiliser avec soin si vous pushez/pullez du code souvent.

Plutôt que de committer du code temporaire (qui a finalement tendance à pourir l&rsquo;historique avec des commits que j&rsquo;oublie de nettoyer), la solution préconisée par git pour ce genre de choses, c&rsquo;est **git stash**.

Cette commande permet de mettre de côté ses modifications pour les récupérer ultérieurement. Une fois exécutée, on peut ensuite changer de branche, faire ses modifications dans la nouvelle branche et revenir, ou bien faire ses modifications directement dans la branche où l&rsquo;on a réservé les modifications, cela n&rsquo;est pas un problème.

Avec un exemple d&rsquo;utilisation, vous allez voir qu&rsquo;il est très simple de s&rsquo;en servir. Le point de départ : vous êtes en train de travailler, vous avez ajouté certains fichiers, modifiés d&rsquo;autres&#8230; en vous devez mettre les modifications de côté. C&rsquo;est parti, on **stash**.

<code lang="bash">&lt;br />
git stash&lt;br />
Saved working directory and index state WIP on feature_branch: d9e2bb5 merged v5.3.4&lt;br />
HEAD is now at d9e2bb5 merged v5.3.4&lt;br />
</code>

Une fois que c&rsquo;est fait, votre git status est vide. 

<code lang="bash">&lt;br />
[clem@clem:~/dev/currProject] git status -s&lt;br />
## feature_branch&lt;br />
# -> rien, les modifications se sont ajoutées à la pile de la réserve&lt;br />
[clem@clem:~/dev/currProject] git stash list&lt;br />
# Sur un écran à part, on peut voir que la pile&lt;br />
# de la réserve contient un élément: nos modifications&lt;br />
</code>

Vous changez de branche, faites ce que vous avez à faire, puis vient le moment où vous revenez sur la branche courante pour reprendre votre travail là où vous l&rsquo;avez laissé. C&rsquo;est le moment d&rsquo;utiliser **git stash pop**.

<code lang="bash">&lt;br />
[clem@clem:~/dev/currProject] git stash pop&lt;br />
# On branch feature_branch&lt;br />
# You are currently rebasing branch 'bh' on 'fb7b1dc'.&lt;br />
#   (all conflicts fixed: run "git rebase --continue")&lt;br />
#&lt;br />
# You are currently bisecting branch 'bh'.&lt;br />
#   (use "git bisect reset" to get back to the original branch)&lt;br />
#&lt;br />
# Changes not staged for commit:&lt;br />
#   (use "git add &lt;file>..." to update what will be committed)&lt;br />
#   (use "git checkout -- &lt;file>..." to discard changes in working directory)&lt;br />
#&lt;br />
#	modified:   app/Berthe/ServiceXHR/ServiceXHRQuote.php&lt;br />
#	modified:   lib/Evaneos/Berthe/JsonServer.php&lt;br />
#&lt;br />
no changes added to commit (use "git add" and/or "git commit -a")&lt;br />
Dropped refs/stash@{0} (21f9583cd4159df5627307eada103e29fe165431)&lt;br />
[clem@clem:~/dev/currProject] git status -s&lt;br />
## feature_branch&lt;br />
 M app/Berthe/ServiceXHR/ServiceXHRQuote.php&lt;br />
 M lib/Evaneos/Berthe/JsonServer.php&lt;br />
</code>

Comme vous pouvez le voir sur les 2 commandes ci-dessus, **git stash pop** enlève les modifications de la pile, les met dans la branche courante, et supprime le sommet de la pile.

Le stash fonctionnant comme une pile, il peut arriver que l&rsquo;on ne veuille pas récupérer ses modifications. Pour cela, on peut supprimer le dernier élément de la pile via **git stash drop**. Voici à quoi cela ressemble :

<code lang="bash">&lt;br />
[clem@clem:~/dev/currProject] git stash&lt;br />
Saved working directory and index state WIP on feature_branch: d9e2bb5 merged v5.3.4&lt;br />
HEAD is now at d9e2bb5 merged v5.3.4&lt;br />
# Je sauvegarde les modifications&lt;br />
[clem@clem:~/dev/currProject] git stash drop&lt;br />
Dropped refs/stash@{0} (befd3f17f416548c30624a01118b609ebb1bc0a8)&lt;br />
# Je n'en ai plus besoin, je les supprime du stash.&lt;br />
[clem@clem:~/dev/currProject] git status -s&lt;br />
## feature_branch&lt;br />
# Ma branche courante est vide. Dans cet exemple, c'est comme&lt;br />
# si j'avais fait git reset HEAD --hard.&lt;br />
</code>

Et voila, non seulement c&rsquo;est plus élégant que des commit temporaires, mais c&rsquo;est aussi très simple d&rsquo;utilisation.