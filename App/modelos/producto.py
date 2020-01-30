from db import Database

db = Database()

#Modelo Producto 
class Producto:
    def __init__(self):
        self.__id = None
        self.__nombre = ''
        self.__descripcion = ''
        self.__precio = None
        self.__modelo = None
        self.__garantia = None
        self.__tipo_producto = None
        self.__marca = None

    #Setter
    def set_id(self, pId):
        self.__id = pId
    
    def set_nombre(self, pNombre):
        self.__nombre = pNombre
    
    def set_descripcion(self, pDescripcio):
        self.__descripcion = pDescripcio

    def set_precio(self, pPrecio):
        self.__precio = pPrecio

    def set_modelo(self, pModelo):
        self.__modelo = pModelo   

    def set_garantia(self, pGarantia):
        self.__garantia = pGarantia

    def set_tipo_producto(self, pTipoProducto):
        self.__tipo_producto = pTipoProducto

    def set_marca(self, pMarca):
        self.__marca = pMarca

    #Getter
    def get_id(self):
        return self.__id
    
    def get_nombre(self):
        return self.__nombre
    
    def get_descripcion(self):
        return self.__descripcion

    def get_precio(self):
        return self.__precio

    def get_modelo(self):
        return self.__modelo   

    def get_garantia(self):
        return self.__garantia
    
    def get_tipo_producto(self):
        return self.__tipo_producto

    def get_marca(self):
        return self.__marca

    #Logica
    def verificar_unico_producto(self):
        verificador = db.querySelect('''
                SELECT * FROM "producto" WHERE "nombre" = '{}';
            '''.format(self.__nombre))
        return verificador

    def alta_producto(self):
        data =[]
        data = db.queryInsert('''
             INSERT INTO "producto" 
                ("nombre", "descripcion", "precio", "modelo", "garantia", "tipoProducto", "marca") 
                values ('{}','{}','{}','{}','{}','{}','{}');
                '''.format(
                        self.__nombre, 
                        self.__descripcion, 
                        self.__precio, 
                        self.__modelo, 
                        self.__garantia, 
                        self.__tipo_producto, 
                        self.__marca))
        return data

    def baja_producto(self):
        data = db.queryInsert('''
               DELETE FROM "producto" WHERE "nombre" = '{}'; 
            '''.format(self.__nombre))
        return data


    def modificar_producto(self, pNuevoNombre, pNuevaDescripcion, pNuevoPrecio, pNuevoModelo, pNuevaGarantia, pNuevoTipoProducto, pNuevaMarca):
        data = db.queryInsert('''
                                UPDATE "producto"
                                        SET "nombre" = '{}', 
                                        "descripcion" = '{}', 
                                        "precio" = '{}', 
                                        "modelo" = '{}', 
                                        "garantia" = '{}', 
                                        "tipoProducto" = '{}', 
                                        "marca" = '{}'
                                        WHERE "nombre" = '{}';
                                '''.format(
                                        pNuevoNombre,
                                        pNuevaDescripcion,
                                        pNuevoPrecio,
                                        pNuevoModelo,
                                        pNuevaGarantia,
                                        pNuevoTipoProducto,
                                        pNuevaMarca,
                                        self.__nombre))
        return data

    def consultar_producto(self):
        data =[]
        data = db.querySelect('''
                SELECT * FROM "producto";
            ''')
        return data 

    def stock(self):         
        stock = None
        #Agregar logica de stock aca
        return stock

    def consultar_vista_productos(self):
        data = db.querySelect(
            ''' 
            SELECT * FROM public.vista_productos;
            ''')
        return data  

    def listar_productos(self):
        data = db.querySelect('''
                SELECT * FROM "producto";
            ''')
        return data 