---
id: 881
title:
  - An intro to rust
date: 2018-02-19T12:46:40+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=881
permalink: /2018/02/19/an-intro-to-rust/
robotsmeta:
  - index,follow
categories:
  - Rust
lang: en
---
I recently gave an introductory talk about the [Rust language](https://www.rust-lang.org), to experienced programmers who did not know the language. The presentation can be seen [here](http://htmlpreview.github.io/?https://github.com/Keirua/rust-intro/blob/master/index.html) and downloaded [on Github](https://github.com/Keirua/rust-intro/). This article is a short summary of what I described.

The idea was not to enumerate features, but to highlight some of the cool things that have made this language so popular and growing quickly with a lot of enthusiasm.

I chose to focus on the 4 following elements:

  * Tools
  * Borrow checker
  * Community
  * Integrations with other languages

There are more of course, but hey, attention and time are limited resources, tech talk are no exception.<!--more-->

# <a class="headeranchor-link" href="#tools" name="user-content-tools" aria-hidden="true"></a>Tools {#tools}

TL;DR:

3 cools things:  
&#8211; cargo. It does a lot of things, and do it well and simply  
&#8211; the rust compiler. It’ll teach you how to program.  
&#8211; nice integration with the existing IDEs.

The cool thing with Rust is that the tools work well, and they work well together. One of the angular stone of this tools is **cargo**. According to [the cargo book](https://doc.rust-lang.org/cargo/):

    Cargo is the Rust package manager. Cargo downloads your Rust project’s dependencies, compiles your project, makes packages, and upload them to crates.io, the Rust community’s package registry.
    

It’s a CLI utility that comes with a few commands, for instance:

    new         Create a new cargo project
      doc         Build this project's and its dependencies' documentation
      run         Build and execute src/main.rs
      test        Run the tests
      build       Compile the current project
    

It can bootstrap a project, run an application or the unit tests, or build the final .

    $ cargo new demo-rust --bin
      # this will bootstrap a project with this folder hierarchy:
      demo-rust
      ├── Cargo.toml
      ├── .git
      │   ├── config
      │   ├── description
      │   ...
      ├── .gitignore
      └── src
          └── main.rs
      # build and run in debug
      $ cargo run
         Compiling demo-rust v0.1.0 (file:///home/clem/dev/demo-rust)
          Finished dev [unoptimized + debuginfo] target(s) in 0.48 secs
           Running `target/debug/demo-rust`
      Hello, world!
    

One of the cool things with all these commands is that everyhting is embedded in one tool, with clever default settings; also, cargo can be extended, and new commands can be added. [rustfmt](https://github.com/rust-lang-nursery/rustfmt), for instance, can add a new command for uniformizing the code style.

I’ll talk again about cargo in the “community” section, regarding the dependency management.

Next, the compiler is your best friend. There’s this saying that, if your rust program compiles, it will work. Let’s take an example in C++:

    #include <iostream>;
      int main(){
          unsigned int a = 2;
          a -= 5.3;
          std::cout << a << std::endl;
      }
    

What will it print ? But more importantly, what should it print ? Do we want to add an unsigned int with a float ? what type should be the result value, an int or a float ? Should we accept negative values ?  
A c++ compiler won’t complain, and execute “incorrectly”:

    $ g++ main.cpp -o cpp -Wall -ansi -pedantic
      $ ./cpp
      4294967293
    

Actually, it does exactly as we asked: the substraction lead to an underflow, and we reached the result we asked. But it’s not what we wanted.

The same rust program will complain a couple times:

    fn main() {
          let a:u32 = 3;
          a -= 5.3;
          println!("{}", a);
      }
    

First, because we add incompatible types:

    error[E0308]: mismatched types
       --> src/main.rs:3:10
        |
      3 |     a -= 5.3;
        |          ^^^ expected u32, found floating-point variable
    

Let’s imagine we want **a** to be a float, and fix our program:

    fn main() {
          let a:f32 = 3.0;
          a -= 5.3;
          println!("{}", a);
      }
    

Now, we get an error because we did not explicitly said we want **a** to be mutable. So when we try to modify it, it raises an error.

    error[E0384]: re-assignment of immutable variable `a`
       --> src/main.rs:3:5
        |
      2 |     let a:f32 = 3.0;
        |         - first assignment to `a`
      3 |     a -= 5.3;
        |     ^^^^^^^^ re-assignment of immutable variable
    

and so on.

The idea is that there is no implicit in Rust; well, there is, but as little as possible. The compiler can (and will) infer things based on what is writen so that the code is not too verbose, but most of the time you’ll have to be clear about your intent.

The goal for this is to make sure that the program will execute what is intented, and for that intentions need to properly be specified.

Another cool thing regarding the tools is that Rust works well with the existing IDEs. You can see on [AreWeIDEYet](https://areweideyet.com/) which tools to install in order to customize your development experience, and have an integrated debugger, code completion, compilation errors next to the code, etc.

# <a class="headeranchor-link" href="#the-borrow-checker" name="user-content-the-borrow-checker" aria-hidden="true"></a>The borrow checker {#the-borrow-checker}

The borrow checker is one of the major ideas that Rust brings. Let’s take an example, imagine we have the following piece of code :

<pre><code class="rust">let matches = search(query, &contents);
  println!("Matches for \"{}\":\n", query);
  for current_match in matches {
      println!("{}", current_match);
  }
</code></pre>

It would search for the list of lines that contains the words inside `query` in the text `contents`.

Now, what would happend if, right after the search, we were (for the sake of the example) to modify the text ?

<pre><code class="rust">let matches = search(query, &contents);
  println!("Matches for \"{}\":\n", query);
  for current_match in matches {
      println!("{}", current_match);
  }
  // What if...
  contents += "plop";
</code></pre>

In most languages, it would be fine. You searched for a string inside the text, you’ve got matches, then you modify the text. Ok, whatever. Not in rust, if you take advantage of its power. With an implementation of `search` that uses references, you’ll get an error:

<pre><code class="bash">error[E0502]: cannot borrow `contents` as mutable because
  it is also borrowed as immutable
    --&gt; src/main.rs:38:5
     |
  34 |  let matches = search(query, &contents);
     |                               -------- immutable borrow
                                              occurs here
  ...
  38 |  contents += "plop";
     |  ^^^^^^^^ mutable borrow occurs here
  39 | }
     | - immutable borrow ends here
</code></pre>

**This is awesome**. This error says that we cannot modify `contents`, because some other data are linked to it: that’s the case because the content of matches is directly linked to the content of `contents`, memory-wise. They point to the same data. So you can’t modify the content like this.

This feature of the langage takes a bit of error to get accustomed to, but it eliminates whole classes of bugs.

# <a class="headeranchor-link" href="#the-community" name="user-content-the-community" aria-hidden="true"></a>The community {#the-community}

The community is really active; Rust community has a strong open-source culture, so a lot of things happen in the open. There’s been a call for writing blogpost about improvement requests for 2018 (look for #Rust2018). Before that there was a implementation frenzy. A lot of things are published everyday in [Rust’s subreddit](https://www.reddit.com/r/rust/). There is also a weekly newsletter, [“This Week In Rust”](http://this-week-in-rust.org/). It contains news about the language and community, as well as contribution requests for various kind of developpers.

Also, a [lot of meetups](https://www.meetup.com/topics/rust/all/) take place every months everywhere.

Many libraries (they are called crates in Rust’s lingo) can be found and used very easily thanks to [crates.io](http://crates.io/). A cool trivia is that crates.io is written in Rust. If you want to find crates for web development, take a look on [AreWeWebyet](http://arewewebyet.org/).

Using an external crate is very easy: you simply have to add a dependency to your Cargo.toml metadata file. Here, I added [clap](https://crates.io/clap), for command line argument parsing:

    # Cargo.toml
      [package]
      name = "demo-rust"
      version = "0.1.0"
      authors = ["clement camin &lt;clement@keiruaprod.fr&gt;"]
      [dependencies]
      clap="2.29.1"
    

Then, you can update your program in order to use the new dependency:

    extern crate clap;
      use clap::{App, Arg};
      // ...
      fn main() {
          let parameters = App::new("rust-demo")
                              .version("1.0")
                              .about("Search for strings in file")
                              .arg(Arg::with_name("pattern")
                                  .help("The string we are looking for")
                                  .index(1)
                                  .required(true))
                              .arg(Arg::with_name("file")
                                  .help("The file we want to open")
                                  .index(2)
                                  .required(true))
                              .get_matches();
          let filename = parameters.value_of("file").unwrap();
          let query = parameters.value_of("pattern").unwrap();
          // etc.
    

In the subsequent code execution, cargo will update the dependencies for you, and run the program when it succeeds.

    $ cargo build --release
         Compiling libc v0.2.35
         Compiling bitflags v1.0.1
         ...
         Compiling atty v0.2.6
         Compiling clap v2.29.1
         Compiling demo-rust v0.1.0 (file:///home/clem/dev/rust-intro/code)
          Finished release [optimized] target(s) in 30.13 secs
    

It may not be impressive if you come from a nodeJS, python, ruby or PHP background for instance. They have their own dependency managers that does this kind of thing more or less similarly. But think of it from a C++ perspective, where people use to work with CMake in order to deal with external libraries. It always took an afternoon to get the configuration right, and half the time things did not work because of incorrect library version that you had to fix by hand.

# <a class="headeranchor-link" href="#integrations-with-other-languages" name="user-content-integrations-with-other-languages" aria-hidden="true"></a>Integrations with other languages {#integrations-with-other-languages}

Rust works well with other languages, thanks to what is called FFI, Fluent Foreign Interfaces. You can write Rust code and execute it in C, C++, python, Ruby, or the other way around. Let’s take an example where you will export a Rust function and use it in a C program. You start by saying you’ll build a dynamic library:

    [dependencies]
      libc = "*"
      [lib]
      crate-type = ["cdylib"]
    

Then you write your function:

    extern crate libc;
      use libc::uint32_t;
      #[no_mangle]
      pub extern fn rs_add(a: uint32_t, b: uint32_t) -> uint32_t {
          a + b
      }
    

Once it’s build, you can refer to it in a C program.

    #include <stdio.h>
      #include <stdint.h>
      extern uint32_t rs_add(uint32_t, uint32_t);
      int main(void) {
        uint32_t sum = rs_add(1, 2);
        printf("%d\n", sum);
        return 0;
      }
    

Of course, it can deal with more complex arguments (strings, objects), but the basic idea is there (more examples on [Rust FFI Omnibus](http://jakegoulding.com/rust-ffi-omnibus))

Another cool things is that since december, there is a webassembly build target in Rust compiler. It means it’s very easy to build a Rust program that compiles to webassembly, and that can be used with a javascript application. [Rust-roguelike](https://github.com/richardanaya/rust-roguelike) is an example of bidirectionnal javascript <-> Rust communication, where you can easily see how to do that.

This rust build target is also already used in a mozilla component for [source maps](https://hacks.mozilla.org/2018/01/oxidizing-source-maps-with-rust-and-webassembly/), that you have maybe used without knowing !

# <a class="headeranchor-link" href="#final-notes" name="user-content-final-notes" aria-hidden="true"></a>Final notes {#final-notes}

There are many topics I didn’t talk about, like:

  * generics
  * traits
  * functional programming
  * unsafe
  * macros
  * concurrency

but I’ll leave that as an exercise to the reader 😉 We have already covered a few amazing things around the language that already make it really great.

If you want to learn Rust, the best resource is [The Rust Book](https://doc.rust-lang.org/book/). There is also <RustByExample.com> that will show you useful code snippets, and the [official youtube channel](https://www.youtube.com/channel/UCaYhcUwRBNscFNUKTjgPFiA/videos). Don’t forget to properly setup you IDE thanks to [AreWeIDEYet](https://areweideyet.com/) !