from db import Database
 
db = Database()

#Modelo Ejemplar 
class Ejemplar:
    def __init__(self):
        self.__numeroSerie = None
        self.__vendido = None #booleano
        self.__producto = None

    #Setter
    def set_numero_serie(self, pNumeroSerie):
        self.__numeroSerie = pNumeroSerie
    
    def set_vendido(self, pVendido):
        self.__vendido = pVendido

    def set_producto(self, pProducto):
        self.__producto = pProducto

    #Getter
    def get_numero_serie(self):
        return self.__numeroSerie
    
    def get_vendido(self):
        return self.__vendido

    def get_producto(self):
        return self.__producto

    #Logica
    def verificar_ejemplar(self):
        verificador = db.querySelect('''
                SELECT * FROM "ejemplar" WHERE "numeroSerie" = '{}';
            '''.format(self.__numeroSerie))
        return verificador        

    def alta_ejemplar(self):
        data = db.queryInsert('''
                INSERT INTO "ejemplar" 
                ("numeroSerie", "vendido", "producto") 
                values ('{}','{}','{}');
                '''.format(
                    self.__numeroSerie,
                    self.__vendido,
                    self.__producto))
        return data

    def baja_ejemplar(self):
        data = db.queryInsert('''
               DELETE FROM "ejemplar" WHERE "numeroSerie" = '{}'; 
            '''.format(self.__numeroSerie))
        return data

    def modificar_ejemplar(self, pNuevoNumeroSerie, pNuevoVendido, pNuevoProducto):
        data = db.queryInsert('''
                    UPDATE "ejemplar"
                            SET "numeroSerie" = '{}', 
                            "vendido" = '{}', 
                            "producto" = '{}'
                            WHERE "numeroSerie" = '{}';
                    '''.format(
                        pNuevoNumeroSerie,
                        pNuevoVendido, 
                        pNuevoProducto, 
                        self.__numeroSerie))
        return data

    def ejemplares_de_un_producto(self, producto):
        data = db.querySelect('''
                SELECT * FROM "ejemplar"
                WHERE "producto" = '{}';
            '''.format(producto))
        return data

    def consultar_ejemplar(self):
        data = db.querySelect('''
                SELECT * FROM "ejemplar";
            ''')
        return data

    def consultar_vista_ejemplares(self):
        data = db.querySelect(
            ''' 
            SELECT * FROM public.vista_ejemplares;
            ''')
        return data