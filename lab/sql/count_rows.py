#!/usr/bin/env python

import psycopg2
import psycopg2.extras
import pprint

con_dwh = psycopg2.connect(host="192.168.61.100", port=5432, user="ncesar", password=".", database="bieler_dw")
cursor_dwh = con_dwh.cursor()

sql= """select grupo_constructivo|| ' - ' ||modelo as columns, anio as rows, avg(stock) as stock
from ft_movimientos
join td_pieza on (ft_movimientos.fk_pieza = td_pieza.id) join td_tiempo on (ft_movimientos.fk_tiempo = td_tiempo.id)
where td_pieza.grupo_constructivo in('184') 
group by grupo_constructivo, modelo, anio
order by grupo_constructivo, modelo, anio"""

cursor_dwh.execute(sql)

print cursor_dwh.rowcount

