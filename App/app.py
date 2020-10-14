from flask import Flask, render_template, request, jsonify, session
from db import Database
from modelos.rol import Rol
from modelos.usuario import Usuario
from modelos.tipoProducto import TipoProducto
from modelos.marca import Marca
from modelos.producto import Producto
from modelos.ejemplar import Ejemplar
from modelos.combo import Combo
from modelos.carrito import Carrito
from modelos.compra import Compra
from modelos.pago import Pago
from modelos.ejemplar_combo import Ejemplar_combo
from modelos.storage import guardarImagen
from modelos.imagenes import Imagenes
from modelos.ejemplar_carrito import Ejemplar_carrito
from modelos.mercadoPago import MercadoPago
from modelos.mercadoPago import nuevaReerencia_mercadoPago
from modelos.mercadoPago import consultarReferencia_mercadoPago
from modelos.combo_carrito import Combo_carrito

db = Database()

app = Flask(__name__)

app.secret_key = 'apptaller2019'


@app.route('/')
def index():
    data = []
    producto = Producto()
    data = producto.listar_productos()

    #cuenta los elementos del data
    contador = 0
    for e in data:
        contador = contador+1
    #agrega el stock y las imágenes de cada producto
    for e in range(contador):

        #guarda el stock del producto en la posición 8 del data
        ejemplar = Ejemplar()
        cantidad = ejemplar.cantidad_ejemplares_de_un_producto(data[e][0])
        data[e] += (cantidad[0][0],)

        #guarda la primer imagen del producto en la posición 9 del data
        imagenes = Imagenes()
        imgs = imagenes.imagenes_producto(data[e][0])
        #Si no tiene imagen deja el campo vacio
        if imgs == []:
            data[e] += ()
        #Sino guarda la primer imagen
        else:
            data[e] += (imgs[0])

    ## Chequea si hay un usuario logueado
    if 'email' in session:
        usuario = Usuario()
        usuario.set_nombre(session['email'])
        dato = usuario.consultar_usuario_por_nombre()
        if dato[3] == 1:
            return render_template('admin/index_admin.html',data=data)
        else:
            return render_template('cliente/index_cliente_logueado.html', data=data)
    else:
        return render_template('index.html', data=data)

#========================== LOGIN  ===================================#
@app.route('/login')
def  login():
    return render_template('login/login.html')

#========================== Fin LOGIN  ===================================#

#=========================ABMC===========================#

#===========================
#         ROL
#===========================

@app.route('/rolABMC') 
def rolABMC():
    data =[]
    return render_template('rol/rolABMC.html', data=data)


#datos para tabla Rol "JSON"
@app.route('/rol_data_table')
def rol_data_table():
    rol = Rol()
    data = rol.formato_datos_tabla()
    return jsonify(data)


#Alta Rol 
@app.route('/altaRol')
def altaRol():
     return render_template('rol/altaRol.html') 


@app.route('/guardarRol', methods=["POST"])
def guardarRol():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombreRol']
        rol =  Rol()
        rol.set_nombreRol(nombre)
        verificador = rol.verificar_unico_rol()

        if verificador == []:
            rol.alta_rol() 
            data = "alta" 
        else:
            data = "ya_existe"

    return render_template('rol/rolABMC.html', data=data, verificador=verificador)  
#Fin Alta Rol


@app.route('/eliminarRol')
@app.route('/eliminarRol/<int:id_rol>')
def eliminarRol(id_rol=None):
    rol =  Rol()
    rol.set_id(id_rol)
    rol.baja_rol()
    data = "eliminado"
    return render_template('rol/RolABMC.html', data=data)    
#Fin Baja Rol


#Modificar Rol
@app.route('/modificarRol') 
@app.route('/modificarRol/<int:id_rol>') 
def modificarRol(id_rol=None):
    rol = Rol()
    rol.set_id(id_rol)
    rol_a_mod = rol.consultar_rol_por_id()
    return render_template('rol/modificarRol.html',data=rol_a_mod)  


@app.route('/editarRol', methods=["POST"])
def editarRol():
    data=[]
    if request.method == 'POST':
        nombre = request.form['nombreRol']
        nombreNuevo = request.form['nombreNuevoRol']
        rol = Rol()
        rol.set_nombreRol(nombre)
        data = rol.modificar_rol(nombreNuevo)     
    return render_template('rol/rolModificado.html', data=data)


# Listar Rol
@app.route('/listarRol')
def listarRol():
    rol = Rol()
    data = rol.listar_rol()
    return render_template('rol/listadoRol.html', data=data)
# Fin Listar Rol


@app.route('/verRol/<int:id>')
def verRol(id):
    rol = Rol()
    rol.set_id(id)
    data = rol.consultar_rol_por_id()
    return render_template('rol/listadoRol.html', data=data)

#===========FIN ROL


#===========================
#       ABM usuario
#===========================
@app.route('/usuarioABMC') 
def usuarioABMC():
    data =[]
    return render_template('usuario/usuarioABMC.html', data=data)


#datos para tabla Usuario "JSON"
@app.route('/usuario_data_table')
def usuario_data_table():
    usuario = Usuario()
    data = usuario.formato_datos_tabla()
    return jsonify(data)


@app.route('/altaUsuario')
def altaUsuario():
    #  return render_template('usuario/altaUsuario.html') 
    return render_template('usuario/crearUsuario.html') 


@app.route('/guardarUsuario', methods=["POST"])
def guardarUsuario():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombreUsuario']
        contrasenia = request.form['contrasenia']
        contrasenia_confirmacion = request.form['contrasenia_confirmacion']
        contacto = request.form['contacto']

        if contrasenia != contrasenia_confirmacion:
            return render_template('usuario/contrasenias_no_coinciden.html', nombre=nombre, contacto=contacto)
        else:
            usuario = Usuario()
            usuario.set_nombre(nombre)
            usuario.set_contrasenia(contrasenia)
            usuario.set_contacto(contacto)

            verificador = usuario.verificar_unico_usuario()  

            if verificador == []:
                data = usuario.alta_usuario() 
            return render_template('usuario/usuarioGuardado.html', data=data, verificador=verificador) 

"""
@app.route('/bajaUsuario') 
def bajaUsuario():
    return render_template('usuario/bajaUsuario.html')  
"""


@app.route('/eliminarUsuario')
@app.route('/eliminarUsuario/<email>')
def eliminarUsuario(email=None):
    usuario = Usuario()
    usuario.set_nombre(email)
    usuario.baja_usuario()
    data = "eliminado"
    return render_template('usuario/usuarioABMC.html', data=data)    


@app.route('/modificarUsuario') 
@app.route('/modificarUsuario/<email>') 
def modificarUsuario(email=None):
    data = {}
    usuario = Usuario()
    usuario.set_nombre(email)#La app usa el email como nombre de usuario 
    uAux = usuario.consultar_usuario_por_nombre()
    
    rol = Rol()
    rol.listar_rol()

    data['email'] = email
    data['roles'] = rol.listar_rol()
    data['rolUsario'] = uAux[3]
    data['Contacto'] = uAux[2]

    return render_template('usuario/modificarUsuario.html', data=data)  


@app.route('/editarUsuario', methods=["POST"])
def editarUsuario():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']      
        contraseniaNueva = request.form['contraseniaNueva']
        contactoNuevo = request.form['contactoNuevo'] 
        RolNuevo = request.form['NuevoRol']  

        usuario = Usuario()
        usuario.set_nombre(nombre)    
        usuario.modificar_usuario(contraseniaNueva, contactoNuevo, RolNuevo)

    return render_template('usuario/usuarioModificado.html', data=data)


@app.route('/listarUsuario')
def listarUsuario():
    data = []
    usuario = Usuario()
    data = usuario.consultar_usuarios() 
    return render_template('usuario/listadoUsuario.html', data=data)   
    

#====================
# ABM tipoProducto
#====================

@app.route('/tipoProductoABMC') 
def tipoProductoABMC():
    data =[]
    return render_template('tipoProducto/tipoProductoABMC.html', data=data)


#datos para tabla Tipo de Producto "JSON"
@app.route('/tipo_de_producto_data_table')
def tipo_de_producto_data_table():
    tp = TipoProducto()
    data = tp.formato_datos_tabla()
    return jsonify(data)   


@app.route('/altaTipoProducto')
def altaTipoProducto():
     return render_template('tipoProducto/altaTipoProducto.html') 


@app.route('/guardarTipoProducto', methods=["POST"])
def guardarTipoProducto():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_producto = TipoProducto()
        tipo_producto.set_nombre_tipo(nombre)
        verificador = tipo_producto.verificar_unico_tipo_producto()

        if verificador == []: 
            tipo_producto.alta_tipo_producto()   
            data = "alta"
        else:
            data = "ya_existe"

    return render_template('tipoProducto/tipoProductoABMC.html', data=data, verificador=verificador)  


@app.route('/eliminarTipoProducto')
@app.route('/eliminarTipoProducto/<int:id>')
def eliminarTipoProducto(id=None):
    data = []
    tipo_producto = TipoProducto()        
    tipo_producto.set_id(id)
    tipo_producto.baja_tipo_producto()
    data = "eliminado"

    return render_template('tipoProducto/tipoProductoABMC.html', data=data)    


@app.route('/modificarTipoProducto') 
@app.route('/modificarTipoProducto/<int:id>')
def modificarTipoProducto(id=None):
    data = []
    tp = TipoProducto()
    tp.set_id(id)
    data = tp.consultar_tipo_producto_por_id()
    return render_template('tipoProducto/modificarTipoProducto.html', data=data)  


@app.route('/editarTipoProducto', methods=["POST"])
def editarTipoProducto():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        nombreNuevo = request.form['nombreNuevo']
        tipo_producto = TipoProducto()
        tipo_producto.set_nombre_tipo(nombre)
        result = tipo_producto.modificar_tipo_producto(nombreNuevo)

        if result == 1:
            data = "modificado"
        else:
            data = "no_modificado"

    return render_template('tipoProducto/tipoProductoABMC.html', data=data)


@app.route('/listarTipoProducto') #### CATEGORIAS DE PRODUCTOS
def listarTipoProducto():
    tipo_producto = TipoProducto()
    data = tipo_producto.consultar_tipo_producto()
    return render_template('tipoProducto/listadoTipoProducto.html', data=data)


@app.route('/listarCategorias', methods=["POST"])
def listarCategorias():
    if request.method == 'POST':
        tipoProducto = request.form['tipoProducto']

    data = []
    producto = Producto()
    data = producto.consultar_producto_por_tipo(tipoProducto)

    #cuenta los elementos del data
    contador = 0
    for e in data:
        contador = contador+1
    #agrega el stock y las imágenes de cada producto
    for e in range(contador):
        #guarda el stock del producto en la posición 8 del data
        ejemplar = Ejemplar()
        cantidad = ejemplar.cantidad_ejemplares_de_un_producto(data[e][0])
        data[e] += (cantidad[0][0],)

        #guarda la primer imagen del producto en la posición 9 del data
        imagenes = Imagenes()
        imgs = imagenes.imagenes_producto(data[e][0])
        #Si no tiene imagen deja el campo vacio
        if imgs == []:
            data[e] += ()
        #Sino guarda la primer imagen
        else:
            data[e] += (imgs[0])


    ## Verifica si hay algún usuario logueado para dirigirlo a la vista correspondiente
    if 'email' in session:
        return render_template('producto/productosPorCategoria.html', data=data, categoria=tipoProducto)
    else:
        return render_template('producto/productosPorCategoria-nolog.html', data=data, categoria=tipoProducto)


#====================
# ABM Marca
#====================
@app.route('/marcaABMC') 
def marcaABMC():
    data =[]
    return render_template('marca/marcaABMC.html', data=data)


#datos para Marca "JSON"
@app.route('/marca_data_table')
def marca_data_table():
    tp = Marca()
    data = tp.formato_datos_tabla()
    return jsonify(data)   


@app.route('/altaMarca')
def altaMarca():
     return render_template('marca/altaMarca.html') 


@app.route('/guardarMarca', methods=["POST"])
def guardarMarca():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = Marca()
        marca.set_nombre(nombre)
        verificador = marca.verificar_unica_marca() 
        if verificador == []: 
            marca.alta_marca()   
            data = "alta"
        else:
            data = "ya_existe"  
    return render_template('marca/marcaABMC.html', data=data, verificador=verificador)  


@app.route('/eliminarMarca')
@app.route('/eliminarMarca/<int:id>')
def eliminarMarca(id=None):
    data = []   
    marca = Marca()
    marca.set_id(id)
    data = marca.baja_marca()
    data = "eliminado"
    return render_template('marca/marcaABMC.html', data=data)    


@app.route('/modificarMarca') 
@app.route('/modificarMarca/<int:id>')
def modificarMarca(id=None):
    marca = Marca()
    marca.set_id(id)
    data = marca.consultar_marca()
    return render_template('marca/modificarMarca.html', data=data)  


@app.route('/editarMarca', methods=["POST"])
def editarMarca():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        nombreNuevo = request.form['nombreNuevo']

        marca = Marca()
        marca.set_nombre(nombre)
        result = marca.modificar_marca(nombreNuevo)
        if result == 1:
            data = "modificado"
        else:
            data = "no_modificado"
    return render_template('marca/marcaABMC.html', data=data)


@app.route('/listarMarca')
def listarMarca():
    data = []
    marca = Marca()
    data = marca.consultar_marca()
    return render_template('marca/listadoMarca.html', data=data)


@app.route('/listadoMarcas') #### Busqueda de productos por marca
def listadoMarcas():
    marca = Marca()
    data = marca.listar_marca()
    return render_template('marca/listadoMarca.html', data=data)


@app.route('/productosPorMarca', methods=["POST"])
def productosPorMarca():
    if request.method == 'POST':
        marca = request.form['marca']

    data = []
    producto = Producto()
    data = producto.consultar_producto_por_marca(marca)

    #cuenta los elementos del data
    contador = 0
    for e in data:
        contador = contador+1
    #agrega el stock y las imágenes de cada producto
    for e in range(contador):
        #guarda el stock del producto en la posición 8 del data
        ejemplar = Ejemplar()
        cantidad = ejemplar.cantidad_ejemplares_de_un_producto(data[e][0])
        data[e] += (cantidad[0][0],)

        #guarda la primer imagen del producto en la posición 9 del data
        imagenes = Imagenes()
        imgs = imagenes.imagenes_producto(data[e][0])
        #Si no tiene imagen deja el campo vacio
        if imgs == []:
            data[e] += ()
        #Sino guarda la primer imagen
        else:
            data[e] += (imgs[0])

    ## Verifica si hay algún usuario logueado para dirigirlo a la vista correspondiente
    if 'email' in session:
        return render_template('producto/productosPorMarca.html', data=data, marca=marca)
    else:
        return render_template('producto/productosPorMarca-nolog.html', data=data, marca=marca)



#==================
# ABMC PRODUCTO
#==================

@app.route('/productoABMC') 
def productoABMC():
    data =[]
    return render_template('producto/productoABMC.html', data=data)


@app.route('/producto_data_table')
def producto_data_table():
    producto = Producto()
    data = producto.formato_datos_tabla()
    return jsonify(data)    


@app.route('/altaProducto')
def altaProducto():
    data = {}
    tp = TipoProducto()
    data['TipoProducto'] = tp.consultar_tipo_producto()
    marca = Marca()
    data['marca'] = marca.listar_marca()
    return render_template('producto/altaProducto.html', data=data) 


@app.route('/guardarProducto', methods=["POST"])
def guardarProducto():
    data = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion'] 
        precio = request.form['precio']
        modelo = request.form['modelo']
        garantia = request.form['garantia']
        tipo_producto = request.form['tipoProducto']
        marca = request.form['marca'] 

        producto = Producto()
        producto.set_nombre(nombre)
        producto.set_descripcion(descripcion)
        producto.set_precio(precio)
        producto.set_modelo(modelo)
        producto.set_garantia(garantia)
        producto.set_tipo_producto(tipo_producto)
        producto.set_marca(marca)

        verificador = producto.verificar_unico_producto()
 
        if verificador == []:
            data = producto.alta_producto()
            data="alta"
        else:
            data="ya_existe"

    producto = Producto()
    idProducto = producto.buscarIdProducto(nombre)
    imagenes=[]
    if request.method == 'POST':
        for imagen in request.files.getlist('imagenes'):
            imagenes.append(imagen)
    guardarImagen(imagenes, idProducto[0][0])

    return render_template('producto/productoABMC.html', data=data)  

@app.route('/eliminarProducto')
@app.route('/eliminarProducto/<int:id>')
def eliminarProducto(id=None):    
    producto = Producto()
    producto.set_id(id)  
    producto.baja_producto() 
    data = "eliminado"
    return render_template('producto/productoABMC.html', data=data)    


@app.route('/modificarProducto') 
@app.route('/modificarProducto/<int:id>') 
def modificarProducto(id=None):
    print(id)
    id=int(id)
    data = {}
    producto = Producto()
    producto.set_id(id)
    data['producto'] = producto.consultar_producto_por_id()
    tipo_prod = TipoProducto()
    data['tipo_producto'] = tipo_prod.consultar_tipo_producto()
    marca = Marca()
    data['marca'] = marca.listar_marca()

    return render_template('producto/modificarProducto.html', data=data)  


@app.route('/editarProducto', methods=["POST"])
def editarProducto():
    if request.method == 'POST':
        idProd = request.form['idProd']
        nuevoNombre = request.form['nuevoNombre']
        nuevaDescripcion = request.form['nuevaDescripcion']
        nuevoPrecio = request.form['nuevoPrecio']
        nuevoModelo = request.form['nuevoModelo']
        nuevaGarantia = request.form['nuevaGarantia']
        nuevoTipoProducto = request.form['nuevoTipoProducto']
        nuevaMarca = request.form['nuevaMarca']
        
        producto = Producto()
        producto.set_id(idProd)
        data = producto.modificar_producto(nuevoNombre, 
                                            nuevaDescripcion,
                                            nuevoPrecio,
                                            nuevoModelo,
                                            nuevaGarantia,
                                            nuevoTipoProducto,
                                            nuevaMarca)     
    return render_template('producto/productoModificado.html', data=data)

@app.route('/fichaProducto')
@app.route('/fichaProducto/<int:id>')
@app.route('/fichaProducto', methods=["POST"])
def fichaProducto(id=None):
    if request.method == 'POST':
        id = request.form['id']
    data = {}
    producto = Producto()
    producto.set_id(id)
    data = producto.consultar_producto_por_id()
    ejemplar = Ejemplar()
    # Consulta el stock
    cantidad = ejemplar.cantidad_ejemplares_de_un_producto(id)
    # Busca las imagenes del producto
    imagenes = Imagenes()
    imgs = imagenes.imagenes_producto(id)
    cantidadImagenes = imagenes.obtener_cantidad_imagenes(id)
    cantidadImagenes=cantidadImagenes[0][0]
    return render_template('producto/fichaProducto.html', data = data, stock = cantidad, fotos = imgs, cantidadFotos = cantidadImagenes)


@app.route('/listarProductos')
def listarProductos():
    data = {}
    producto = Producto()
    data['productos'] = producto.listar_productos()
    cant = producto.obtener_cantidad_productos()
    for e in cant:
        cantidad = e[0]
    cantidad=int(cantidad)
    return render_template('producto/productos.html', data=data, cantidad=cantidad)

## Vista del usuario
@app.route('/verProducto')
@app.route('/verProducto/<int:id>')
def verProducto(id=None):
    if request.method == 'POST':
        id = request.form['id']
    # Trae los datos del producto
    data = {}
    producto = Producto()
    producto.set_id(id)
    data = producto.consultar_producto_por_id()
    # Trae el stock
    ejemplar = Ejemplar()
    cantidadEjemplares = ejemplar.cantidad_ejemplares_de_un_producto(id)
    # Busca las imagenes del producto
    imagenes = Imagenes()
    imgs = imagenes.imagenes_producto(id)
    cantidadImagenes = imagenes.obtener_cantidad_imagenes(id)
    cantidadImagenes=cantidadImagenes[0][0]
    return render_template('producto/verProducto.html', data = data, stock = cantidadEjemplares, fotos = imgs, cantidadFotos = cantidadImagenes)

@app.route('/buscarProducto', methods=["POST"])
def buscarProducto():
    if request.method == 'POST':
        palabra = request.form['palabra']
    data = {}
    producto = Producto()
    data = producto.buscarProductos(palabra)
    return render_template('index.html', data=data)

#ver producto viejo
# @app.route('/verProducto')
# @app.route('/verProducto/<int:id>')
# def verProducto(id=None):
#     data = {}
#     producto = Producto()
#     producto.set_id(id)
#     data = producto.consultar_producto_por_id()
#     return render_template('producto/verProducto.html', data = data)



#==================
# ABMC EJEMPLAR
#==================
@app.route('/altaEjemplar')
@app.route('/altaEjemplar/<int:id_prod>')
def altaEjemplar(id_prod=None):
    data = {}
    prod = Producto()
    data['lista_productos'] = prod.listar_productos()
    data['id_prod'] = id_prod
    return render_template('ejemplar/altaEjemplar.html', data=data) 


@app.route('/guardarEjemplar', methods=["POST"])
def guardarEjemplar():
    data, verificador = [], []

    if request.method == 'POST':
        numeroSerie = request.form['numeroSerie']
        vendido = request.form['vendido'] 
        producto = request.form['producto']

        ejemplar = Ejemplar()
        ejemplar.set_numero_serie(numeroSerie)
        ejemplar.set_vendido(vendido)
        ejemplar.set_producto(producto)
        
        verificador = ejemplar.verificar_ejemplar()
 
        if verificador == []:
            data = ejemplar.alta_ejemplar()            
    return render_template('ejemplar/ejemplarGuardado.html', data=data, verificador=verificador)  


@app.route('/bajaEjemplar') 
def bajaEjemplar():
    return render_template('ejemplar/bajaEjemplar.html')  


@app.route('/eliminarEjemplar', methods=["POST"])
def eliminarEjemplar():
    if request.method == 'POST':
        numeroSerie = request.form['numeroSerie']
        ejemplar = Ejemplar()
        ejemplar.set_numero_serie(numeroSerie)
        data = ejemplar.baja_ejemplar()
    return render_template('ejemplar/ejemplarEliminado.html', data=data)    


@app.route('/modificarEjemplar') 
def modificarEjemplar():
    return render_template('ejemplar/modificarEjemplar.html')  


@app.route('/editarEjemplar', methods=["POST"])
def editarEjemplar():
    if request.method == 'POST':
        numeroSerie = request.form['numeroSerie']
        nuevoNumeroSerie = request.form['nuevoNumeroSerie']
        nuevoVendido = request.form['nuevoVendido']
        nuevoProducto = request.form['nuevoProducto']
        
        ejemplar = Ejemplar()
        ejemplar.set_numero_serie(numeroSerie)
        data = ejemplar.modificar_ejemplar(nuevoNumeroSerie, nuevoVendido, nuevoProducto )

    return render_template('ejemplar/ejemplarModificado.html', data=data)


@app.route('/listarEjemplar')
def listarEjemplar():
    data = []
    ejemplar = Ejemplar()
    data = ejemplar.consultar_ejemplar()
    return render_template('ejemplar/listadoEjemplar.html', data=data)


#====COMBO
@app.route('/comboABMC') 
def comboABMC():
    data =[]
    return render_template('combo/comboABMC.html', data=data)


#datos para tabla Combo "JSON"
@app.route('/combo_data_table')
def combo_data_table():
    combo = Combo()
    data = combo.formato_datos_tabla()
    return jsonify(data)


#datos para tabla Emplares del Combo "JSON"
@app.route('/productos_combo_data_table')
@app.route('/productos_combo_data_table/<int:idCombo>')
def productos_combo_data_table(idCombo=None):
    combo = Combo()
    data = combo.formato_datos_tabla_productos(idCombo)
    return jsonify(data)


@app.route('/altaCombo')
def altaCombo():
     return render_template('combo/altaCombo.html') 


@app.route('/guardarCombo', methods=["POST"])
def guardarCombo():
    dato = {}
    data, verificador = [], []
    if request.method == 'POST':
        nombre = request.form['nombre']

        combo = Combo()
        combo.set_nombre(nombre)
        combo.set_total(0)
        combo.set_descuento(0)
        combo.set_totalConDescuento(0)
        combo.set_vendido(False)
        verificador = combo.verificar_combo() 
        if verificador == []:
            data = combo.alta_combo()  

        producto = Producto()
        producto.listar_productos()

        dato['productos'] = producto.listar_productos()
        dato['nombreCombo'] = combo.get_nombre()
        dato['total'] = combo.get_total()
        dato['descuento'] = combo.get_descuento()
        dato['totalConDescuento'] = combo.get_totalConDescuento()
        dato['vendido'] = combo.get_vendido()
        ListaCombos = combo.listar_combos()
        for e in ListaCombos:
            id= e[0]

    return render_template('combo/cargarProductosalCombo.html', dato=dato,id=id)  
    

@app.route('/verCombo')
@app.route('/verCombo/<int:id>')
def verCombo(id):
    combo = Combo()
    combo.set_id(id)
    data = combo.consultar_combo_por_id()

    dato = {}
    dato['nombreCombo'] = data[0][1]
    dato['idCombo'] = data[0][0]
    dato['descuento']  = data[0][3] 
    dato['total']  = data[0][2]
    dato['totalConDescuento']  = data[0][4]
    id=data[0][0]

    producto = Producto()
    producto.listar_productos()

    dato['productos'] = producto.listar_productos()

    return render_template('combo/cargarProductosAlCombo.html', dato=dato, id=id)


@app.route('/mostrarComboAlUsuario')
@app.route('/mostrarComboAlUsuario', methods=["POST"])
def mostrarComboAlUsuario():
    if request.method == 'POST':
        id  = request.form['id']
    combo = Combo()
    combo.set_id(id)
    data = combo.consultar_combo_por_id()

    dato = {}
    dato['nombreCombo'] = data[0][1]
    dato['idCombo'] = data[0][0]
    dato['descuento']  = data[0][3] 
    dato['total']  = data[0][2]
    dato['totalConDescuento']  = data[0][4]
    id=data[0][0]

    producto = Producto()
    producto.listar_productos()

    dato['productos'] = producto.listar_productos()

    return render_template('combo/mostrarComboAlUsuario.html', dato=dato, id=id)


@app.route('/cargarProductos')
@app.route('/cargarProductos', methods=["POST"])
@app.route('/verCombo/cargarProductos', methods=["POST"])
# @app.route('/cargarProductos/<int:id>')
def cargarProductos():
    data = {}
    if request.method == 'POST':
        data['nombreCombo']  = request.form['nombreCombo']      
        data['idCombo'] = request.form['idCombo']
        data['producto'] = request.form['producto']
        data['descuento'] = request.form['descuento']
        total = request.form['total']
        data['totalConDescuento'] = request.form['totalConDescuento']

    producto = Producto()
    p = producto.obtener_precio(data['producto'])
    for e in p: 
        precio = e[0] 
    precio =int(precio)
    total = float(total)
    data['total'] = total + precio

    combo = Combo()
    combo.cambiar_precio((data['idCombo']), (data['total']))
    
    ejemplar = Ejemplar()

    data['ejemplares'] = ejemplar.ejemplares_de_un_producto(data['producto'])

    return render_template('combo/cargarEjemplaresAlCombo.html', data=data)


@app.route('/cargarEjemplaresAlCombo', methods=["POST"])
@app.route('/verCombo/cargarEjemplaresAlCombo', methods=["POST"])
def cargarEjemplaresAlCombo():
    dato = {}
    data = []
    if request.method == 'POST':
        dato['nombreCombo']  = request.form['nombreCombo']      
        dato['idCombo'] = request.form['idCombo']
        dato['idProducto'] = request.form['idProducto']
        dato['ejemplar'] = request.form['ejemplar']
        dato['total'] = request.form['total']
        dato['descuento'] = request.form['descuento']
        dato['totalConDescuento'] = request.form['totalConDescuento']
        id=request.form['idCombo']

    ejemplacombo = Ejemplar_combo()
    ejemplacombo.set_idCombo(dato['idCombo'])
    ejemplacombo.set_numero_serie(dato['ejemplar'])
    data = ejemplacombo.alta_ejemplar_combo()

    producto = Producto()
    producto.listar_productos()
    dato['productos'] = producto.listar_productos()

    total = float(dato['total'])   
    desc = float(dato['descuento'])
    importeDescuento = ((total * desc)/100)
    totalConDesc = total - importeDescuento
    dato['totalConDescuento'] = totalConDesc

    return render_template('combo/cargarProductosalCombo.html',data=data, dato=dato, id=id)


@app.route('/cargarDescuentoAlCombo', methods=["POST"])
@app.route('/verCombo/cargarDescuentoAlCombo', methods=["POST"])
def cargarDescuento():
    dato = {}
    if request.method == 'POST':
        dato['nombreCombo'] = request.form['nombreCombo']
        dato['idCombo'] = request.form['idCombo']
        dato['descuento']  = request.form['descuento'] 
        dato['total']  = request.form['total']
        dato['totalConDescuento']  = request.form['totalConDescuento']
        id=request.form['idCombo']

    total = float(dato['total'])   
    desc = float(dato['descuento'])
    importeDescuento = ((total * desc)/100)
    totalConDesc = total - importeDescuento

    combo = Combo()
    combo.aplicarDescuento(dato['idCombo'], totalConDesc, dato['descuento'])

    dato['totalConDescuento']  = totalConDesc

    producto = Producto()
    producto.listar_productos()
    dato['productos'] = producto.listar_productos()


    return render_template('combo/cargarProductosalCombo.html', dato=dato, id=id)    


@app.route('/bajaCombo') 
def bajaCombo():
    return render_template('combo/bajaCombo.html')  


@app.route('/eliminarCombo')
@app.route('/eliminarCombo/<int:id_combo>')
def eliminarCombo(id_combo=None):
    ejemplar_combo = Ejemplar_combo()
    ejemplar_combo.set_idCombo(id_combo)
    ejemplar_combo.eliminar_ejemplares_combo()
    combo =  Combo()
    combo.set_id(id_combo)
    combo.baja_combo()
    data = "eliminado"
    return render_template('combo/comboABMC.html', data=data) 


@app.route('/modificarCombo') 
@app.route('/modificarCombo/<int:id>') 
def modificarCombo(id=None):
    combo = Combo()
    combo.set_id(id)
    data = combo.consultar_combo_por_id()
    return render_template('combo/modificarCombo.html',data=data, id=id)  


@app.route('/editarCombo', methods=["POST"])
def editarCombo():
    data=[]
    if request.method == 'POST':
        id = request.form['id']
        print(id)
        nombre = request.form['nombre']
        nombreNuevo = request.form['nombreNuevo']
        combo = Combo()
        combo.set_id(id)
        data = combo.modificar_combo(nombreNuevo)     
    return render_template('combo/comboModificado.html', data=data)


@app.route('/ejemplar_data_table')
def ejemplar_data_table():
    ejemplar = Ejemplar()
    data = ejemplar.formato_datos_tabla()
    return jsonify(data)


@app.route('/listarCombo')
def listarCombo():
    combo = Combo()
    data = combo.listar_combos()
    ## Verifica si hay algún usuario logueado para dirigirlo a la vista correspondiente
    if 'email' in session:
        return render_template('combo/listadoCombo.html', data=data)
    else:
        return render_template('combo/listadoCombo-nolog.html', data=data)
    


#======== ejemplar_combo
@app.route('/altaEjemplar_combo')
def altaEjemplar_combo():
     return render_template('ejemplar_combo/altaEjemplar_combo.html') 


@app.route('/guardarEjemplar_combo', methods=["POST"])
def guardarEjemplar_combo():
    data = []
    if request.method == 'POST':
        idCombo = request.form['idCombo']
        numeroSerie = request.form['numeroSerie']
        data = db.queryInsert('''
            INSERT INTO "ejemplar_combo" ("idCombo", "numeroSerie") values ('{}', '{}');
            '''.format(idCombo, numeroSerie)) 
    # Se marca el ejemplar como vendido
    ejemplar = Ejemplar()
    ejemplar.marcar_ejemplar_vendido(numeroSerie)
    return render_template('index.html')   


@app.route('/modificarEjemplar_combo') 
def modificarEjemplar_combo():
    return render_template('ejemplar_combo/modificarEjemplar_combo.html')  


@app.route('/editarEjemplar_combo', methods=["POST"])
def editarEjemplar_combo():
    data = []
    if request.method == 'POST':
        idCombo = request.form['idCombo']
        numeroSerie = request.form['numeroSerie']
        nuevoIdCombo = request.form['nuevoIdCombo']
        nuevoNumeroSerie = request.form['nuevoNumeroSerie']  
        data = db.queryInsert('''
               UPDATE "ejemplar_combo"
	                SET "idCombo" = '{}', "numeroSerie" = '{}'
	                WHERE "idCombo" = '{}' AND "numeroSerie" = '{}';
            '''.format(nuevoIdCombo, nuevoNumeroSerie, idCombo, numeroSerie))
    return render_template('index.html')


@app.route('/listarEjemplar_combo')
def listarEjemplar_combo():
    data = db.querySelect('''
                SELECT * FROM "ejemplar_combo";
            ''')
    return render_template('ejemplar_combo/listadoEjemplar_combo.html', data=data) 


@app.route('/eliminarEjemplar_combo')
@app.route('/eliminarEjemplar_combo/<string:numeroSerie>/<int:idCombo>')
def eliminarEjemplar_combo(numeroSerie, idCombo):
    combo = Combo()
    combo.set_id(idCombo)
    total = combo.consultar_precio_combo()
    total = total[0][0]
    ejemplar = Ejemplar()
    ejemplar.set_numero_serie(numeroSerie)

    # Marcamos el ejemplar como disponible
    ejemplar.marcar_ejemplar_disponible(numeroSerie)

    precioDelProducto = ejemplar.precioDelEjemplar()
    precioDelProducto = precioDelProducto[0][0]
    nuevoTotal = (int(total) - int(precioDelProducto))
    combo.cambiar_total(nuevoTotal)

    ejemplar_combo = Ejemplar_combo()
    ejemplar_combo.set_idCombo(idCombo)
    ejemplar_combo.set_numero_serie(numeroSerie)
    ejemplar_combo.baja_ejemplar_combo()

    nuevoTotal = float(nuevoTotal)   
    desc = combo.consultar_descuento_combo()
    desc = float(desc[0][0])
    importeDescuento = ((nuevoTotal * desc)/100)
    totalConDesc = nuevoTotal - importeDescuento
    print(nuevoTotal)
    print(desc)
    print(totalConDesc)
    combo.actualizarDescuento(totalConDesc)

    data = combo.consultar_combo_por_id()
    dato = {}
    dato['nombreCombo'] = data[0][1]
    dato['idCombo'] = data[0][0]
    dato['descuento']  = data[0][3] 
    dato['total']  = data[0][2]
    dato['totalConDescuento']  = data[0][4]
    id=data[0][0]

    producto = Producto()
    producto.listar_productos()

    dato['productos'] = producto.listar_productos()

    return render_template('combo/cargarProductosAlCombo.html', dato=dato, id=id)
    
    
#====CARRITO

## No se usaria
""" @app.route('/altaCarrito')
def altaCarrito():
     return render_template('carrito/altaCarrito.html')  """

@app.route('/agregarAlCarrito', methods=["POST"])
def agregarAlCarrito():
    if request.method == 'POST':
        id = request.form['id']
    ejemplar = Ejemplar()
    ## Chequea si hay ejemplares disponibles
    cantidad = ejemplar.cantidad_ejemplares_de_un_producto(id)
    if cantidad[0][0]==0:
        return render_template('producto/sinStock.html')
    else:
        # Chequea si el usuario tiene un carrito activo (con productos)
        carrito = Carrito()
        datosCarrito = carrito.carrito_actual(session['email'])
        if (datosCarrito == []):
            # Si no hay carrito evalúa si tiene una compra pendiente de pago
            compra = Compra()
            datosCompra = compra.compra_pendiente_pago(session['email'])
            # Si no hay compra pendiente de pago crea un carrito nuevo
            if (datosCompra == []):
                nuevoCarrito = Carrito()
                nuevoCarrito.set_usuario(session['email'])
                data = nuevoCarrito.alta_carrito()
                # Obtenemos los datos de nuevo carrito
                datosCarrito = carrito.carrito_actual(session['email'])
                id_carrito = datosCarrito[0][0]
                # Obtenemos un ejemplar disponible
                ejempleares_disponibles = ejemplar.seleccionarEjemplares(id)
                for ej in ejempleares_disponibles:
                    # obtiene el numero de serie
                    ejemplar_seleccionado = ej[0]
                    break 
                # Carga el ejemplar_carrito
                ejemplar_carrito = Ejemplar_carrito()
                ejemplar_carrito.set_idCarrito(id_carrito)
                ejemplar_carrito.set_numero_serie(ejemplar_seleccionado)
                data = ejemplar_carrito.alta_ejemplar_carrito()
                # Se marca el ejemplar como vendido
                ejemplar_vendido = Ejemplar()
                ejemplar_vendido.marcar_ejemplar_vendido(ejemplar_seleccionado)
                # Se suma el importe del producto al total del carrito
                # Precio del ejemplar
                precio_ejemplar = ejemplar.precio_ejemplar(ejemplar_seleccionado)
                precio_ejemplar = precio_ejemplar[0][4]
                # Total del carrito actual antes de agregarle el producto
                total = carrito.carrito_actual(session['email'])
                total = total[0][1]
                nuevo_total = int(precio_ejemplar) + int(total)
                carritoActualizado = Carrito()
                carritoActualizado.actualizar_total_carrito(nuevo_total, id_carrito)
            # Si hay compra pendiente de pago no crea un carrito nuevo
            else:
                idCompra = datosCompra[0][0]
                totalCompra = datosCompra[0][2]
                idCarrito = datosCompra[0][1]
                return render_template('carrito/compra_pendiente_pago.html', total=totalCompra, idCarrito=idCarrito, idCompra = idCompra)
        else:
            # Si hay carrito activo, le agrega el ejemplar del producto
            # obtenemos el id del carrito
            id_carrito = datosCarrito[0][0]
            # Selecciona un ejemplar
            ejempleares_disponibles = ejemplar.seleccionarEjemplares(id)
            for ej in ejempleares_disponibles:
                # obtiene el numero de serie
                ejemplar_seleccionado = ej[0]
                break 
            # Carga el ejemplar_carrito
            ejemplar_carrito = Ejemplar_carrito()
            ejemplar_carrito.set_idCarrito(id_carrito)
            ejemplar_carrito.set_numero_serie(ejemplar_seleccionado)
            data = ejemplar_carrito.alta_ejemplar_carrito()
            # Se marca el ejemplar como vendido
            ejemplar_vendido = Ejemplar()
            ejemplar_vendido.marcar_ejemplar_vendido(ejemplar_seleccionado)
            # Se suma el importe del producto al total del carrito
            # Precio del ejemplar
            precio_ejemplar = ejemplar.precio_ejemplar(ejemplar_seleccionado)
            precio_ejemplar = precio_ejemplar[0][4]
            # Total del carrito actual antes de agregarle el producto
            total = carrito.carrito_actual(session['email'])
            total = total[0][1]
            nuevo_total = int(precio_ejemplar) + int(total)
            carritoActualizado = Carrito()
            carritoActualizado.actualizar_total_carrito(nuevo_total, id_carrito)
        
        # Traemos los datos actualiados del carrito para pasar a la vista
        data = []
        carritoCargado = Carrito()
        # Obtenemos los datos del carrito actual
        datos_carrito = carritoCargado.carrito_actual(session['email'])
        # Seleccionamos el id del carrito y el total
        id_carrito = datos_carrito[0][0]
        total = datos_carrito[0][1]
        ejemplaresCarrito = Ejemplar_carrito()
        # Traemos los ejemplares del carrito
        data = ejemplaresCarrito.ejemplares_de_un_carrito(id_carrito)
        return render_template('carrito/mostrarCarrito.html', data=data, total=total, idCarrito=id_carrito)


@app.route('/agregarComboAlCarrito', methods=["POST"])
def agregarComboAlCarrito():
    if request.method == 'POST':
        idCombo= request.form['id']

        # Chequea si el usuario tiene un carrito activo (con productos)
        carrito = Carrito()
        datosCarrito = carrito.carrito_actual(session['email'])
        if (datosCarrito == []):
            # Si no hay carrito evalúa si tiene una compra pendiente de pago
            compra = Compra()
            datosCompra = compra.compra_pendiente_pago(session['email'])
            # Si no hay compra pendiente de pago crea un carrito nuevo
            if (datosCompra == []):
                nuevoCarrito = Carrito()
                nuevoCarrito.set_usuario(session['email'])
                data = nuevoCarrito.alta_carrito()
                # Obtenemos los datos de nuevo carrito
                datosCarrito = carrito.carrito_actual(session['email'])
                id_carrito = datosCarrito[0][0]
                # Carga el combo_carrito
                combo_carrito = Combo_carrito()
                combo_carrito.set_idCarrito(id_carrito)
                combo_carrito.set_idCombo(idCombo)
                data = combo_carrito.alta_combo_carrito()
                # Se marca el combo como vendido
                combo = Combo()
                combo.marcar_combo_vendido(idCombo)
                # Se suma el importe del combo al total del carrito
                # Precio del combo 
                precioCombo = combo.total_combo(idCombo)
                precioCombo = precioCombo[0][0]
                # Total del carrito actual antes de agregarle el producto
                total = carrito.carrito_actual(session['email'])
                total = total[0][1]
                nuevo_total = int(precioCombo) + int(total)
                carritoActualizado = Carrito()
                carritoActualizado.actualizar_total_carrito(nuevo_total, id_carrito)
            # Si hay compra pendiente de pago no crea un carrito nuevo
            else:
                idCompra = datosCompra[0][0]
                totalCompra = datosCompra[0][2]
                idCarrito = datosCompra[0][1]
                return render_template('carrito/compra_pendiente_pago.html', total=totalCompra, idCarrito=idCarrito, idCompra = idCompra)
        else:
            # Si hay carrito activo, le agrega el ejemplar del producto
            # obtenemos el id del carrito
            id_carrito = datosCarrito[0][0]
            # Carga el combo_carrito
            combo_carrito = Combo_carrito()
            combo_carrito.set_idCarrito(id_carrito)
            combo_carrito.set_idCombo(idCombo)
            data = combo_carrito.alta_combo_carrito()
            # Se marca el combo como vendido
            combo = Combo()
            combo.marcar_combo_vendido(idCombo)
            # Se suma el importe del combo al total del carrito
            # Precio del combo
            precioCombo = combo.total_combo(idCombo)
            precioCombo = precioCombo[0][0]
            # Total del carrito actual antes de agregarle el producto
            total = carrito.carrito_actual(session['email'])
            total = total[0][1]
            nuevo_total = int(precioCombo) + int(total)
            carritoActualizado = Carrito()
            carritoActualizado.actualizar_total_carrito(nuevo_total, id_carrito)
        
        # Traemos los datos actualiados del carrito para pasar a la vista
        ejempares_carrito = []
        carritoCargado = Carrito()
        # Obtenemos los datos del carrito actual
        datos_carrito = carritoCargado.carrito_actual(session['email'])
        # Seleccionamos el id del carrito y el total
        id_carrito = datos_carrito[0][0]
        total = datos_carrito[0][1]
        ejemplaresCarrito = Ejemplar_carrito()
        # Traemos los ejemplares del carrito
        ejemplares_carrito = ejemplaresCarrito.ejemplares_de_un_carrito(id_carrito)
        # Traemos los combos del carrito
        combos_carrito = []
        comboCarrito = Combo_carrito()
        combos_carrito = comboCarrito.combos_de_un_carrito(id_carrito)
        return render_template('carrito/mostrarCarrito.html', ejemplares=ejemplares_carrito, combos=combos_carrito,total=total, idCarrito=id_carrito)


@app.route('/mostrarCarrito')
def mostrarCarrito():
    ejempares_carrito = []
    carrito = Carrito()
    # Obtenemos los datos del carrito actual
    datos_carrito = carrito.carrito_actual(session['email'])
    #Si no hay carrito activo
    if (datos_carrito == []):
        ejempares_carrito = []
        total = 0
        id_carrito = []
        combos_carrito = []
    # Si hay carrito
    else:
        # Seleccionamos el id del carrito y el total
        id_carrito = datos_carrito[0][0]
        total = datos_carrito[0][1]
        ejemplar_carrito = Ejemplar_carrito()
        # Traemos los ejemplares del carrito
        ejempares_carrito = ejemplar_carrito.ejemplares_de_un_carrito(id_carrito)
        # Traemos los combos del carrito
        combos_carrito = []
        comboCarrito = Combo_carrito()
        combos_carrito = comboCarrito.combos_de_un_carrito(id_carrito)
    return render_template('carrito/mostrarCarrito.html', ejemplares=ejempares_carrito, combos=combos_carrito, total=total, idCarrito=id_carrito)


## No se usaria
""" @app.route('/guardarCarrito', methods=["POST"])
def guardarCarrito():
    data = []
    if request.method == 'POST':
        total = request.form['total']
        
        carrito = Carrito()
        carrito.set_total(total)
        data = carrito.alta_carrito()
    return render_template('carrito/carritoGuardado.html', data=data)


@app.route('/bajaCarrito') 
def bajaCarrito():
    return render_template('carrito/bajaCarrito.html')  


@app.route('/eliminarCarrito', methods=["POST"])
def eliminarCarrito():
    if request.method == 'POST':
        idCarrito = request.form['id']

        carrito = Carrito()
        carrito.set_id(idCarrito)
        data = carrito.baja_carrito()
    return render_template('carrito/carritoEliminado.html', data=data)    


@app.route('/modificarCarrito') 
def modificarCarrito():
    return render_template('carrito/modificarCarrito.html')  


@app.route('/editarCarrito', methods=["POST"])
def editarCarrito():
    data = []
    if request.method == 'POST':
        total = request.form['nuevoTotal']
        idCarrito = request.form['id']

        carrito = Carrito()
        carrito.set_id(idCarrito)
        data = carrito.modificar_carrito(total) 

    return render_template('carrito/carritoModificado.html', data=data)
 """



#======== ejemplar_carrito

# No se usaría
""" @app.route('/altaEjemplar_carrito')
def altaEjemplar_carrito():
     return render_template('ejemplar_carrito/altaEjemplar_carrito.html')  """

# No se usaria
""" @app.route('/guardarEjemplar_carrito', methods=["POST"])
def guardarEjemplar_carrito():
    data = []
    if request.method == 'POST':
        idCarrito= request.form['idCarrito']
        numeroSerie = request.form['numeroSerie']
        data = db.queryInsert('''
            INSERT INTO "ejemplar_carrito" ("idCarrito", "numeroSerie") values ('{}', '{}');
            '''.format(idCarrito, numeroSerie))  
    return render_template('index.html') """


### No se usaría
""" @app.route('/bajaEjemplar_carrito') 
def bajaEjemplar_carrito():
    return render_template('ejemplar_carrito/bajaEjemplar_carrito.html')  """ 


@app.route('/eliminarEjemplar_carrito', methods=["POST"])
def eliminarEjemplar_carrito():
    # Obtenemos los datos que vienen del formulario
    if request.method == 'POST':
        idCarrito = request.form['idCarrito']
        numeroSerie = request.form['numeroSerie']
        precioProducto = request.form['precioProducto']
        totalCarrito = request.form['totalCarrito']
    # Eliminamos el producto del carrito
    ejemplar_carrito = Ejemplar_carrito()
    ejemplar_carrito.set_idCarrito(idCarrito)
    ejemplar_carrito.set_numero_serie(numeroSerie)
    data = ejemplar_carrito.baja_ejemplar_carrito()
    # Marcamos el ejemplar como disponible para la venta
    ejemplar = Ejemplar()
    ejemplar.marcar_ejemplar_disponible(numeroSerie)
    # Descontamos el importe del producto al total carrito
    total = float(totalCarrito) - float(precioProducto)
    carrito = Carrito()
    carrito.actualizar_total_carrito(total, idCarrito)
    # Traemos los datos actualizados para refrescar la vista
    carritoActual = Carrito()
    datos_carrito = carritoActual.carrito_actual(session['email'])
    # Traemos los ejemplares del carrito
    ejemplaresCarrito = Ejemplar_carrito()
    ejempares_carrito = ejemplaresCarrito.ejemplares_de_un_carrito(idCarrito)
    # Traemos los combos del carrito
    combos_carrito = []
    comboCarrito = combo_carrito()
    combos_carrito = comboCarrito.combos_de_un_carrito(idCarrito)
    return render_template('carrito/mostrarCarrito.html', ejemplares=ejempares_carrito, combos=combos_carrito, total=total, idCarrito=id_carrito)

 
@app.route('/eliminarCombo_carrito', methods=["POST"])
def eliminarCombo_carrito():
    # Obtenemos los datos que vienen del formulario
    if request.method == 'POST':
        idCarrito = request.form['idCarrito']
        idCombo = request.form['idCombo']
        totalConDescuento = request.form['totalConDescuento']
        totalCarrito = request.form['totalCarrito']
    # Eliminamos el combo del carrito
    combo_carrito = Combo_carrito()
    combo_carrito.set_idCarrito(idCarrito)
    combo_carrito.set_idCombo(idCombo)
    combo_carrito.baja_combo_carrito()
    # Marcamos el combo como disponible para la venta
    combo = Combo()
    combo.marcar_combo_disponible(idCombo)
    # Descontamos el importe del combo al total carrito
    total = float(totalCarrito) - float(totalConDescuento)
    carrito = Carrito()
    carrito.actualizar_total_carrito(total, idCarrito)
    # Traemos los datos actualizados para refrescar la vista
    carritoActual = Carrito()
    datos_carrito = carritoActual.carrito_actual(session['email'])
    # Traemos los ejemplares del carrito
    ejemplaresCarrito = Ejemplar_carrito()
    ejempares_carrito = ejemplaresCarrito.ejemplares_de_un_carrito(idCarrito)
    # Traemos los combos del carrito
    combos_carrito = []
    comboCarrito = Combo_carrito()
    combos_carrito = comboCarrito.combos_de_un_carrito(idCarrito)
    return render_template('carrito/mostrarCarrito.html', ejemplares=ejempares_carrito, combos=combos_carrito, total=total, idCarrito=idCarrito)


# No se usaría
""" @app.route('/modificarEjemplar_carrito') 
def modificarEjemplar_carrito():
    return render_template('ejemplar_carrito/modificarEjemplar_carrito.html')   """

# No se usaría
""" @app.route('/editarEjemplar_carrito', methods=["POST"])
def editarEjemplar_carrito():
    data = []
    if request.method == 'POST':
        idCarrito = request.form['idCarrito']
        numeroSerie = request.form['numeroSerie']
        nuevoIdCarrito = request.form['nuevoIdCarrito']
        nuevoNumeroSerie = request.form['nuevoNumeroSerie']  
        data = db.queryInsert('''
               UPDATE "ejemplar_carrito"
	                SET "idCarrito" = '{}', "numeroSerie" = '{}'
	                WHERE "idCarrito" = '{}' AND "numeroSerie" = '{}';
            '''.format(nuevoIdCarrito, nuevoNumeroSerie, idCarrito, numeroSerie))
    return render_template('index.html') """

# No se usaría
""" @app.route('/listarEjemplar_carrito')
def listarEjemplar_carrito():
    data = db.querySelect('''
                SELECT * FROM "ejemplar_carrito";
            ''')
    return render_template('ejemplar_carrito/listadoEjemplar_carrito.html', data=data)   """ 


#====COMPRA

# No se usaría
""" @app.route('/altaCompra')
def altaCompra():
     return render_template('compra/altaCompra.html')  """


@app.route('/confirmarCompra', methods=["POST"])
def confirmarCompra():
    data = []
    if request.method == 'POST':
        idCarrito = request.form['idCarrito']
        montoCompra = request.form['totalCarrito']  
        # Se crea la compra
        compra = Compra()
        compra.set_id_carrito(idCarrito)
        compra.set_monto_compra(montoCompra)
        compra.set_estado_confirmacion(False)
        data = compra.alta_compra() 
        # Se obtiene el id de la compra  
        ids = compra.id_compra(idCarrito)
        idCompra = ids[0][0]
        # Marcamos el carrito como finalizado
        carrito = Carrito()
        c = carrito.carrito_finalizado(idCarrito)
        return render_template('compra/compraConfirmada.html', total=montoCompra, idCarrito=idCarrito, idCompra=idCompra)

@app.route('/misCompras')
def misCompras():
    if 'email' in session:
        usuario = session['email']
        compra = Compra()
        data = compra.mis_compras(usuario)
        return render_template('compra/misCompras.html', data=data)
    else:
        return render_template('login/solicitarLogin.html')

@app.route('/verCompra', methods=["POST"])
def verCompra():
    if request.method == 'POST':
        idCompra = request.form['idCompra']
        idCarrito = request.form['idCarrito']
        total = request.form['total']
        estado = request.form['estado']
    ejemplar_carrito = Ejemplar_carrito()
    data = ejemplar_carrito.ejemplares_de_un_carrito(idCarrito)
    return render_template('compra/detalleCompra.html', data=data, total=total, estado=estado, idCompra=idCompra, idCarrito=idCarrito)


@app.route('/verVenta', methods=["POST"])
def verVenta():
    if request.method == 'POST':
        idCompra = request.form['idCompra']
        idCarrito = request.form['idCarrito']
        total = request.form['total']
        estado = request.form['estado']
    # Traemos los ejemplares del carrito correspondiente a la compra
    ejemplar_carrito = Ejemplar_carrito()
    ejemplares_carrito = ejemplar_carrito.ejemplares_de_un_carrito(idCarrito)
    # Treamos los combos del carrito correpondiente a la compra
    combos_carrito = []
    comboCarrito = Combo_carrito()
    combos_carrito = comboCarrito.combos_de_un_carrito(idCarrito)
    #Consultamos el estado del pago correspondiente al pago
    mercado_pago = MercadoPago()
    estado_pago = mercado_pago.estado_pago(idCompra)
    estado_pago = estado_pago[0][0]
    print(estado_pago)
    return render_template('compra/detalleVenta.html', ejemplares=ejemplares_carrito, combos= combos_carrito, total=total, estado=estado_pago, idCompra=idCompra, idCarrito=idCarrito)

# Elimina la compra desde admin
@app.route('/bajaVenta', methods=["POST"]) 
def bajaCompra():
    if request.method == 'POST':
        idCompra = request.form['idCompra']
    compra = Compra()
    compra.baja_compra(idCompra)
    return render_template('compra/compraEliminada.html') 


# Elimina la compra desde el comprador
@app.route('/cancelarCompra', methods=["POST"])
def cancelarCompra():
    if request.method == 'POST':
        idCompra = request.form['idCompra']
        idCarrito = request.form['idCarrito']
        total = request.form['total']
    # Eliminamos la compra
    compra = Compra()
    data = compra.baja_compra(idCompra)
    # Volvemos a activar el carrito
    carrito = Carrito()
    data = carrito.carrito_activo(idCarrito)
    # Vamos al carrito
    # Traemos los ejemplares del carrito
    ejemplar_carrito = Ejemplar_carrito()
    data = ejemplar_carrito.ejemplares_de_un_carrito(idCarrito)
    return render_template('carrito/mostrarCarrito.html', data=data, total=total, idCarrito=idCarrito) 
    
@app.route('/ventas')
def ventas():
    compra = Compra()
    data = compra.ventas()
    return render_template('compra/ventas.html', data=data)

# No se usaría
""" @app.route('/modificarCompra') 
def modificarCompra():
    return render_template('compra/modificarCompra.html')   """

# No se usaría
""" @app.route('/editarCompra', methods=["POST"])
def editarCompra():
    if request.method == 'POST':
        idCompra = request.form['id']
        nuevoMontoCompra = request.form['nuevoMontoCompra']
        nuevoEstadoConfirmacion = request.form['nuevoEstadoConfirmacion']

        compra = Compra()
        compra.set_id(idCompra)   

        data = compra.modificar_compra(nuevoMontoCompra, nuevoEstadoConfirmacion)
    return render_template('compra/compraModificada.html', data=data)
 """

# No se usaría
""" @app.route('/mostrarCompra')
def mostrarCompra():
    compra = Compra()
    data = compra.consultar_compra()
    return render_template('compra/mostrarCompra.html', data=data) """


#====PAGO
@app.route('/altaPago')
def altaPago():
     return render_template('pago/altaPago.html') 


@app.route('/guardarPago', methods=["POST"])
def guardarPago():
    data = []
    # Traemos los datos del formulario html
    if request.method == 'POST':
        idCompra = request.form['idCompra']
        total = request.form['total']

    # Creamos una referencia en mercadopago
    total = int(float(total))
    resultado = nuevaReerencia_mercadoPago(idCompra, total)
    id_mercadoPago = resultado['response']['id']
    link_mercadoPago = resultado['response']['init_point']  

    # Cargamos el pago a nuestra base de datos
    mercadoPago = MercadoPago()
    mercadoPago.set_id(id_mercadoPago)
    mercadoPago.set_id_compra(idCompra)
    mercadoPago.set_total(total)
    mercadoPago.set_link_pago(link_mercadoPago)
    mercadoPago.set_estado(False)
    data = mercadoPago.alta_mercadopago() 

    # Cerramos la compra, de forma que solo nos dirija al cupón de pago
    compra = Compra()
    C = compra.compra_confirmada(idCompra)

    return render_template('pago/mercadoPago.html', link=link_mercadoPago)

@app.route('/verCupon', methods=["POST"]) 
def verCupon():
    if request.method == 'POST':
        idCompra = request.form['idCompra']
    mercadoPago = MercadoPago()
    # Obtenemos el link para mercado pago
    link = mercadoPago.link_mercadopago(idCompra)
    link = link[0][0]
    return render_template('pago/mercadoPago.html', link=link)


@app.route('/bajaPago') 
def bajaPago():
    return render_template('pago/bajaPago.html')  


@app.route('/eliminarPago', methods=["POST"])
def eliminarPago():
    if request.method == 'POST':
        idPago = request.form['id']

        pago = Pago()
        pago.set_id(idPago)

        data = pago.baja_pago()
    return render_template('pago/pagoEliminado.html', data=data)    


@app.route('/modificarPago') 
def modificarPago():
    return render_template('pago/modificarPago.html')  


@app.route('/editarPago', methods=["POST"])
def editarPago():
    if request.method == 'POST':
        idPago = request.form['id']
        nuevoTotal = request.form['nuevoTotal']
        nuevoEstado = request.form['nuevoEstado']
        nuevaTarjeta = request.form['nuevaTarjeta']
        nuevoCuotas = request.form['nuevoCuotas']
        
        pago = Pago()
        pago.set_id(idPago)

        data = pago.modificar_pago(nuevoTotal, nuevoEstado, nuevaTarjeta, nuevoCuotas)        
    return render_template('pago/pagoModificado.html', data=data)


@app.route('/mostrarPago')
def mostrarPago():
    pago = Pago()    
    data = pago.consultar_pago() 
    return render_template('pago/mostrarPago.html', data=data)

    
#=========================Fin ABMC===================================


#========================== CLIENTE ===================================#
@app.route('/cliente')
@app.route('/cliente/home')
def cliente_home():
    data = {}
    producto = Producto()   
    data["productos"] = producto.formato_datos_tabla()
    return render_template('cliente/home.html', data=data)

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    ## Verifica si hay algún usuario logueado para dirigirlo a la vista correspondiente
    if 'email' in session:
        return render_template('cliente/faq.html')
    else:
        return render_template('cliente/faq-nolog.html')


@app.route('/contacto')
def contacto():
    ## Verifica si hay algún usuario logueado para dirigirlo a la vista correspondiente
    if 'email' in session:
        return render_template('cliente/contacto.html')
    else:
        return render_template('cliente/contacto-nolog.html')

#========================== Fin CLIENTE ===============================#

#========================== Sesion de usari ===============================#

@app.route('/login/validarRolUsuario')
def validarRolUsusario():
    if request.method == 'GET':
        res = request.args['usuario'] 
    ### si el usario existe , si es nuevo falta ARMAR y ver flujos js    
        usuario = Usuario()
        usuario.set_nombre(res)
        rol_id = usuario.validar_rol()
        data ={'rol_id': rol_id }
        #data ={'rol_id': 1 } #consultar backend HARCODEADO 1: admin (admin@admin.com), 2: cliente, 0 No registrado otro nada
        return jsonify(data)

@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template('login/loginAndrea.html')
    

@app.route('/loginAndrea', methods=["POST"])
def loginAndrea():
    if request.method == 'POST':
        email = request.form['email']
        contrasenia = request.form['contrasenia']
    ## Buscar el usuario en la base de datos
    usuario = Usuario()
    usuario.set_nombre(email)#La app usa el email como nombre de usuario 
    data = usuario.consultar_usuario_por_nombre()
    ## Si no encuentra el usuario le pide que se registre
    if data == []:
        return render_template('login/usuarioNoExiste.html')
    ## Si el usuario existe, verifica que la contraseña es la correcta
    elif data[1] != contrasenia:
        return render_template('login/contraseniaIncorrecta.html', email=email)
    ## Si encuentra en usuario y la contraseña es correcta, inicia sesion
    else:
        session['email'] = email
        session['contraseña'] = contrasenia
        ## Si es usuario es administrador, lo envía a la vista del admin
        if data[3] == 1:
            return render_template('admin/index_admin.html',data=data)
        ## Si es usuario es comprador, lo envía a la vista del cliente
        else:
            datos = []
            producto = Producto()
            datos = producto.listar_productos()
            #cuenta los elementos del data
            contador = 0
            for e in datos:
                contador = contador+1
            #agrega el stock y las imágenes de cada producto
            for e in range(contador):

                #guarda el stock del producto en la posición 8 del data
                ejemplar = Ejemplar()
                cantidad = ejemplar.cantidad_ejemplares_de_un_producto(datos[e][0])
                datos[e] += (cantidad[0][0],)

                #guarda la primer imagen del producto en la posición 9 del data
                imagenes = Imagenes()
                imgs = imagenes.imagenes_producto(datos[e][0])
                #Si no tiene imagen deja el campo vacio
                if imgs == []:
                    datos[e] += ()
                #Sino guarda la primer imagen
                else:
                    datos[e] += (imgs[0])
            return render_template('cliente/index_cliente_logueado.html',data=datos)

@app.route('/miCuenta')
def miCuenta():
    return render_template('usuario/miCuenta.html')

@app.route('/salir')
def salir():
    ## Elimina la sesion actual
    session.clear()
    return render_template('usuario/salir.html')

@app.route('/solicitarLogin', methods=["POST"])
def solicitarLogin():
    return render_template('login/solicitarLogin.html')

#========================== CLIENTE ===============================#




#Inicio de aplicacion
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(ssl_context='adhoc', debug=True)