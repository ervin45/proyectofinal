#!/bin/bash -x

ARCHIVOS=`find . -name "*.png" -and -not -name "login.png"`

for ARCHIVO in $ARCHIVOS
do
	FNAME="${ARCHIVO##*/}"
	EXT="${ARCHIVO##*.}"
	NEWNAME="${FNAME%%.$EXT}".eps

	#convert -resize 400x300 $FNAME $NEWNAME
	convert -rotate 270 -resize 1024x614 $FNAME $NEWNAME
done

convert -resize 512x307 login.png login.eps