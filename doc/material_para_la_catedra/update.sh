#!/bin/bash

./update_vih.py | iconv --from=latin1 --to=utf8 > versiones-iteraciones-historias.txt
