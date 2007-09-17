#!/bin/sh

if [ $# -eq 0 ]
then
	echo "usage: $0 archivo_impresion_octosis.txt"
fi

#sacamos el encabezado
#desde:
# el principio
#hasta:
#C?digo..
perl -i -p -e 'undef $/; s@^.*?C\xa2digo:@ C\xa2digo:@s' $1


#sacamos el encabezado por cada pagina
#desde:
# 0c 0d  12 0d 0a
#hasta: 
#Saldo Inicial al..
perl -i -p -e 'undef $/; s@\x0c\x0d\x12\x0d\x0a.*?Saldo Inicial al.*?\]@@msg' $1


#sacamos el pie de informe
#desde:
# "[saldo Final.."
#hasta:
# -------...-------\x0c\x0
perl -i -p -e 'undef $/; s@\[ Saldo Final.*?-+\x0c\x0d@@s' $1