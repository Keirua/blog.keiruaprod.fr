---
title: Ajout d'une supervision telegraf/influxdb/grafana
layout: post
lang: fr
---

Il y a quelques temps j'ai ajouté du monitoring dans une pile telegraf/influxdb/grafana.

Voici l'idée:

 - **telegraf** s'occupe de remonter des données à partir de diverses sondes, configurées dans des fichiers textes via un système de plugin en Go.
 - **influxdb** stocke ces données sous forme de séries temporelles
 - **grafana** se charge de l'affichage.

On va ajouter le suivi d'un service `systemd`, et aller afficher un graphique dans grafana à partir de tout ça.

# Modification de la configuration telegraf :

Telegraf remonte le status du process dans influxdb, par défaut à intervalles de 10s, via le plugin procstat: https://github.com/influxdata/telegraf/tree/master/plugins/inputs/procstat

    cat /etc/telegraf/telegraf.conf
    …
    [[inputs.procstat]]
        systemd_unit = "ds_proxy.service"

Quand c'est terminé, on redémarre !

    systemctl restart telegraf

Là, si le service est actif, des données vont être envoyés dans influxdb. On va commencer par regarder ça.

# Vérification 

On se connecte sur la machine de supervision et on vérifie que des données sont remontées dans influxdb:

    $ influx
    Connected to …
    InfluxDB shell version: …
    Enter an InfluxQL query
    > help
    … quelques infos
    > show databases
    name: databases
    name
    ----
    supervision_db
    …
    > use supervision_db
    Using database supervision_db
    # on peut voir qu'il y a des chiffres dans influxdb
    > select time, pid, num_threads, host from procstat where process_name='ds_proxy' limit 10
    # moult lignes

# Configuration de grafana

On peut trouver plein de dashboards tout prêts chez Grafana (https://grafana.com/dashboards), mais c'est super générique et pour des outils plus connus, je n'ai rien trouvé pour systemd/procstat

Pour ajouter le notre:

Dashboard -> Manage -> DS proxy -> add panel (graph) avec la requête suivante:

    SELECT mean("num_threads") FROM "procstat" WHERE $timeFilter GROUP BY time($__interval) fill(0)

    SELECT mean("num_threads") FROM "procstat" WHERE ("host" =~ /^$server$/) AND $timeFilter GROUP BY time($__interval) fill(0)

On peut faire plus subtil (en particulier quand on veut plusieurs serveurs), mais dans l'esprit on a un graphe.

Voila !