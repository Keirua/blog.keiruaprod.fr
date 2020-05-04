---
title: Automatiser la recherche de bugs avec git bisect
author: Keirua
layout: post
lang: fr
---

Je suis tombé sur un bug dans une branche partagée (`dev`) et aucun des commits récents ne semblaient en cause. Certains tests automatisés (avec `rspec`) échouaient.

```bash
$ bin/rspec ./spec/services/expired_dossiers_deletion_service_spec.rb:249
6 examples, 6 failures
```

Comment remonter au commit qui a introduit cette erreur ? `git bisect` peut s'occuper de trouver ça tout seul:

```bash
$ git bisect start
```

On identifie un commit qui fonctionne: le 120ème commit avant le commit courant de la branche dev, par exemple.

```bash
$ git bisect good dev~120
```

On identifie un commit qui échoue:

```bash
$ git bisect bad c992eb654
Bisecting: 169 revisions left to test after this (roughly 7 steps)
[72d003b62c89d5ddf5a829ce6e28075bbeadd375] javascript: fix missign argument to catch
```

On automatise la commande à tester:

```bash
$ git bisect run bin/rspec ./spec/services/expired_dossiers_deletion_service_spec.rb:249
```

On laisse tourner quelques instants… et rapidement la réponse arrive:

```bash
51224fad4990a72a097f572caec23c6fe2c96268 is the first bad commit
commit 51224fad4990a72a097f572caec23c6fe2c96268
Author: [redacted]
Date:   Wed Mar 25 10:38:17 2020 +0100

    Refactor scopes with intervals and use Time.zone.now

:040000 040000 ec52b83ef15a4fe883bb65b4571c021112040e08 533bad13cb9116bf9efaa5db31743721c9069c20 M  app
bisect run success
```

Après il reste à corriger le problème. Mais notez qu'on a laissé la machine identifier une source potentielle parmi de nombreux commits. Pendant ce temps là, on a pu aller se faire couler un café. Ça n'arrive pas souvent, mais c'est plutôt agréable.