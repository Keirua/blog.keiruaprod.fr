---
title: You don't need microservices.
layout: post
lang: en
---

I regularly receive requests to work on microservices. Here is my position.

If you are a small business (say, less than 100 million euros), the odds are you'd be better off with a **monolithic architecture** for your next project. If you are starting or have a small team (less than ten persons), the microservice approach will most likely not help you grow your business.


## What are microservices?

A **microservice setup** usually goes like this:

 - each microservice has its code repository
 - each microservice has its CI and deployment pipeline
 - each microservice has its infrastructure (VM or container, webserver…)
 - each microservice has its database. A microservice has no idea what other business things exist
 - communication between services is done asynchronously through a message queue

By introducing separated databases or message queues, you add new moving parts to the system, and new classes of bugs appear.

## Microservices misconceptions 

Microservices is still a popular pattern in the tech crowd because of two assumptions:

 - separation of concerns at the **code level** is a good thing.
 - separation of concerns at the **infrastructure level** is an improvement over monolithic code architectures.

The two ideas above understate that this **separation introduces technical complexity and new classes of bugs**.

## The problems

I used to think microservices would improve things because isolation helps isolate problems. To me, that seemed like a clean way to expose HTTP APIs.

I've since been part of three projects that involved microservices. They all were massive failures, in the sense that the **time to production was completely disconnected from the actual business complexity** (by a factor of, say, four: they were about four times longer to build than initially expected). It was not a question of capacity: in all cases, the team had great persons. It's just that building and debugging microservices take time.

Being slow on purpose is not what I think is suitable for my clients' products: I prefer short feedback loops between the development and usage of the product.

Separation of concerns, in itself, is usually a good thing; that's how you manage to have testable code. In some cases, that's how you extract some code to make it reusable. But I now think that going all-in on the separation of concerns is a tech whim instead of a solution to a business need, and probably for a long time.

That's the idea for microservices: they can't share data, they all are stateless, and they have a small responsibility. Microservices introduces complexity at many levels:
 - there's a technology gap for communication between services (the message queue)
 - you cannot debug through a single stack trace: you may need to propagate a request id through the communication and follow that in the logs.

## In summary

All of this is doable and possible, but for small businesses this is hardly compatible with the goal of shipping quickly.

The best summary I've found on the complexity slide from code to infra was on [Hackers news](https://news.ycombinator.com/item?id=12508655), a few years ago:

> You need to be this tall to use [micro] services:
> 
> * Basic Monitoring, instrumentation, health checks
> * Distributed logging, tracing
> * Ready to isolate not just code, but whole build+test+package+promote for every service
> * Can define upstream/downstream/compile-time/runtime dependencies clearly for each service
> * Know how to build, expose and maintain good APIs and contracts
> * Ready to honor b/w and f/w compatibility, even if you're the same person consuming this service on the other side
> * Good unit testing skills and readiness to do more (as you add more microservices it gets harder to bring everything up, hence more unit/contract/api test driven and lesser e2e driven)
> * Aware of [micro] service vs modules vs libraries, distributed monolith, coordinated releases, database-driven integration, etc
> * Know infrastructure automation (you'll need more of it)
> * Have working CI/CD infrastructure
> * Have or ready to invest in development tooling, shared libraries, internal artifact registries, etc
> * Have engineering methodologies and process-tools to split down features and develop/track/release them across multiple services (xp, pivotal, scrum, etc)
> * A lot more that doesn't come to mind immediately
>
> Thing is - these are all generally good engineering practices.
>
> But with monoliths, you can get away without having to do them. There is the "login to server, clone, run some commands, start a stupid nohup daemon and run ps/top/tail to monitor" way. But with microservices, your average engineering standards have to be really high. Its not enough if you have good developers. You need great engineers.

It matches my experience; it requires technical expertise that you may not need: Peter Levels runs a million-dollar business with [SQLite on a single machine](https://twitter.com/levelsio/status/1102487697220820994). That's another extreme. If you want us to work together, I'd rather help you shipping quickly instead of focusing on an idea of technical perfection.

Those details may not matter if you are starting if you don't find your market anyway.