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


def same(cube):
    pass

same.meta = {
                                "label": "Ninguno",
                                "params": []
                                }