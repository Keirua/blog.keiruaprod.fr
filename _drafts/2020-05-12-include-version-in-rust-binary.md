# How to include the build version inside a rust binary

A recent problem was to include the build version of a rust binary, so that `$ program --version` answers with the appropriate version number.

We'll look at various solutions.

## Starting with an empty example

Here is a snippet of such a program:

```rust
// bin/empty.rs
extern crate clap; 
use clap::App; 
 
fn main() { 
    App::new("")
       .version("1.0")
       .get_matches(); 
}
```

in `Cargo.toml`, you'll need to add `clap = "*"` as a dependency. It's a popular crate that does Command Line Argument Parsing, you'll encounter it often if you write command line programs.

If you run this example, it'll output our hardcoded version:

```bash
$ cargo run --bin empty -- --version
 1.0
```

It's not very useful for now since it's static, but that's a start.

A note about the command syntax: 

 - first we tell cargo that we want to run a binary (something in the `bin` directory) called empty : `cargo run --bin empty`
 - then we tell that we want to provide this program with arguments using `--`
 - then we provide the arguments, here `--version`

It's very similar as running `cargo build && ./target/debug/empty --version`.

## Using cargo built-in variables

Let's improve this program. A first way to do is it to use **cargo's built-in variables**:

```rust
// bin/cargopkg.rs
fn main() { 
    App::new("")
       .version(env!("CARGO_PKG_VERSION"))
       .get_matches(); 
}
```

If we run this program, we have a version:

```bash
$ cargo run --bin cargopkg -- --version
 0.1.0
```

Where does this `0.1.0` come from ? `std::env!` is a macro that fetches the value of an environment variable during compile time. **`CARGO_PKG_VERSION` gives us the version number set in `Cargo.toml`**.

A few [other environment variables](https://doc.rust-lang.org/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-crates) are available.

If you go in this direction, **you'll need to update your version every time you make a release**. There are pros and cons to this approach.

## Using a build script

Another approach is to **use a build script**. There are many parts so it is a bit hard to grasp at first:

 - we'll **setup a build script, `build.rs`**, and specify it's a build script in `Cargo.toml`
 - **our build script will print something with [a specific syntax](https://doc.rust-lang.org/cargo/reference/build-scripts.html#outputs-of-the-build-script)**.
 - **the build scripts' output is used by Cargo as an input** so that we can feed infos to cargo

One of the things we can tell Cargo is "let's add a new environment variable, with the hash of the latest commit". Let's do that.

```toml
# Cargo.toml
[package]
# …
build = "build.rs"
```

Cargo only supports one build script per project at the moment, so everything we do will be available to all the binary (should they care to use it). Here is our `build.rs` script:

```rust
// build.rs
use std::process::Command;
fn main() {
    // taken from https://stackoverflow.com/questions/43753491/include-git-commit-hash-as-string-into-rust-program
    let output = Command::new("git")
        .args(&["rev-parse", "HEAD"])
        .output()
        .unwrap();
    let git_hash = String::from_utf8(output.stdout).unwrap();
    println!("cargo:rustc-env=GIT_HASH={}", git_hash);
}
```

So we write a program that fetches the last commit hash via `git rev-parse HEAD`. [git rev-parse](https://git-scm.com/docs/git-rev-parse) provides the SHA1 of a revision.

Now we can make use of the `GIT_HASH` environment variable in our main program:

```rust
// bin/gitcommit.rs
extern crate clap; 
use clap::App; 
 
fn main() { 
    App::new("")
       .version(env!("GIT_HASH"))
       .get_matches(); 
}
```

Now, lets run this program:

```bash
$ cargo run --bin gitcommit -- --version
909d20fe5bf4cfc3ae784c78401455b42bdf02d2
```

This is the approach we went with for [`ds_proxy`](https://github.com/betagouv/ds_proxy/pull/20/files)

## Using a dedicated crate

Well, parsing the git output ourselves in order to feed it to a special cargo string can be a bit tedious. As often in the rust ecosystem, there is a crate for that. [vergen](https://github.com/rustyhorde/vergen) exposes [a bunch of environment variables](https://docs.rs/vergen/3.0.4/vergen/#generate-build-time-information), like the build date, the sha1 of the commit or the target architecture.
