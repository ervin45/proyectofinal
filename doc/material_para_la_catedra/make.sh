#!/bin/bash

rst2latex --language=es \
          --no-doc-title \
	  --documentclass=book \
	  --documentoptions=12pt,a4paper,spanish \
	  --stylesheet=proyecto.stx \
	  --section-numbering \
	  --file-insertion-enabled \
	  --use-latex-toc  < documentacion_final.txt > documentacion_final.tex
	  
latex documentacion_final.tex
