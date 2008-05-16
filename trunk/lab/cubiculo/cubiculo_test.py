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
from cubiculo import Cubiculo

def pieza_mes_test():
    c = Cubiculo("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]])
    print c.sql()
    assert c.sql() == '\nselect td_tiempo.anio,td_pieza.codigo,sum(stock)\nfrom ft_movimientos\njoin td_tiempo on (ft_movimientos.fk_tiempo = td_tiempo.id) join td_pieza on (ft_movimientos.fk_pieza = td_pieza.id) \n\ngroup by td_tiempo.anio, td_pieza.codigo'

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
from cubiculo import Cubiculo

def pieza_mes_test():
    c = Cubiculo("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]])
    print c.sql()
    assert c.sql() == '\nselect td_tiempo.anio,td_pieza.codigo,sum(stock)\nfrom ft_movimientos\njoin td_tiempo on (ft_movimientos.fk_tiempo = td_tiempo.id) join td_pieza on (ft_movimientos.fk_pieza = td_pieza.id) \n\ngroup by td_tiempo.anio, td_pieza.codigo'

