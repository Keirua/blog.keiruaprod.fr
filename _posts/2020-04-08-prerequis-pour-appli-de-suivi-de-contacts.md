---
title: 10 prérequis pour l'évaluation d'applications de «suivi de contact Coronavirus»
author: Keirua
layout: post
lang: fr
---

Cet article est la traduction d'un article du [Chaos Computer Club](https://en.wikipedia.org/wiki/Chaos_Computer_Club) du 6 avril 2020 sur les conditions que devraient respecter une [application de suivi de contact](https://www.ccc.de/en/updates/2020/contact-tracing-requirements) dans le cadre du Covid-19. Les experts de la surveillance sont unanymes ; [Tristan Nitot](https://standblog.org/blog/post/2020/04/08/Covid-19-et-la-surveillance), [Olivier Tesquet](https://twitter.com/oliviertesquet/status/1247823274597404672), ou encore [Amaelle Guiton](https://twitter.com/amaelle_g/status/1247928366621167616), tous constatent la même chose. Les idées évoluent vite dans l'esprit du public et du gouvernement dans ce qu'il est tolérable d'accepter de changer pour sortir au plus vite de la crise sanitaire, et les risques de dérive sont majeurs. Si nous devons aller dans la direction d'une telle application, il faudra être très vigilant pour ne pas avancer un grand coup et dans la durée dans une société de surveillance.

Les remarques du CCC me paraissent donc essentielles et j'aimerais qu'un maximum de gens les aient en tête au cours des discussions qui, en fait, ont déja démarré. Voici la traduction, l'[original est ici](https://www.ccc.de/en/updates/2020/contact-tracing-requirements).

<hr />

Les «applications Corona» sont sur les lèvres de tout le monde comme un moyen de contenir l'épidémie du SARS-CoV-2. Le CCC publie 10 prérequis pour leur évaluation d'un point de vue technique et sociétal.

Actuellement, le «suivi de contact» supporté techniquement est considéré comme un moyen de lutter contre la diffusion du SARS-CoV-2 d'une manière plus ciblée. L'idée générale est de permettre une plus grande liberté de mouvement pour la majorité de la société à travers un suivi rapide et en interrompant les chaines d'infection. Les contacts des personnes infectées devraient être alertées plus rapidement et ainsi pouvoir se mettre en quarantaine plus rapidement. Cela permet, ensuite, de prévenir les avancées des contaminations. Une «appli Corona» ne nous protègerait ni nous, ni nos contacts: elle serait conçue pour casser des chaines d'infection en protégeant les contacts de nos contacts.

## Le suivi des contacts comme une technologie du risque

Il y a un grand nombre de suggestions pour l'implémentation technique de ce concept. Ces propositions vont de systèmes dystopiqus de surveillance totale à des méthodes ciblées, complètement anonymes d'alerter les personnes potentiellement infectées sans connaissance de personnes spécifiques.

En principe, le concept d'une «appli Corona» implique une énorme risque à cause des données de contact et de santé qui sont collectées. En même temps, c'est une opportunité pour les concepts et les technologies de «vie privée par design» (privacy-by-design), développés par les communauté crypto et vie privée ces dernières décennies. Avec l'aide de ces technologies, il est possible de gérer le potentiel épidémiologique du suivi de contacts sans créer un désastre pour la vie privée. Pour cette raison seule, tous les concepts qui brisent ou même mettent en danger la vie privée doivent être strictement rejetés.

Dans ce qui suit, nous soulignons les prérequis minimum sociaux et technologiques pour de telles technologies. Le CCC se voit lui-même comme un conseiller et un observateur dans ce débat. Nous ne recommanderons pas d'appli spécifique, de concepts ou de procédures. Cependant nous mettrons en garde contre l'usage d'applications qui ne respecteront pas cet prérequis.

## I Prérequis sociétaux

### 1 Sens épidémiologique et but

Les prérequis de base est que le «suivi de contact» peut de manière réaliste aider significativement et de manière vérifiable à réduire le nombre d'infections. La validation de cette affirmation est la responsabilité de l'épidémiologie. S'il s'avère que le «suivi de contact» par application n'est pas utile ou ne remplit pas ce but, l'expérience doit être arrêtée.

L'application et toutes les données collectées doivent être utilisées exclusivement pour combattre les chaines d'infection du SARS-CoV-2. Tout autre usage doit être empêché techniquement aussi loin que possible et être interdit légalement.

### 2 Volontariat et liberté contre les discriminations

Pour une efficacité significative épidémiologique, une appli de «suivi de contact» nécessite un haut degré de dissémination dans la société. Cette large distribution ne doit pas être accomplie par la force, mais seulement en mettant en oeuvre un système de confiance qui respecte la vie privée. Dans cette optique, il ne doit pas y avoir de barrière par des tarifs ainsi qu'aucune incitation financière à l'usage.

Les gens qui refusent de l'utiliser ne doivent pas subir de conséquences négatives. S'en assurer est une question de politique et de législation.

L'application doit régulièrement informer les gens de son fonctionnement. Elle doit permettre simplement d'être temporairement désactivée ou supprimer de manière permanente. Les mesures restrictives, par exemple de type «bracelet électronique», pour controller l'application des restrictions de contact, ne doivent pas être implémentées.

### 3 Vie privée fondamentale

C'est seulement avec un concept convaincant basé sur le principe de vie privée que l'acceptation sociale pourra être obtenue.

En même temps, des mesures technologiques tel que le chiffrement ou les technologies d'anonymisation doivent assurer la vie privée des utilisateurs. Il n'est pas suffisant de se baser sur des mesures organisationnelles, la "confiance" et des promesses. Des bloquages organisationnels ou légaux contre l'accès aux données ne doivent pas être considérés comme suffisants dans le climat social actuel de pensée d'état d'urgence qui rend possible des exceptions extrèmes aux droits constitutionnels à travers l'État d'Urgence Sanitaire.

Nous rejetons l'implication de société développant des technologies de surveillance comme étant du «covid-washing» (ndt: les présenter sous un jour favorable car ils contribuent à lutter contre l'épidémie). Un principe de base est que les utilisateurs ne devraient pas devoir "faire confiance" à qui que ce soit ou à des institutions concernant leurs données, mais doivent pouvoir s'assurer d'une sécurité technique, documentée et testée.

### 4 Transparence et vérifiabilité

Le code source complet de l'application et de l'infrastructure doit être librement accessible sans restrictions d'accès pour permettre un audit par les parties intéressées. Des techniques d'industrialisation reproductibles doivent être utilisées pour que les utilisateurs puissent s'assurer que l'application qu'ils téléchargent a bien été construite à partir du code source audité.

## II Prérequis techniques

### 5 Pas d'entité centrale de confiance

Un suivi de contact complètement anonyme sans serveurs centraux omniscients est techniquement possible. Faire dépendre la vie privée sur la confiance et la compétence des opérateurs des structures centrales n'est techniquement pas nécessaire. Les concepts basés sur cette "confiance" doivent être rejetés.

Par ailleurs, la sécurité promise et la confiance dans les systèmes centralisés ne peut pas être effectivement vérifiée par des utilisateurs. Les systèmes doivent de ce fait être conçus pour garantir la sécurité et la confidentialité des données des utilisateurs exclusivement à travers leur chiffrement, leur concept d'anonymisation et la vérifiabilité du code source.

### 6 Économie des données

Seul un minimum de données et les métadonnées nécessaires pour le but de l'application peuvent être stockées. Cette contrainte empêche la collecte centrale de toute donnée qui n'est pas spécifique à un contact entre des personnes et sa durée.

Si des données additionnelles, tel que les informations de localisation sont enregistrées localement sur les téléphones, les utilisateurs ne doivent pas être forcés ou tentés de transmettre ces données à des tiers, ni même de les publier. Les données qui ne sont plus nécessaires doivent être détruites. Les données sensibles doivent aussi être chiffrées localement sur le téléphone.

Pour la collecte volontaire de données dans une optique de recherche épidémiologique, qui va donc au dela du but initial du suivi de contact, un consentement clair et séparé doit être explicitement obtenu dans l'interface de l'application et il doit être possible, à tout instant, de le révoquer. Ce consentement ne doit pas être un prérequis pour l'utilisation.

### 7 Anonymat

Les données que chaque appareil collecte à propos des autres appareils ne doivent pas permettre de désanonymiser leurs utilisateurs. Les données que les utilisateurs transmettent à propos d'eux-même ne doivent pas permettre de les désanonymiser. Il faut de ce fait que le système puisse être utilisé sans collecter des données personnelles de quelque type. Ce prérequis interdit les informations uniques d'identité.

Les identifiants pour les suivi de contact par des technologies sans fil (par ex. Bluetooth ou ultrason) ne doivent pas permettre de remonter aux personnes et doivent changer régulièrement. Pour cette raison, il est également interdit de connecter ou de dériver ces identifiants avec des données de communication qui les accompagnent, tel que des numéro de téléphones, adresses IP, identifiant de l'appareil…

### 8 Pas de création de profils centraux de mouvements ou de contacts

Le système doit être conçu de telle manière à ce que les profils de mouvement (suivi de localisation) ou les profils de contacts (motifs des contacts fréquents qui permettent de remonter à des personnes spécifiques) ne puissent être établis, intentionnellement ou non. Des méthodes tel que la centralisation de données GPS ou de localisation, ou lier les données à des numéros de téléphone, des comptes sur les réseaux sociaux et autres doivent donc être rejetés par principe.

### 9 Non-liabilité

La conception de la génération de ces identifiants temporaires doit être telle que ces identifiants ne puissent pas être interprétées et liées sans connaissance d'une clé privée controllée par les utilisateurs. Ils ne doivent de ce fait pas être dérivés à partir d'une information identifiant l'utilisateur, directement ou indirectement. Indépendemment du fait que les 






