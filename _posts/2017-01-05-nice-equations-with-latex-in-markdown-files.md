---
id: 854
title: Nice equations with LaTeX in Markdown files
date: 2017-01-05T08:48:20+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=854
permalink: /2017/01/05/nice-equations-with-latex-in-markdown-files/
robotsmeta:
  - index,follow
categories:
  - Astuce
lang: en
archived: true
---
I&rsquo;m using [Markdown](http://daringfireball.net/projects/markdown/) as a markup syntax for many things: the syntax is indeed really simple to use, it lets me focus on the content I need to write, and it can later be converted to HTML for « real life » display once I&rsquo;m done. In the open-source community, it has become largely spread, and many developpers use it, like me, for non code-related stuff, like keeping notes or writing their journal. <!--more-->

Until recently, I&rsquo;ve been using **[Markdown Preview](https://github.com/revolunet/sublimetext-markdown-previewarticle.md)**. It&rsquo;s a sublime-text plugin for previewing the HTML transformation a markdown file. It works well, but it has a few issues for me. The first is that it uses Github as a backend for HTML conversion. When working for a long time on a file, I often reach the max amount of allowed calls to the webservice for the conversions, then conversions are not possible for a while, which is quite annoying.

The second problem is that, recently, I&rsquo;ve become interested in writing math things. LaTeX comes immediately to the mind, as the language invented by Donald Knuth in the beginning of the 80x is the _de facto_ standard for writing equations in the academic world. But it is not possible to have LaTeX properly converted when it is in the middle of a markdown file using Github flavoured markdown. There are [ways to cheat this](http://stackoverflow.com/questions/35498525/latex-rendering-in-readme-md-on-github) though, but it is not easy and it is not compatible as-is with Markdown Preview.

We will take a different route.

## The problem {#the-problem}

The use-case is the following : **I want to write my markdown files in sublime-text. They can contain LaTeX content, and I want to be able to generate an HTML output with the proper transformations applied**. How to do that ? Can it be simple ? The answer is yes, let&rsquo;s see how.

Let&rsquo;s start with a sample markdown file that contains some LaTeX:

    # Some Markdown
    
    Here is a list:
    
     - a
     - b
    
    # Some $\LaTeX$
    
    The Fibonnacci's sequence is defined as follow:
    
    $$
    \begin{aligned}
    u_0&=0 \\
    u_1&=1 \\
    u_n&=u_{n-1}+u_{n-2} \forall n \in \Bbb{N}, n \geq 2
    \end{aligned}
    $$
    
    The golden ratio $\phi$ equals to $\frac{1+\sqrt{5}}{2}$

I want it to be displayed like this :

[<img class="size-medium wp-image-859 aligncenter" src="http://blog.keiruaprod.fr/wp-content/uploads/2017/01/output-mdtex-300x300.png" alt="" width="300" height="300" srcset="http://blog.keiruaprod.fr/wp-content/uploads/2017/01/output-mdtex-300x300.png 300w, http://blog.keiruaprod.fr/wp-content/uploads/2017/01/output-mdtex-150x150.png 150w, http://blog.keiruaprod.fr/wp-content/uploads/2017/01/output-mdtex.png 401w" sizes="(max-width: 300px) 100vw, 300px" />](http://blog.keiruaprod.fr/wp-content/uploads/2017/01/output-mdtex.png)

## A bash script to the rescue {#a-bash-script-to-the-rescue}

**[Pandoc](http://pandoc.org/)** is a swiss knife for conversion between markup formats. It works well for markdown to html, but can calso convert LaTeX to HTML. The latest release can be downloaded [here](https://github.com/jgm/pandoc/releases/),w e will use it later.

The thing is that pandoc either converts markdown to html or latex to html, but not both at the same time. However, we can cheat: the trick is to convert from markdown to html, and include the JavaScript **[MathJax library](https://www.mathjax.org/)** in the HTML output. That way, the LaTeX is not transformed during the markdown to HTML conversion, but it is transformed at runtime, in the browser.

Let&rsquo;s write a script mdtex2html.sh :

    #!/bin/sh
    pandoc $1 -t html -s -o "${1%.*}".html --mathjax=https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML

The syntax « ${1%.*} ».html means « remove the extension then add .html ». So the script creates a file.html out of the pandoc markdown conversion of a file.something. In this HTML file, the javascript library MathJax is included

Once it has the proper execution rights ($ chmod +x mdtex2html.sh), it can be used to convert a file with any extension

    $ ./mdtex2html.sh sample.mdtex

Thanks to that, we can have the expected output.

We could decide that we are done here, but every time we want to convert the markdown file, we have to execute the script from the command line. We can do better 🙂 We can create a custom sublime-text build.

## Making it better with a build script {#making-it-better-with-a-build-script}

First, let&rsquo;s move our shell script to a path-aware directory :

    $ sudo cp mdtex2html.sh /usr/bin

Now we can invoke mdtex2html.sh from anywhere :

    $ mdtex2html.sh sample.mdtex

Then, we&rsquo;ll create a build for our markdown files. The **.mdtex** extension is arbitrary, but it will be useful now : Tools -> Build system -> New build system. Immediately save the build file as **mdtex.sublime-build**:

    {
        "cmd": ["mdtex2html.sh", "${file_path}/${file_name}"]
    }

The build calls mdtex2html.sh and provide the current file name as an argument.

Now, every time we run a build (with **Ctrl+B**) from our .mdtex files, it will be compiled into HTML.

## Even better with live reload {#even-better-with-live-reload}

So. Now, every time we hit **Ctrl+B**, files with a **.mdtex** extension are converted into HTML. We then have to refresh the page in the browser in order to see the changes. It needs to open the tab, hit F5, and wait for the rendering to be over.

We can do better, and skip the F5 update with the proper tool. One solution is to use system tools like _inotify_ (or variants like _pynotify_, in python) to watch the changes on the HTML file. There is a detailled setup [here](http://sakthipriyan.com/2016/02/15/auto-refresh-chrome-when-files-modified.html): it works well for complex solutions, like a jekyll blog that involve a lot of files.

There however are various browser extensions, like [Auto-reload](https://addons.mozilla.org/fr/firefox/addon/auto-reload/) for Firefox, that watch file and reload the page when they change. Once it is setup, you can work from sublime text, save with Ctrl+S, build with Ctrl+B, and the latest built version will be updated in the browser.

It is also possible to trigger the build on save with the [Build on save](https://github.com/alexnj/SublimeOnSaveBuild) extension, but I did not do that.