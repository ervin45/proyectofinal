from cubiculo import Cubiculo

def pieza_mes_test():
    c = Cubiculo("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]])
    print c.sql()
    assert c.sql() == '\nselect td_tiempo.anio,td_pieza.codigo,sum(stock)\nfrom ft_movimientos\njoin td_tiempo on (ft_movimientos.fk_tiempo = td_tiempo.id) join td_pieza on (ft_movimientos.fk_pieza = td_pieza.id) \n\ngroup by td_tiempo.anio, td_pieza.codigo'

