---
id: 684
title: Configurer Vagrant pour DigitalOcean
date: 2013-11-21T07:33:08+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=684
permalink: /2013/11/21/digitalocean-vagrant/
robotsmeta:
  - index,follow
categories:
  - Non classé
lang: fr
archived: true
---
Depuis quelques temps, j&rsquo;ai un serveur chez [DigitalOcean](https://www.digitalocean.com/), qui me sert principalement pour bricoler des petites applis, et jouer autour de nouvelles technos. DigitalOcean m&rsquo;a séduit par le rapport pricing/résultat. Même s&rsquo;il y a des choses à redire, où s&rsquo;il existe des offres similaires moins chères, je suis très satisfait de pouvoir créer/détruire des machines virtuelles en 2 clics. Cela correspond en fait totalement à mon cas d&rsquo;utilisation, qui consiste à monter une machine pour tester une techno, bidouiller dessus, et la détruire quand j&rsquo;ai fait le tour de ce que je voulais voir.

Par contre, il est du coup un peu pénible de devoir réinstaller sa machine virtuelle à chaque fois. Installer un LAMP basique avc phpmyadmin se fait assez vite, ça tient en quelques ligne de bash :

<code lang="bash">&lt;br />
#!/bin/sh&lt;br />
apt-get update&lt;br />
#install apache&lt;br />
apt-get install apache2&lt;br />
#install mysql&lt;br />
apt-get install mysql-server&lt;br />
mysql_secure_installation&lt;br />
#install php&lt;br />
apt-get install php5 php-pear php5-suhosin php5-mysql&lt;br />
service apache2 restart&lt;br />
# install phpmyadmin&lt;br />
apt-get install phpmyadmin&lt;br />
ln -s /usr/share/phpmyadmin/ /var/www&lt;br />
</code>

Mais dès qu&rsquo;on veut faire quoi que ce soit de plus évolué, la complexité augmente rapidement. En plus d&rsquo;installer des paquets il faut aller modifier des fichiers de configuration, ce qui devient rapidement chronophage, et me détourne de l&rsquo;essentiel, le développement. Avec l&rsquo;habitude on finit par connaitre les écueils à éviter pour aller vite, mais on y passe quand même du temps.

C&rsquo;est là où [Vagrant](http://www.vagrantup.com/) devient intéressant. Couplés à [PuPHPet](https://puphpet.com/) et DigitalOcean, j&rsquo;ai personnellement atteint le nirvana de l&rsquo;installation de VM en à peine 2H.

**Vagrant** sert à piloter des machines virtuelles. On lui file un répertoire de configuration pour définir l&rsquo;environnement à installer sur une machine virtuelle. [PuPHPet]() est une appli web qui permet de construire sa configuration pour Vagrant via une IHM, ce qui évite de devoir lire la doc. On est forcément plus limité que si on faisait tout soi même, mais dans mon cas (déployer un environnement apache ou nginx avec mysql ou postgresql, suivant l&rsquo;humeur), j&rsquo;ai de bonnes bases pour pouvoir faire ce qui m&rsquo;intéresse sans m&#8217;embêter.

## De l&rsquo;intérêt de Vagrant

En fait, mon cas d&rsquo;utilisation (déployer des VM kamikaze) est loin d&rsquo;être le plus intéressant. Là où Vagrant prend tout son sens, c&rsquo;est lorsqu&rsquo;on travaille en équipe, et que l&rsquo;on a le besoin de pouvoir avoir finalement de nouvelles machines identiques. Par exemple, lorsqu&rsquo;un nouvel arrivant doit installer sa machine et qu&rsquo;on veut une belle machine toute neuve, sans avoir à copier l&rsquo;ISO de celle d&rsquo;un copain, sans faire d&rsquo;efforts, et sans surprises.  
Et même s&rsquo;il y a une valeur ajoutée à ce qu&rsquo;un nouvel arrivant installe sa machine et comprenne ce qui s&rsquo;y trouve, lorsqu&rsquo;on plante sa bécane, on a pas forcément envie de passer du temps à tout réinstaller. De plus, une installation automatique et scénarisée permet d&rsquo;assurer que tout le monde a le même environnement, ce qui n&rsquo;est pas le cas d&rsquo;un installation manuelle (« j&rsquo;ai pas réussi à faire les choses telles qu&rsquo;elles étaient décrites dans le manuel, donc j&rsquo;ai googlé une alternative »), et qui peut souvent poser problème.

Autre avantage, toute la configuration de la machine à déployer tient en quelque fichiers de configuration. On peut donc la modifier, la versionner, la partager, la livrer&#8230; beaucoup plus facilement qu&rsquo;on le ferait avec un manuel d&rsquo;installation.

## Ok, on a compris, on fait comment ?

**PuPHPet** vous permet de déployer des machines en local, chez DigitalOcean ou Amazon EC2.  
Je vais décrire les étapes par lesquelles je suis passé pour partir de rien, et déployer une machine virtuelle sur Digital Ocean. Avoir un compte chez eux (associé à une carte bancaire) est nécessaire pour aller jusqu&rsquo;au bout, mais la logique est la même si vous voulez déployer ailleurs.

### Configuration de la machine locale

Nous aurons besoin d&rsquo;une clé SSH pour nous authentifier par la suite, créons la.  
<code lang="bash">&lt;br />
cd ~/.ssh&lt;br />
ssh-keygen -t rsa -C "votre@email.com"&lt;br />
</code>

Je l&rsquo;ai appelé digital\_ocean au lieu d&rsquo;id\_rsa.

Il est nécessaire d&rsquo;installer vagrant et virtual box. Vous pouvez récupérez les derniers paquets sur <http://downloads.vagrantup.com/>  
<https://www.virtualbox.org/wiki/Linux_Downloads>

Sur Ubuntu/Debian, on installe les fichiers .deb avec **sudo dpkg -i *.deb**

Il également installer le plugin pour digital ocean :

<code lang="bash">&lt;br />
vagrant plugin install vagrant-digitalocean&lt;br />
vagrant box add dummy https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box&lt;br />
</code>

## Créer un projet

<code lang="bash">&lt;br />
mkdir vagrant_env&lt;br />
</code>

C&rsquo;est dans ce répertoire que nous mettrons le code de configuration utilisé par vagrant. En général, on fait un **vagrant init** pour démarrer un nouveau fichier de configuration, mais nous allons utiliser PuPHPet qui va faire ça pour nous.

### Configurer digital ocean

Enregistrez la clé SSH que vous avez créé : <https://cloud.digitalocean.com/ssh_keys>

Il faut ensuite récupérer votre identifiant utilisateur et votre clé API : [https://cloud.digitalocean.com/generate\_api\_key](https://cloud.digitalocean.com/generate_api_key)

Notez la clé API quelquepart, car elle n est plus affichée quand on revient sur la page et le seul moyen d&rsquo;en avoir une est de la regénérer.

### Configurez votre machine avec PuPHPet

Je vous laisse configurer votre machine aux petits oignons avec [PuPHPet](https://puphpet.com/). N&rsquo;oubliez pas de renseigner toutes les informations sur la configuration Digitalocean (clés API), nom de la machine, et type de machine.  
Vous pouvez choisir le type de serveur (apache2/nginx), postgresql ou mysql, installer ou non phpmyadmin, la configuration de PHP, les packages divers à installer&#8230; c&rsquo;est très simple.

Une fois terminé, un immense bouton permet de télécharger vos fichiers de configuration. Décompressez les dans un répertoire, vous devriez avoir l&rsquo;arborescence suivante :

<code lang="bash">&lt;br />
.&lt;br />
├── files&lt;br />
│   └── dot&lt;br />
├── hiera.yaml&lt;br />
├── puppet&lt;br />
│   ├── hieradata&lt;br />
│   │   └── common.yaml&lt;br />
│   ├── manifests&lt;br />
│   │   └── default.pp&lt;br />
│   └── Puppetfile&lt;br />
├── shell&lt;br />
│   ├── initial-setup.sh&lt;br />
│   ├── librarian-puppet-vagrant.sh&lt;br />
│   ├── os-detect.sh&lt;br />
│   ├── self-promotion.txt&lt;br />
│   └── update-puppet.sh&lt;br />
└── Vagrantfile&lt;br />
</code>

Dans le fichier puppet/hieradata/common.yaml, vous trouverez toutes les informations que vous avez spécifiées sur comment configurer votre machine. Dans le répertoire files/dot, vous pouvez ajouter un fichier .bashrc, .vimrc&#8230; qui seront déployées lors de l&rsquo;installation de votre machine.

Normalement, on est prêt à déployer sa machine :  
<code lang="bash">&lt;br />
vagrant up&lt;br />
</code>

Ca n&rsquo;a pas marché pour moi (machine sous Ubuntu 12.04), il fallait encore faire quelques légères modifications. La clé ssh n&rsquo;a pas été bien prise en compte lorsque je l&rsquo;ai précisé dans PuPHPet, j&rsquo;ai du modifier  
`<br />
config.ssh.private_key_path = "~/.ssh/digitalocean" dans le fichier VagrantFile<br />
`  
Il a également fallu ajouter dans mon fichier .bashrc  
`<br />
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt<br />
`  
puis dans le fichier VagrantFile, ajouter la ligne  
`<br />
provider.ca_path = "/etc/ssl/certs/ca-certificates.crt"<br />
`  
dans vm.provider

Voici donc un exemple de configuration qu&rsquo;on peut avoir. Vous pouvez voir que c&rsquo;est au final très simple, on dit ce dont on a besoin et comment le configurer, et vagrant se charge de l&rsquo;installer pour nous. Grâce au plugin DigitalOcean, il crée même la machine pour nous.

### Fichier VagrantFile

`<br />
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'digital_ocean'</p>
<p>Vagrant.configure("2") do |config|<br />
  config.ssh.private_key_path = "~/.ssh/digitalocean"<br />
  config.ssh.username = "clem"</p>
<p>  config.vm.box = "dummy"</p>
<p>  config.ssh.private_key_path = "~/.ssh/digitalocean"</p>
<p>  config.vm.hostname = "plop"<br />
  config.vm.provider :digital_ocean do |provider|<br />
    provider.client_id = "id_digital_ocean_que_vous_avez_fourni"<br />
    provider.api_key = "cle_api_digital_ocean_que_vous_avez_fourni"<br />
    provider.image = "Debian 7.0 x64"<br />
    provider.region = "Amsterdam 1"<br />
    provider.size = "512MB"<br />
    provider.ca_path = "/etc/ssl/certs/ca-certificates.crt"<br />
  end</p>
<p>  config.vm.synced_folder "./", "/var/www", id: "webroot"</p>
<p>  config.vm.provision :shell, :path => "shell/initial-setup.sh"<br />
  config.vm.provision :shell, :path => "shell/update-puppet.sh"<br />
  config.vm.provision :shell, :path => "shell/librarian-puppet-vagrant.sh"<br />
  config.vm.provision :puppet do |puppet|<br />
    puppet.facter = {<br />
      "ssh_username" => "clem"<br />
    }</p>
<p>    puppet.manifests_path = "puppet/manifests"<br />
    puppet.options = ["--verbose", "--hiera_config /vagrant/hiera.yaml", "--parser future"]<br />
  end</p>
<p>  config.ssh.shell = "bash -l"</p>
<p>  config.ssh.keep_alive = true<br />
  config.ssh.forward_agent = false<br />
  config.ssh.forward_x11 = false<br />
  config.vagrant.host = :detect<br />
end</p>
<p>`

### Fichier common.yml

`<br />
---<br />
vagrantfile-digital_ocean:<br />
    vm:<br />
        box: digital_ocean<br />
        hostname: nom_de_votre_machine<br />
        network:<br />
            private_network: 192.168.56.101<br />
            forwarded_port: {  }<br />
        provider:<br />
            digital_ocean:<br />
                image: 'Debian 7.0 x64'<br />
                region: 'Amsterdam 1'<br />
                size: 512MB<br />
                client_id: id_digital_ocean_que_vous_avez_fourni<br />
                api_key: cle_api_digital_ocean_que_vous_avez_fourni<br />
        provision:<br />
            puppet:<br />
                manifests_path: puppet/manifests<br />
                options:<br />
                    - --verbose<br />
                    - '--hiera_config /vagrant/hiera.yaml'<br />
                    - '--parser future'<br />
        synced_folder:<br />
            DXt5BtQJjHh3:<br />
                id: webroot<br />
                source: ./<br />
                target: /var/www<br />
    ssh:<br />
        host: null<br />
        port: null<br />
        private_key_path: ~/.ssh/digitalocean<br />
        username: clem<br />
        guest_port: null<br />
        keep_alive: true<br />
        forward_agent: false<br />
        forward_x11: false<br />
        shell: 'bash -l'<br />
    vagrant:<br />
        host: ':detect'<br />
server:<br />
    packages:<br />
        - vim<br />
        - git<br />
    dot_files:<br />
        -<br />
            bash_aliases: null<br />
    _prevent_empty: ''<br />
nginx:<br />
    vhosts:<br />
        1Zbx9ZeVKOfF:<br />
            server_name: awesome.dev<br />
            server_aliases:<br />
                - www.awesome.dev<br />
            www_root: /var/www/awesome.dev<br />
            listen_port: '80'<br />
            index_files:<br />
                - index.html<br />
                - index.htm<br />
                - index.php<br />
            envvars:<br />
                - 'APP_ENV dev'<br />
php:<br />
    version: '55'<br />
    composer: '1'<br />
    modules:<br />
        php:<br />
            - cli<br />
            - intl<br />
            - mcrypt<br />
            - curl<br />
            - common<br />
            - gd<br />
            - fpm<br />
            - memcache<br />
            - memcached<br />
            - xcache<br />
        pear: {  }<br />
        pecl:<br />
            - pecl_http<br />
    ini:<br />
        display_errors: On<br />
        error_reporting: '-1'<br />
        session.save_path: /var/lib/php/session<br />
    timezone: Europe/Paris<br />
xdebug:<br />
    install: 0<br />
    settings:<br />
        xdebug.default_enable: '1'<br />
        xdebug.remote_autostart: '0'<br />
        xdebug.remote_connect_back: '1'<br />
        xdebug.remote_enable: '1'<br />
        xdebug.remote_handler: dbgp<br />
        xdebug.remote_port: '9000'<br />
mysql:<br />
    root_password: votre_mot_de_passe_root_bdd<br />
    phpmyadmin: '1'<br />
    databases:<br />
        T7hssen8Pk2a:<br />
            grant:<br />
                - ALL<br />
            name: clem<br />
            host: localhost<br />
            user: clem<br />
            password: votre_mot_de_passe_bdd<br />
            sql_file: ''<br />
` 

Bref, j&rsquo;ai vraiment été séduit par le rapport effort/résultat. Il m&rsquo;aura fallu environ 1h30 pour générer cette configuration de machine que je peux redéployer à volonté, ce qui est à peine plus que le temps que ça m&rsquo;aurait pris si je l&rsquo;avais fait à la main. Sauf que maintenant, tous les déploiements suivants peuvent se faire via **vagrant up**, et que si je souhaite travailler avec des collègues sur les projets pour lesquels j&rsquo;ai construit cette machine, je peux leur fournir la configuration exacte de la machine à installer.