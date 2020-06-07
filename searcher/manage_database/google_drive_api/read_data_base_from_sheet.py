import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from ...simple_scripts import text


def readGoogleSheet():
    scope = [
        'https://spreadsheets.google.com/feeds', 
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/home/mono/projects_web_apps/django_projects/ahome_api/searcher/manage_database/google_drive_api/ahome-api-be0bc461b723.json',
        scope
    )

    gc = gspread.authorize(credentials)

    work_book = gc.open('BASE DE DATOS ')

    all_properties = []
    for sheet in work_book:    
        properties = sheet.get_all_records()
        available = []
        for prop in properties:
            if prop['STATUS'] == 'D' and prop['I.D.'] != '' and prop['TIPO'] != '':
                available.append(prop)        
        for prop in available:
            all_properties.append(prop)
    return all_properties


class PropertiesInformation(object):


    def __init__(self):
        self.properties_raw = readGoogleSheet()
        self.properties_clean = {}
        self.clean_properties()
    
    def clean_properties(self):
        for prop in self.properties_raw:
            ahome_id = prop["I.D."]
            accion = ""
            if 'AH' in ahome_id:
                accion = "Venta"
            elif 'H' in ahome_id:
                accion = "Renta"
            elif 'A' in ahome_id:
                accion = "Venta"
           
            self.properties_clean[ahome_id] = {
                "TYPE" : prop["TIPO"],
                "ACTION" : accion,
                "CITY" : text.normalize_text(prop["CIUDAD"]),
                "STATE" : text.normalize_text(prop["ESTADO"]),
                "ZONE" : text.normalize_text(prop["ZONA"]),
                "HOOD" : prop["COLONIA O FRACCIONAMIENTO"],
                "ADDRES" : prop["DIRECCION"],
                "TOTAL AREA" : self.check_float(prop["METROS TERRENO"]),
                "PRICE": self.check_price(prop["PRECIO"])
            }
        
            if prop['TIPO'] == 'Terreno':
                self.properties_clean[ahome_id]['CONSTRUCTION AREA'] = 0.0
                self.properties_clean[ahome_id]['ROOMS'] = 0
                self.properties_clean[ahome_id]['HALF BATHS'] = 0
                self.properties_clean[ahome_id]['BATHS'] = 0
                self.properties_clean[ahome_id]['PARKING'] = 0
                self.properties_clean[ahome_id]['DESCRIPTION'] = prop['DESCRIPCION']
            else:
                self.properties_clean[ahome_id]['CONSTRUCTION AREA'] = self.check_float(prop['METROS CONSTRUCCION'])
                self.properties_clean[ahome_id]['ROOMS'] = self.check_integer(prop['HABITACIONES'])
                self.properties_clean[ahome_id]['HALF BATHS'] = self.check_integer(prop['MEDIOS BAÑOS'])
                self.properties_clean[ahome_id]['BATHS'] = self.check_integer(prop['BAÑOS COMPLETOS'])
                self.properties_clean[ahome_id]['PARKING'] = self.check_integer(prop['ESTACIONAMIENTO'])
                self.properties_clean[ahome_id]['DESCRIPTION'] = prop['HIGHLIGHTS'] + ' ' + prop['DESCRIPCION']

    def check_price(self, string_price):
        try:
            assert(string_price != '')
            comma_price = string_price.split('$')[1]
            integer_price = comma_price.replace(',', '')
            return float(integer_price)
        except AssertionError:
            return 0.0

    def check_float(self, value):
        try:
            number = float(value)
            return number
        except ValueError:
            return 0.0
    
    def check_integer(self, value):
        try:
            number = int(value)
            return number
        except ValueError:
            return 0

    def get_information(self):
        return self.properties_clean
    


if __name__ == "__main__":
    a = PropertiesInformation()
