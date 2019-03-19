---
id: 872
title: 'Starting Rust: where to learn, what to install'
date: 2017-07-28T12:29:33+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=872
permalink: /2017/07/28/starting-rust-where-to-learn-what-to-install/
robotsmeta:
  - index,follow
categories:
  - Rust
---
I had a hard time learning rust at first. I didn&rsquo;t quite know where to start, I focused on the wrong resources and lost some time. Here are my suggestions about everything you may need in order to learn and work with rust: where and what to learn, how to properly install the compiler, what tools you need and how to use them.

<!--more-->

TL;DR:

  * Useful learning resources: 
      * Start learning rust with **[the rust book](https://doc.rust-lang.org/book/second-edition/)**. It will teach you **why** things work like this in rust, which is more important than **how** in this language (but you&rsquo;ll learn that too). It&rsquo;s free, online, and hands on: there are a few practicals apps that you&rsquo;ll build while reading the book (the first is in chapter 2, almost right away).
      * You can share a code sample with your problem on **[rust playground]](https://play.rust-lang.org/)** to [rust-beginners](https://chat.mibbit.com/?server=irc.mozilla.org&channel=%23rust-beginners).
      * Use [Rust by example](http://rustbyexample.com/) in order to **refresh your memory**.
      * Browse [24 days of rust](http://zsiciarz.github.io/24daysofrust/book/vol1/day1.html). You&rsquo;ll see some apps, patterns or crates (rust libraries)&#8230; from the **rust ecosystem**.
      * If you work for the web, [http://www.arewewebyet.org/](Are we web yet) provides info about the current state of the crates for **web development**.

  * Tools you may find useful: 
      * **rustup** allows you to have multiple rust versions on your system. It&rsquo;s handy when some crates require you to use a nightly build of the compiler.
      * **racer** will let you have code completion, and there are various plugins for your IDEs.
      * learn how to use a debugger like [**gdb**](http://www.unknownroad.com/rtfm/gdbtut/gdbtoc.html) or **rust-gdb** in order to debug you code
      * [**rustfmt**](https://github.com/rust-lang-nursery/rustfmt) lets you reformat your code in a standard way
      * **[clippy](https://github.com/rust-lang-nursery/rust-clippy)** is a **linter**. It can help you spot bad code patterns.

## Why sould you learn Rust ? {#why-sould-you-learn-rust-}

That&rsquo;s not the topic of this article 🙂 I&rsquo;ll assume you have a basic understanding of what it&rsquo;s meant for, but are not quite sure where to get started.

## Start with the rust book. Learn the WHYs, not just the HOWs. {#start-with-the-rust-book-learn-the-whys-not-just-the-hows-}

I&rsquo;ve learnt a lot of languages since I started programming, ~15 years ago. I&rsquo;ve had the opportunity to use them both for personnal projects, out of curiosity, or in a professional setting, where the constraints are different. I guess I can consider myself an experienced developer.

Often, when it comes to learning a new language, things are easy: I simply pop a REPL or some sample hello world project, grab some documentation, and start messing around. I wrote a Brainfuck interpreter in Ruby a few hours after I started reading about the language, because the langage is very close to python, which I already knew.

Things in Rust didn&rsquo;t work like that for me.

[Like many](https://stackoverflow.com/questions/29458935/how-can-i-add-strings-and-print-them), I tried to jump at writing code and faced a lot of walls. The compiler gives detailed explanations about where I did mistakes, but sometimes I didn&rsquo;t understand what was wrong.

When learning rust, you don&rsquo;t simply need to learn **how to do things**. You need to understand **why you do them** like this. And it will question a lot of your bad habits as a developer. Like using mutable variables when you don&rsquo;t need to (it&rsquo;s way more tricky than it sounds), extensively checking for errors (you really have no idea how terrible you are. Yes it&rsquo;s hard, yes it&rsquo;s not fun, but if you won&rsquo;t to be in real control of what&rsquo;s happening, yes, you should deal with all the errors your code may throw !), dealing with return values (not using one throws a warning in rust).

Rust enforces the [**principle of least privilege**](https://en.wikipedia.org/wiki/Principle_of_least_privilege), and you&rsquo;ll most likely notice (via trial and error) that it&rsquo;s not something you&rsquo;re used to. And that you don&rsquo;t do it as much as you think you do. It&rsquo;s pretty frustrating to feel like the code you usually write is bloated with mistakes, but this deeper understanding about how code should behave will help you and you code grow.

## Then, go further {#then-go-further}

Once you understand why things work the way they do in Rust, it&rsquo;s time to broaden your horizons.

  * [Rust by example](http://rustbyexample.com/) contains a lot of example, in order to quickly refresh my memory or to get started using a particular component.
  * [24 days of rust](http://zsiciarz.github.io/24daysofrust/book/vol1/day1.html) will make you discover apps, patterns or crates (rust libraries)&#8230; from the rust ecosystem.
  * If you work for the web, [http://www.arewewebyet.org/](Are we web yet) provides info about the current state of the crates you may need for web development.

Browsing through the code of popular crates will also help you understand some idiomatic code patterns. Plenty of them are on Github.

## Asking for help {#asking-for-help}

These resources cover a lot of ground but you may need help in order to understand some things. The [Rust Playground](https://play.rust-lang.org/?gist=7a0a0e0b102a9bf0b494d21b9729babb&version=stable&backtrace=0) will let you share and execute a code sample, so that&rsquo;s easier for someone else to understand and debug or fix the piece of code you&rsquo;re stuck with.

You can ask for help on stackoverflow, or [Reddit](https://www.reddit.com/r/rust/) but there is also the [rust-beginners](https://chat.mibbit.com/?server=irc.mozilla.org&channel=%23rust-beginners) IRC channel on irc.mozilla.org. A lot of friendly people there.

# Setting up a complete working environment {#setting-up-a-complete-working-environment}

A small overview about how to properly install rust and some dependencies that can be useful.

## Installing rust with rustup {#installing-rust-with-rustup}

Contrarilly to many tools, you don&rsquo;t install the rust compiler right away when you get started with rust: instead, you first install rustup, a rust compiler version manager. That&rsquo;ll allow you to install multiple versions of rust, and switch between them at will. Some libraries, like [clippy](https://github.com/rust-lang-nursery/rust-clippy) (it&rsquo;s a rust linter) expect you to use the nightly build, while most of the time, you may want to use the latest stable release, so you may need to be able to switch between language versions.

Once you have installed rustup, you can install a new build of the language. For instance, here I install the latest nightly build:

<div class="line">
  <span class="syntax--source syntax--shell">$ rustup install nightly</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">&#8230; installing info</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">$ rustup show</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">Default host: x86_64-unknown-linux-gnu</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell"> </span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">installed toolchains</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell"> </span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">stable-x86_64-unknown-linux-gnu <span class="syntax--meta syntax--scope syntax--subshell syntax--shell"><span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">(</span>default<span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">)</span></span></span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">nightly-x86_64-unknown-linux-gnu</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell"> </span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">active toolchain</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">&#8212;&#8212;&#8212;&#8212;&#8212;-</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell"> </span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">stable-x86_64-unknown-linux-gnu <span class="syntax--meta syntax--scope syntax--subshell syntax--shell"><span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">(</span>default<span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">)</span></span></span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">rustc 1.18.0 <span class="syntax--meta syntax--scope syntax--subshell syntax--shell"><span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">(</span>03fc9d622 2017-06-06<span class="syntax--punctuation syntax--definition syntax--subshell syntax--shell">)</span></span></span>
</div>

<pre class="editor-colors lang-bash"></pre>

You can see that I have two build toolchains setup: the _stable_ and the _nightly_. The active one is the _stable_. So without more details, cargo run will execute thing with the active toolchain, but I can change it:

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo run <span class="syntax--comment syntax--line syntax--number-sign syntax--shell"><span class="syntax--punctuation syntax--definition syntax--comment syntax--shell">#</span> runs the project with the active toolchain</span></span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo +nightly run <span class="syntax--comment syntax--line syntax--number-sign syntax--shell"><span class="syntax--punctuation syntax--definition syntax--comment syntax--shell">#</span> runs the project with the nightly</span></span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">$ rustup default nightly <span class="syntax--comment syntax--line syntax--number-sign syntax--shell"><span class="syntax--punctuation syntax--definition syntax--comment syntax--shell">#</span> setups the nightly as active</span></span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo run <span class="syntax--comment syntax--line syntax--number-sign syntax--shell"><span class="syntax--punctuation syntax--definition syntax--comment syntax--shell">#</span> now my project will be run using the nightly build</span></span>
</div>

<pre class="editor-colors lang-bash"></pre>

## Understand the existing tools {#understand-the-existing-tools}

### cargo {#cargo}

cargo is rust&rsquo;s package manager. You&rsquo;ll use cargo for a lot of things (on the rust book, for instance). Among other things, it can:

  * scaffold a new project: 
      * library: cargo new some_project
      * binary: cargo new some_project &#8211;bin
  * build your project ($ cargo build)
  * run the project ($ cargo run)
  * install a dependency: cargo install some\_project\_or_library
  * run the unit tests: $ cargo test (the examples in the documentation can also be [considered as unit tests!](https://doc.rust-lang.org/1.5.0/book/documentation.html#running-documentation-tests) )
  * build and open the project&rsquo;s documentation (it includes the doc for the dependencies): cargo doc &#8211;open

Thanks to cargo, you can easily get started with continuous integration of a platform like **Travis-CI**. For instance, you may want to run the tests every time a commit is pushed on a branch on github, in order to see if said branch breaks the project.

Travis-CI&rsquo;s got [some explanations](https://docs.travis-ci.com/user/languages/rust/) regarding how to do that.

### Debugging gdb, rust-gdb {#debugging-gdb-rust-gdb}

In a complex project, you may need a debugger in order to understand why things do not work the way you thought they were (no, printing stuff to the console is NOT a good habit).

You can use gdb (or better, rust-gdb, in provides more context). Instead of running your project with

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo run</span>
</div>

<pre class="editor-colors lang-bash"></pre>

you&rsquo;ll do

<div class="line">
  <span class="syntax--source syntax--shell">$ gdb target/debug/name_of_you_executable</span>
</div>

<pre class="editor-colors lang-bash"></pre>

or

<div class="line">
  <span class="syntax--source syntax--shell">$ rust-gdb target/debug/name_of_you_executable</span>
</div>

<pre class="editor-colors lang-bash"></pre>

Then, the application will run inside the debugger and you see what is happening. Here are some more info about [getting started](http://thornydev.blogspot.fr/2014/01/debugging-rust-with-gdb.html), and here is an useful [list of how to&rsquo;s)](http://www.unknownroad.com/rtfm/gdbtut/gdbtoc.html) to get you started with gdb.

## Installing some more things {#installing-some-more-things}

Out of the box, some things are missing: I&rsquo;ll give you detail about how to properly and automatically format your code, how to lint and setup code completion.

### Formatting the code with rustfmt {#formatting-the-code-with-rustfmt}

There is not rust fmt like there is in Go. I think go fmt is fantastic, because it puts code style of out the equation. I find the talks about code style useless and boring, and I&rsquo;ve found go fmt to be an amazing way to get that out of the way: in Go, the code style is part of the language.

There is no such thing in rust, but there is [rustfmt](https://github.com/rust-lang-nursery/rustfmt). It&rsquo;s a tool that enforces a given code style.

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo install rustfmt</span>
</div>

<pre class="editor-colors lang-bash"></pre>

The you can reformat a source file or directory:

<div class="line">
  <span class="syntax--text syntax--plain"><span class="syntax--meta syntax--paragraph syntax--text">$ cargo fmt src</span></span>
</div>

<pre class="editor-colors lang-text"></pre>

### Code completion with racer (with rustup for atom) {#code-completion-with-racer-with-rustup-for-atom-}

[racer](https://github.com/racer-rust/racer) is a code completion tool. It&rsquo;s super useful if you don&rsquo;t want to have to browse the documentation every other second.

It relies on the rust source code to provide this information, so we need to download it before installing racer:

<div class="line">
  <span class="syntax--source syntax--shell">$ rustup component add rust-src</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">$ cargo install racer</span>
</div>

<pre class="editor-colors lang-bash"></pre>

Then, you&rsquo;ll need to setup racer in your IDE. I use atom, and there is an [atom-racer](https://github.com/edubkendo/atom-racer) package.

If you use rustup, you&rsquo;ll need to provide 2 information in the settings of the rust-atom package:

  * the location of the rustc binary

<div class="line">
  <span class="syntax--source syntax--shell">$ which rustc</span>
</div>

<div class="line">
  <span class="syntax--source syntax--shell">/home/clemk/.cargo/bin/rustc</span>
</div>

<pre class="editor-colors lang-bash"></pre>

  * the location of the rust source code

<div class="line">
  <span class="syntax--source syntax--shell"><span class="syntax--string syntax--interpolated syntax--dollar syntax--shell"><span class="syntax--punctuation syntax--definition syntax--string syntax--begin syntax--shell">$(</span>rustc &#8211;print sysroot<span class="syntax--punctuation syntax--definition syntax--string syntax--end syntax--shell">)</span></span>/lib/rustlib/src/rust/src/</span>
</div>

<pre class="editor-colors lang-bash"></pre>

I&rsquo;ve also had an issue with flickering in Atom, because of the frequent creation of a temporary file. I solved it [thanks to this page](https://github.com/edubkendo/atom-racer/issues/31). Doesn&rsquo;t sound solid, but that&rsquo;s OK for now.

Yeah, I know. There&rsquo;s a kind of irony in working with a crazy quick language in a javascript-powered electron app, but hey, nobody&rsquo;s perfect.

# Conclusion {#conclusion}

That&rsquo;s it ! I hope this article gave you some ideas about where to get started learning rust, and what are the tools you may need. It&rsquo;s a long road, but the landscape is worth it.