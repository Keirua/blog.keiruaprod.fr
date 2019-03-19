---
id: 726
title:
  - Basic docker usage for a PaaS activity
date: 2014-06-17T22:18:24+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=726
permalink: /2014/06/17/basic-docker-usage-for-a-paas-activity/
description:
  - 'An introduction to docker through the basic setup of a PaaS for executing  sandboxed php.'
robotsmeta:
  - index,follow
categories:
  - Astuce
---
I wrote this article a while ago. Instead of letting it sink on my hard drive, the [release of docker 1.0](http://blog.docker.com/2014/06/its-here-docker-1-0/ "Docker 1.0 release") is a good opportunity to let people know how easy getting started is. There might be some better solutions for many things, since stuff have evolved a lot in the last months, but you can see this article as an introduction to what docker is and how it works.

A few months ago, I talked about how to use Vagrant in order to deploy virtual machines on DigitalOcean. More recently, I&rsquo;ve been playing with [Docker](https://www.docker.io/ "Docker"), which is a kind of git for virtual machines.

With this tool, one can create virtual machines. The philosophy is not to ease machine creation (stuff that you would find with Vagrant + Puppet or Chef). The magic idea is that after every modification on the system (setup, file creation, script execution&#8230;), it is possible to save the state of the machine. This is so similar to &lsquo;git commit&rsquo; that the command is&#8230; &lsquo;docker commit&rsquo;.  
With such a philosophy, it is possible to navigate between the states, publish a machine like you would publish a repository on github, update a set of already-running machines efficiently, and so on.

I&rsquo;ll get through the first steps to create a small machine that can be used in order to execute sandboxed php code : the php code will run inside the machine, and we&rsquo;ll get the result. This could be used for a PaaS (Platform as a Service), like jsbin or codepen, but for languages whose functionnalities could pose security threats if it was executed on the main machine (php, python, ruby&#8230;).

## Installing docker

I won&rsquo;t get much into the details about how to install docker actually, everything you need is up to date in the <a href= »http://docs.docker.io/en/latest/ »>documentation</a>. There are some requirements about the version of your kernel, so if you can&rsquo;t install, a solution is to run it inside a vagrant virtual machine. The source code contains a Vagrantfile already setup, so nothing could be easier :



Now that we have our new toy, we can start creating an image.

Open a terminal and start an instance using the base image :

<code lang="bash">&lt;br />
sudo docker run -i -t base /bin/bash&lt;br />
</code>

This will launch you into a shell inside the machine. We can now start customizing the image. We won&rsquo;t do much in this tutorial, we will simply install php, but of course you can do everything you would do with any virtual machine.

## Installing php

Inside the shell, run :

<code lang="bash">&lt;br />
apt-get update&lt;br />
apt-get install php5&lt;br />
</code>

## Saving of a machine

Now that we have a machine with PHP installed, we want to save it, in order to be able to reuse it afterwards. We have made modifications on the system but if we exit the shell right now, since they have not been saved, we&rsquo;ll have to install php again the next time we run our image.

Leave the current terminal open, and open another terminal. In order to save our image we need its identifier, so run :

 <code lang="bash">sudo docker ps&lt;br />
</code>

It will show the ID of the running container in the other terminal. We can save our image with the name &lsquo;clem/php&rsquo; by running the commit command :

<code lang="bash">&lt;br />
sudo docker commit clem/php&lt;br />
</code>

The name looks like the conventions on github (user/repository). Even though here there are no obligations, it&rsquo;s good to keep good habits.

If all went well, your images &lsquo;clem/php&rsquo; will appear in the list of available images :

<code lang="bash">&lt;br />
sudo docker images&lt;br />
</code>

Images are similar to git branches of the base image. The next time you want to create a machine, if you want to install php and mysql, you can :

  * run the base image, install php and mysql
  * run the clem/php, and install mysql

## Our basic jsbin like for PHP

Remember, we want to do something similar to jsbin, but for executing php in a sandbox. Our image clem/php will be the sandbox, because we don&rsquo;t want to restrict the functionnalities of the language, what if someone executed some shell code from PHP in order to erase the whole system. We can use docker to start a machine, execute any phpcode, return us the result, and quit. Since we won&rsquo;t save the machine, every execution will provide us with a brand new machine. If someone destroys it in anyway, we couldn&rsquo;t care less.

We need to create a file on the host, that will be executed in docker. Create test.php, and write something like :

<code lang="php">&lt;br />
<?php echo 'Hello World !'.PHP_EOL;
</code>&lt;br />
Run some code inside your new sandbox&lt;br />
The first idea I came up with was this one :&lt;/p>
&lt;p>&lt;code lang="bash">&lt;br />
cat test.php | sudo docker run -i clem/php /bin/bash -c "cat &gt; test.php; php test.php"&lt;br />
</code>

Basically, to manually copy the content of the file thanks to cat inside docker. Then we run it thanks to bash, with a 2 command script : "cat > test.php; php test.php", or 'dump the content to test.php then run test.php'.

There is a better solution : using a mounting point. We can share a folder on the host machine to docker.  
/home/vagrant/test.php will be the file on the host machine  
/home/docker.php is the file we want to have on the docker machine.  
the '-v' option tells docker to create a mounting point between the two files.  
This time, instead of running bash, we can directly run PHP.

<code lang="bash">&lt;br />
docker run -v /home/vagrant/test.php:/home/docker.php php /home/docker.php&lt;br />
</code>  
Awesome, huh ?