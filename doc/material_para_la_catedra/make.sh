#!/bin/bash

## actualizacion de versiones-iteraciones... etc
#./update.sh

rst2latex --language=es \
          --no-doc-title \
	  --use-latex-footnotes \
	  --documentclass=book \
	  --documentoptions=12pt,oneside,a4paper \
	  --stylesheet=proyecto.stx \
	  --section-numbering \
	  --file-insertion-enabled \
	  --use-latex-citations  \
	  --use-latex-toc  < documentacion_final.txt > documentacion_final.tex
	  
RESULT=$?

if [ $RESULT -eq 0 ]
then
	latex documentacion_final.tex
fi
