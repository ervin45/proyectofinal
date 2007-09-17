#!/bin/sh

if [ $# -eq 0 ]
then
	echo "usage: $0 archivo_impresion_octosis.txt"
fi

perl -i -p -e 'undef $/; s@\f\r\x12\r\n.*?Saldo Inicial al.*?\]@@msg' $1
