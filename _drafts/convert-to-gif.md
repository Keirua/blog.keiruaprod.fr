Turning a mp4 screen recording into a gif

I use Kazam when have to make video recording. This is super useful when I do tech demos and I don't want the infamous "demo effect".

It can record the whole screen, a window or a part of the screen and can export to mp4, which suits most of my demo recording needs.

Recently, I've started including animated gifs of some features I've been working on in my pull requests. We have lot of freedom in the way we implement things, so it helps my colleagues understand what a button or workflow may look like in the app when they approve the pull request, without the need to launch the app on their own, go to a particular screen, etc.

Unfortunately, Kazam does not export to gif, and I don't want to have to search, install, maintain another software on my machine. These tools often have a short lifespan, so I don't want to have to go throush that process again the next time I setup a machine, in order to find alternative.

My workaround is to use ffmpeg in order to convert the videos I make. It's the underlying library many video applications use, so the odds are it won't change much in the next few years.

Let's take a recent example, a 9 second, 360kb mp4 video. The easiest way creates huge gif:

    ffmpeg -y -i input.mp4 -r 5 output.gif

The quality is good but it generates a 6.7mb gif, that's almost 18 times the initial size. Even if github hosts the image and we don't pay for hosting, people have to download it, maybe through their mobile data so 6.7mb for a 9s gif is unacceptable. We have to do better.

Another option is to convert our video to individual frames, then stitch those frames together using imagick:

    mkdir -p .frames-input && ffmpeg -i input.mp4  -r 5 .frames-input/frame-%03d.jpg
    convert -delay 20 -loop 0 .frames-input/*.jpg output.gif

The -r option indicates the fps (5 frames per second), and every image is displayed for 200 ms (-delay 20).

That's 4.1mb now, but it introduces some terribly ugly jpeg artifacts, and it results in a blurry, hard to read gif. We can again do better.

We can improve the quality using PNGs, which is a lossless compression format:

    mkdir -p .frames-input && ffmpeg -i input.mp4  -r 5 .frames-input/frame-%03d.png
    convert -delay 20 -loop 0 .frames-input/*.png output.gif

That's 3.3mb now without artifacts : the end result is clean. That's half the initial gif, but still 10 times the mp4 video.

The best solution I've found is to export a color palette, and use this color palette for the gif. Using this method, the quality is the same as in the video (no jpeg/gif artifacts), and the gif is super slim, 412kb in this example. Here is the final script:

    #!/bin/sh

    # using a palette reduce the size of the gif
    ffmpeg -y -i $1.mp4 -vf palettegen palette-$1.png
    ffmpeg -y -i $1.mp4 -i palette-$1.png -filter_complex paletteuse -r 10 $1.gif

You can save this as convert-to-gif.sh, make it executable (chmod +x convert-to-gif.sh), then use it through ./convert-to-gif.sh some-video, provided there is a some-video.mp4 file in the directory. Beware, the -y option erases the output file if it already exists.