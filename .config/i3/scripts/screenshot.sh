#! /bin/bash
maim -s | xclip -selection clipboard -t image/png; xclip -selection clipboard -t image/png -o > ~/Pictures/$(date +%F-%H:%M:%S).png
