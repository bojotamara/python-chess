for i in *.svg ; do convert -background none -size 64x64 "$i" "${i%.*}-white.png" ; done
#for i in *.svg ; do convert -negate -background none -size 64x64 "$i" "${i%.*}-black.png" ; done
