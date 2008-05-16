#!/usr/bin/env python
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

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

