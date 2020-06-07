from ..simple_scripts import text


def process(raw_Data):
    cookedData = {}
    cookedData['where'] = processWhere(raw_Data['where'])
    cookedData['operationType'] = processOperation(raw_Data['operationType'])
    cookedData['propertyType'] = processType(raw_Data['propertyType'])
    cookedData['rooms'] = processRoom(raw_Data['check'])
    cookedData['baths'] = processBath(raw_Data['check-bath'])
    cookedData['price'] = processPrice(raw_Data['price'], cookedData['operationType'])
    return cookedData

def processWhere(param):
    if param == '' or param == False:
        return False
    param = text.normalize_text(param)
    possibilities = param
    return possibilities

def processOperation(param):
    if param:
        operation = {"1":'VENTA', "2":"RENTA"}
        return operation[param]
    else:
        return False
        
def processType(param):
    if param:
        type_ = {"1":["Departamento"], "2":["Casa Habitación", "Residencia"], "3":["Terreno"], "4":["Oficina"], "5":["Bodega"],
                "6":["Local Comercial"], "7":["Salon de Fiestas", "Salón de Fiestas"] 
        }
        return type_[param]
    else:
        return False

def processRoom(param):
    if not param:
        return param
    else:
        return param

def processBath(param):
    if not param:
        return param
    else:
        return param

def processPrice(param, action):
    maxPrice = 0
    minPrice = 0
    precioFinal = 0
    if action == 'VENTA':
        maxPrice = 1.5E+07
        minPrice = 1.0E+06
        porcentaje = int(param) / 100
        precioFinal =  porcentaje * (maxPrice - minPrice) + 1E6
    elif action == 'RENTA':
        maxPrice = 70000
        minPrice = 1000
        porcentaje = int(param) / 100
        precioFinal =  porcentaje * (maxPrice - minPrice) + 1000
    return precioFinal
