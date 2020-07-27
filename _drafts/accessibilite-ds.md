Rendre DS accessible pour les usagers.md

 - contexte: DS, accessibilité des services publics
 - le flow utilisateur
 - les pages publiques faciles
 - intégration en CI pour éviter les régressions
 - comment on fait des tests

# DS, à quoi ça sert

## Déposer un dossier

Cela consiste à:
 - arriver sur la page d'accueil d'un formulaire
 - s'identifier (via france connect, ou en créant un compte)
 - remplir un formulaire et le soumettre

## Suivre l'avancement d'un dossier

Une fois un dossier déposé, quelques écrans permettent de voir:
 - la liste des dossiers qu'on a déposé
 - pour un dossier en particulier, on peut regarder les informations déposées, et éventuellement échanger avec l'administration

La méthodologie d’audit employée repose sur le référentiel français RGAA 4, consultable à l’adresse suivante : https://www.numerique.gouv.fr/publications/rgaa-accessibilite/methode/criteres

# Commence a y avoir du volume
# Rendre accessible, c'est quoi, pour qui ?

# Les quick win
# Quelques outils

 - [Wave](https://wave.webaim.org/extension/) a une extension chrome/firefox qui permet de tester
 - [Axe](https://addons.mozilla.org/fr/firefox/addon/axe-devtools/) permet de faire la même chose, mais dans la console
 - [HeadingsMap](https://addons.mozilla.org/fr/firefox/addon/headingsmap/) permet de voir la structure des titres: est-ce qu'il y a bien un titre de niveau 1 ? Les titres sont-ils bien dans le bon ordre (pas de h3 avant un h2) ?
 - [Asqatasun](https://asqatasun.org/) permet de faire un audit d'accessibilité de toute l'application

Rendre DS accessible

Accessibilité de DS

https://github.com/betagouv/demarches-simplifiees.fr/wiki/Accessibilit%C3%A9

https://github.com/betagouv/demarches-simplifiees.fr/pull/5185/files

# Intégration en CI

Là, c'est plus compliqué.

nokogiri:
https://nokogiri.org/tutorials/ensuring_well_formed_markup.html

https://github.com/w3c-validators/w3c_validators/issues
https://github.com/validator/validator

https://github.com/gjtorikian/html-proofer
 -> prend que des fichiers
https://github.com/svenkreiss/html5validator

Automated accessibility checkers: https://news.ycombinator.com/item?id=23244703
 - IBM equal access: https://github.com/IBMa/equal-access
 - Google Lighthouse: https://developers.google.com/web/tools/lighthouse/#cli
 - Wave fournit une API, mais c'est très cher

# Rendre le site accessible vite fait

Les écrans concernés pour le moment, c'est les écrans globalement statiques:

 - commencer
 - sign_up
 - sign_in
 - formulaire
 - merci
 - homepage
 - liste des dossiers
 - messagerie
 - page de contact

Les critères:
 - w3c compatible https://validator.w3.org/
 - Avoir un h1 par page + hiérarchie descendate

# Rendre vraiment le site accessible

 - Contraste (-> revoir la charte graphique de l'application)
 - Tout le parcours accessible au clavier
   - L'essentiel des difficultés, c'est le dépot de formulaire:
    - gestion des PJs
    - carte !
    - champs à sélection multiple


Utilisation d'un plugin pour tester l'accessibilité (proposition de https://addons.mozilla.org/fr/firefox/addon/axe-devtools/ )
Faire passer https://wave.webaim.org sur les écrans