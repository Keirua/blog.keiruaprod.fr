#!/bin/sh

ffmpeg -y -i $1.mp4 -vf palettegen palette-$1.png
ffmpeg -y -i $1.mp4 -i palette-$1.png -filter_complex paletteuse -r 10 $1.gif