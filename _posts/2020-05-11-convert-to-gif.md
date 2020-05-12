---
title: Better pull requests with GIFs from screen recordings
author: Keirua
layout: post
lang: en
image: mp4-to-gif.png
---

## TL;DR

Adding a **short GIF animation is a great way to communicate** how a new feature behave in a pull request (example [here](https://github.com/betagouv/demarches-simplifiees.fr/pull/4996)).

Here is the final script `convert-to-gif.sh` you can use to convert a mp4 screen recording into a `gif` file:

    #!/bin/sh

    # using a palette reduce the size of the gif
    ffmpeg -y -i $1.mp4 -vf palettegen palette-$1.png
    ffmpeg -y -i $1.mp4 -i palette-$1.png -filter_complex paletteuse -r 10 $1.gif

You can save this as `convert-to-gif.sh`, make it executable (`chmod +x convert-to-gif.sh`), then use it through `./convert-to-gif.sh some-video`.

## The problem

I use [Kazam](https://launchpad.net/kazam) to make short video recordings. It can record the whole screen, a window or a part of the screen and can export to mp4, which suits most of my demo recording needs.

Making **screen recordings** has already proven to be super useful when I do **tech demos**. I can totally **avoid the infamous "demo effect"**, and the **demo time is kept under precise control**.

Recently, I've started including animated gifs of some features I've been working on in my pull requests, like [this one](https://github.com/betagouv/demarches-simplifiees.fr/pull/4996). We have lot of freedom in the way we implement things, so it helps my colleagues understand what a button or workflow may look like in the app when they approve the pull request, without the need to launch the app on their own, go to a particular screen, etc.

Unfortunately, Kazam does not export to gif, and I don't want to have to search, install, maintain another software on my machine. These tools often have a short lifespan, so I don't want to have to go throush that process again the next time I setup a machine, in order to find alternative.

## Solutions

My workaround is to use ffmpeg in order to convert the videos I make. It's the underlying library many video applications use, so the odds are it won't change much in the next few years.

Let's take a recent example, a 9 second, 360kb mp4 video. **The easiest way creates huge gif**:

```bash
ffmpeg -y -i input.mp4 -r 5 output.gif
```

The quality is good but it generates a 6.7mb gif, that's almost 18 times the initial size. Even if github hosts the image and we don't pay for hosting, people have to download it, maybe through their mobile data so 6.7mb for a 9s gif is unacceptable. We have to do better.

**Another option is to convert our video to individual frames**, then stitch those frames together using imagick:

```bash
mkdir -p .frames-input && ffmpeg -i input.mp4  -r 5 .frames-input/frame-%03d.jpg
convert -delay 20 -loop 0 .frames-input/*.jpg output.gif
```

The `-r` option indicates the fps (5 frames per second), and every image is displayed for 200 ms (`-delay 20`).

That's *4.1mb* now, but it introduces some terribly ugly jpeg artifacts, and it results in a blurry, hard to read gif. We can again do better.

**We can improve the quality using PNGs**, which is a lossless compression format:

```bash
mkdir -p .frames-input && ffmpeg -i input.mp4  -r 5 .frames-input/frame-%03d.png
convert -delay 20 -loop 0 .frames-input/*.png output.gif
```

That's *3.3mb* now without artifacts : the end result is clean. That's half the initial gif, but still *10 times* the size the mp4 video.

**The best solution I've found is to export a color palette**, and use this color palette for the gif. Using this method, the quality is the same as in the video (no jpeg/gif artifacts), and the gif is super slim, 412kb in this example. Here is the final script:

```bash
#!/bin/sh
# using a palette reduce the size of the gif
ffmpeg -y -i $1.mp4 -vf palettegen palette-$1.png
ffmpeg -y -i $1.mp4 -i palette-$1.png -filter_complex paletteuse -r 10 $1.gif
```

You can save this as convert-to-gif.sh, make it executable (chmod +x convert-to-gif.sh), then use it through ./convert-to-gif.sh some-video, provided there is a some-video.mp4 file in the directory. Beware, the -y option erases the output file if it already exists.

![](https://user-images.githubusercontent.com/1223316/78377614-1b4e8700-75d0-11ea-9e2f-42cf5929e32d.gif)