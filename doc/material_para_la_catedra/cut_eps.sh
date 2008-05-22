#!/bin/bash

TMPFILE=/tmp/diagrama_entidad_relacion_en_2_hojas.eps

poster -v -mA4 -p2x1A4 diagrama_entidad_relacion.eps  > $TMPFILE


psselect -p1 $TMPFILE diagrama_entidad_relacion1.eps
psselect -p2 $TMPFILE diagrama_entidad_relacion2.eps