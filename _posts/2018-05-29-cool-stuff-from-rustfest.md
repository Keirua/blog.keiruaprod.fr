---
id: 887
title: Cool stuff from Rustfest
date: 2018-05-29T14:51:06+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=887
permalink: /2018/05/29/cool-stuff-from-rustfest/
robotsmeta:
  - index,follow
categories:
  - Rust
---
I was at [Rustfest](http://paris.rustfest.eu/) this weekend. As expected, it was a great conference ! Lots of things to learn, and great people to meet.

I could not attend the workshops (nor the [Impl days](https://paris.rustfest.eu/about_impl_days/)), but this cool community puts so many things on Github that I&rsquo;m gonna be able to do them anyway, see for instance:

  * [the workshop on libp2p](https://github.com/tomaka/rustfest-2018-workshop)
  * <a href="http://troubles.md/posts/rustfest-2018-workshop/" rel="nofollow">the workshop on performances</a>

Also, the videos are on <a href="https://media.ccc.de/c/rustfest18" rel="nofollow">the web already</a>, and you can download lrlna&rsquo;s [zine about memory](https://github.com/lrlna/sketchin/blob/master/zines/data-ownership.md) 

What follows is a summary of the talks I liked the most.

Tech:

  * [Yew, Javascript without javascript 😉](#yew)
  * [Immutable data structures](#immutable)
  * [Building reliable infrastructures](#infrastructure)

Non-tech:

  * [Learning How To Learn](#learn)
  * [Rust Communities](#communities)

# <a id="yew" class="anchor" href="#yew-javascript-without-javascript" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Yew, JavaScript without JavaScript

Denis Kolodin talked about [Yew](https://github.com/DenisKolodin/yew/), the rust framework he develops.

As a web developper, this is really exciting : we can have both the power and safety of Rust, with the reach of web applications ! Yew looks a lot like doing React development with Redux.

Let&rsquo;s take an example : imagine we want to create a counter, with 2 buttons to increment/decrement the value. We would:

  1. Create a model

    pub struct Model {
        value: i64,
    }
    

<ol start="2">
  <li>
    Create the messages
  </li>
</ol>

    pub enum Msg {
        Increment,
        Decrement
    }
    

<ol start="3">
  <li>
    Implement the message handling
  </li>
</ol>

```rust
impl<CTX> Component<CTX> for Model
where
    CTX: AsMut<ConsoleService>,
{
    type Message = Msg;
    type Properties = ();

    fn create(_: Self::Properties, _: &mut Env<CTX, Self>) -> Self {
        Model { value: 0 }
    }

    fn update(&mut self, msg: Self::Message, env: &mut Env<CTX, Self>) -> ShouldRender {
        match msg {
            Msg::Increment => {
                self.value = self.value+1;
            }
            Msg::Decrement => {
                self.value = self.value-1;
            }
        }
        true
    }
}
```
    

<ol start="4">
  <li>
    Create a view that displays the value and the buttons, and sends the messages on a click
  </li>
</ol>

```rust
impl<CTX> Renderable<CTX, Model> for Model
where
    CTX: AsMut<ConsoleService> + 'static,
{
    fn view(&self) -> Html<CTX, Self> {
        html! {
            <div>
                <nav class="menu",>
                    <button onclick=|_| Msg::Increment,>{ "Increment" }</button>
                    <button onclick=|_| Msg::Decrement,>{ "Decrement" }</button>
                </nav>
                <p>{ self.value }</p>
                <p>{ Date::new().to_string() }</p>
            </div>
        }
    }
}
```
    

and that&rsquo;s pretty much it ! It works well with [stdweb](https://github.com/koute/stdweb) and [cargo web](https://github.com/koute/cargo-web).

&#8230; have a look at the [examples](https://github.com/DenisKolodin/yew/tree/master/examples) (I took the counter example there), and enjoy how easy it is to do javascript without writing javascript.

# <a id="immutable" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Immutable data structures and why you want them

A great talk with a great <a href="https://bodil.lol/persistence/" rel="nofollow">slide deck</a>. I&rsquo;m a bit sad @bodil talked mostly about the data structures, I&rsquo;d have loved to hear more about the necessity for their immutability.

Anyway, if you wanna learn stuff on

  * <a href="https://doc.rust-lang.org/std/boxed/#examples" rel="nofollow">Cons lists</a>
  * Trees
  * Binary trees
  * <a href="https://en.wikipedia.org/wiki/B-tree" rel="nofollow">B-trees</a>
  * <a href="https://en.wikipedia.org/wiki/Radix_tree" rel="nofollow">Tries (a.k.a radix trees)</a>
  * Relaxed Radix Balanced Trees

&#8230;go watch the talk ! She provides an impressive reading list of papers regarding RRB trees :

  * Okasaki: <a href="https://www.cs.cmu.edu/%7Erwh/theses/okasaki.pdf" rel="nofollow">Purely Functional Data Structures</a> 
  * L&rsquo;Orange: Understanding Clojure&rsquo;s Vectors (  
    <a href="https://hypirion.com/musings/understanding-persistent-vector-pt-1" rel="nofollow">part 1</a>, <a href="https://hypirion.com/musings/understanding-persistent-vector-pt-1" rel="nofollow">2</a>, <a href="https://hypirion.com/musings/understanding-persistent-vector-pt-3" rel="nofollow">3</a>  
    )
  * Bagwell: <a href="http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.21.6279" rel="nofollow">Ideal Hash Trees</a> 
  * Hinze, Paterson: <a href="https://www.cs.ox.ac.uk/ralf.hinze/publications/FingerTrees.pdf" rel="nofollow">Finger Trees, a simple general-purpose data structure</a> 
  * Acar, Charguéraud, Rainey: <a href="https://hal.inria.fr/hal-01087245" rel="nofollow">Theory and Practice of Chunked Sequences</a> 
  * Stucki, Rompf, Ureche, Bagwell: <a href="https://infoscience.epfl.ch/record/213452/files/rrbvector.pdf" rel="nofollow">RRB Vector: A Practical General Purpose Immutable Sequence</a> 

After skimming through a few of them&#8230; I know I&rsquo;m gonna need more time during lunch breaks this week to dive deeper on the topic 🙂

She also dropped some cools remarks:

  * _nobody is gonna use a library with a bad documentation_. Sounds obvious ? It is. And yet as developpers we don&rsquo;t like to write docs anyway, but we should work on that.
  * I can&rsquo;t wait for the moment I&rsquo;m gonna use The « Haskell Defence » in an argument, aka « immutable values make it easier to reason about your program »

# <a id="infrastructure" class="anchor" href="#building-reliable-infrastructure" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Building reliable infrastructure

[@spacejam](https://github.com/spacejam) talked about [how to introduce verifications in complex architectures](https://github.com/spacejam/slides/blob/master/reliable_infrastructure_in_rust.pdf)&#8230; and he introduced tons of great tools that can help us, software developpers, write better applications, with an amazing set of references.

The issue with everything we build stems from our brain : everything we know is subject to bias, and everything we build reflects these biases (see _<a href="https://www.readthesequences.com/" rel="nofollow">Rationality: From AI to Zombies</a>_ (confonting assumptions)). Since our code reflects our biases, our automated tests do as well&#8230;so our tests tend not to be as effective as they could be.

A solution: **don&rsquo;t write tests**. Write **expectations** instead, and **have the machine generate random test cases**.

There is a for that, called [proptest](https://github.com/altsysrq/proptest).

It gives **non-determinism** in test execution, but with replayability (if a test case crashes, it does not simply crash randomly : you can relaunch it). It is used in [im-rs](https://github.com/bodil/im-rs), where there are tons of examples.

Another option is _Model based testing_:

  1. write a simplified model of a system
  2. apply random sequences of operations on both the implementation and the model
  3. if the model and implementation behave differently, it means we&rsquo;ve found a problem
  4. the library will rerun the test, dropping out operations until it finds a minimal failing sequence (the machine just wrote a regression test for you!!!)

There&rsquo;s a crate for that: <a href="https://crates.io/crates/model" rel="nofollow"><strong>model</strong></a>

Another option is **fault injection**. You make your system crash, and see how behaves. Sounds obvious ? Well the problem is not solved anyway. « in 58% of the catastrophic failures, the underlying faults could easily have been detected through simple testing of error handling code. », according to <a href="https://blog.acolyer.org/2016/10/06/simple-testing-can-prevent-most-critical-failures/" rel="nofollow">Yuan et al., OSDI 2014</a>. Again, there are crates for that :

  * [Fail](https://github.com/pingcap/fail-rs)
  * <a href="https://crates.io/crates/pagecache" rel="nofollow">pagecache</a>

There were things about **jepsen** and [**TLA+**](/home/clemk/dev/rustfest/learntla.com), but by now if you are interested you should at least watch the slides.

He did not cover how to build such architectures, but provided some great references:

  * _Google&rsquo;s <a href="https://landing.google.com/sre/book.html" rel="nofollow">Site Reliability Engineering</a>_
  * The book _Designing database intensive applications_ 
  * _<a href="http://www.brendangregg.com/sysperfbook.html" rel="nofollow">Systems performance, enterprise and cloud</a>_ by Brendan Gregg (the guy behind flamegraph)

# Learning how to learn {#learn}

<a href="https://speakerdeck.com/vaidehijoshi/learning-how-to-learn" rel="nofollow">Link to the slide deck</a>

In 2015, <a href="https://twitter.com/vaidehijoshi/" rel="nofollow">@vaidehijoshi</a> learnt computer science on her own through <a href="https://medium.com/basecs" rel="nofollow">her project basecs</a>: study a CS topic every week for a year, and publish a blog post. She created her own curriculum through those 52 articles. It had unexpected side effects ! The writen baseCS turned into a podcast, and a video serie.

One the main lesson is that learning new things is **extremely hard**. So she studied the psychology & science behind learning. It led her to Richard Feynman, a famous phisicist who had a Nobel prize. Unsurprisingly, he also taught physics, but&#8230; he was also an artist, a philosopher, a bongo player, and many other things you don&rsquo;t expect from a Nobel. Like, he particularly liked to break safes.  
The thread through all his achievements is that he was super great at learning and understand things he was unconfortable with.

Let&rsquo;s talk about how he learnt, and then I&rsquo;ll summarize why it works well.

## <a id="user-content-the-feynman-technique" class="anchor" href="#the-feynman-technique" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>The Feynman Technique

Feynman left what is now called the Feynman Technique for learning, which has **four steps**:

  1. **Identify the subject**, the thing we want to learn

write down everything we know, and add things to this repository

<ol start="2">
  <li>
    <strong>Explain it to someone who&rsquo;d knw nothing about the topic</strong> (teach it as if it was to a 5yo child) => It forces you to use plain, simple terms
  </li>
</ol>

« When we speack without jargon, it frees us from hiding behind knowledge we don&rsquo;t have ». We are pushed to go the the heart of a concept. **Brevity** is important and necessary, because childs don&rsquo;t have a long attention span. Do not fear using **diagrams**. They were one of Feynman&rsquo;s most important tools.

<ol start="3">
  <li>
    <p>
      <strong>identify any gaps</strong> in your understanding. Arguably the most important, it&rsquo;s where the learning happens.
    </p>
  </li>
  
  <li>
    <p>
      <strong>Organize & simplify into a narrative</strong>. Use simple sentences for story telling, analogies&#8230;
    </p>
  </li>
</ol>

Here is how he would explain atoms work, in a sentence:  
« all things are made from atoms &#8211; little particles that move around in perpetual motion, attracting each other when they are a little distance apart, but repelling upon being squeezed into one another »

Feynman was nicknamed « The Great Explainer » (« the best teacher I never had », bill gates)=> maybe **one of the important aspects of learning is to be able to teach things**  
Another is component is **curiosity**: he had a notebook « Notebook of things I don&rsquo;t know about ». In his bio, _Genius_, he said he tried to find the essential kernels of each subjects.

This methodology:

  * **tests our understanding**
  * **challenges our assumptions**. Often, we you start learning a topic, you don&rsquo;t know what you don&rsquo;t know. « I&rsquo;m smart enough to know that I&rsquo;m dumb », said Feynman.
  * **Reinforces what we do know**
  * teaches us to be **better explainers**. By reframing stuff we know, and forcing us to teach things simply, we know that we know something once we are able to do that. Even for particularly complex topics.

Also, it **makes knowledge accessible**. People get interested to stuff when you explain it to them simply. Tech needs more great explainers !  
As a side-effect, it makes our industry more diverse and inclusive.

# <a id="communities" class="anchor" href="#supercharging-rust-communities" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Supercharging Rust Communities

Matt Gathu (@swissgathu) talked about what made the rust communities such a success.

  * **Flat governance**. There is no chain of command, no hierarchy. Teams are more or less independant. As a consequence, things get to move very fast, because there is not the bureaucracy of having someone to approve of a choice
  * **Diversity & Inclusivity** as a goal. Be deliberate about diversity and inclusion.
  * Having a roadmap allows to have a **shared vision** 
  * **Collective decision making**. In the « RFC decision process », everyone has a say. Decisions are not made behind a closed door, you can always know why a given choise has been made.
  * Having a **Code of Conduct**. It&rsquo;s a conscious effort to make sure everyone would be safe. People have joined because other communities were toxic to them.
  * **Retrospectives**. Take time to reflect on what you did: what is going right ? what can we improve ? This let&rsquo;s you iterate faster.

It was also noted in another conference that the Rust&rsquo;s language itself is really good due to the presence of great docs, a build system, package manager, memory safety&#8230;