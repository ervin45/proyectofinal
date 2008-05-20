def _compare_dicts_asc(a, b):
    if a[1] > b[1]:
        return 1
    elif a[1] < b[1]:
        return -1
    return 0

def _compare_dicts_desc(a, b):
    if a[1] > b[1]:
        return -1
    elif a[1] < b[1]:
        return 1
    return 0

def _top_ordered(d, total_elements = 10, order = "desc"):
    temp = d.items()
    if order=="desc":
        order_func = _compare_dicts_desc
    else:
        order_func = _compare_dicts_asc

    temp.sort(order_func)
    rtn = temp[:int(total_elements)]
    return dict(rtn)
    
def order_and_slice_the_cube(cube, total_elements=2, order="desc"):
    cube.data = _top_ordered(cube.data, total_elements, order)
    cube.clean()

order_and_slice_the_cube.meta = {
                                "label": "ordenar y recortar",
                                "params": [
                                            {"label": "Cantidad", "type":"text", "sequence": []}, 
                                            {"label": "Orden", "type": "select", "sequence": ["asc", "desc"]}
                                          ]
                                }

def order_and_slice_the_cube2(cube, total_elements=2, order="desc"):
    cube.data = _top_ordered(cube.data, total_elements, order)
    cube.clean()

order_and_slice_the_cube2.meta = {
                                "label": "ordenar y recortar2",
                                "params": [
                                            {"label": "Cantidad2", "type":"text", "sequence": []}, 
                                            {"label": "Orden2", "type": "text", "sequence": []}
                                          ]
                                } 

def top10(cube,eje = 0,total_elements = 10,order = 'desc'):    
    sum_1 = {}
    for k in cube.data.keys():
        try:
            sum_1[k[eje]] += cube.data[k]
        except:
            sum_1[k[eje]] = cube.data[k]

    top = _top_ordered(sum_1,total_elements, order).keys()
  
    for i in cube.data.keys():
        if i[eje] not in top:
            del cube.data[i]

    cube.clean()

top10.meta = {
    "label": "Top 10",
    "params": []
    }

def same_cube(cube):
    pass

same_cube.meta = {
                                "label": "Ninguno",
                                "params": []
                                }

def no_zeros(cube):
    eje = 0

    sum_1 = {}
    for k in cube.data.keys():
        try:
            sum_1[k[eje]] += cube.data[k]
        except:
            sum_1[k[eje]] = cube.data[k]

    
    los_zeros = [x[0] for x in tuple(sum_1.items()) if x[1] == 0]

    for i in cube.data.keys():
        if i[eje] in los_zeros:
            del cube.data[i]

    cube.clean()

no_zeros.meta = {
    "label": "Sin filas con todos ceros",
    "params": []
    }
