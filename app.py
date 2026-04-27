from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

#conexion a la BD tienda_db en mysql
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "tienda_db"

@app.route('/test')
def test():
    cursor = mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    return "conexion existosa!!!"


'''@app.route('/')
def inicio():
    return "Servidor Flask funcionando!!!"'''

#ENDPOINT GET /categorias
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    cursor = mysql.connection.cursor()
    sql = "SELECT id, nombre FROM categoria"
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos is None:
        msg = {
            "mensage": "No existe producto!!"
        }
        return jsonify(msg)
   
    categorias = []
    for fila in datos:
        categorias.append(
            {
                "id": fila[0],
                "nombre": fila[1]
            }
        )
    cursor.close()
    return jsonify(categorias)

# endpoint POST /categorias
@app.route('/categorias', methods=['POST'])
def crear_categoria():
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO categoria (nombre) VALUES (%s)"
    cursor.execute(sql, (request.json['nombre'],))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Producto creado con exito!!"})

# endpoint GET /productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    cursor = mysql.connection.cursor()
    sql = "SELECT id, nombre, precio, stock, categoria_id FROM producto"
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos is None:
        msg = {
            "mensage": "No existe producto!!"
        }
        return jsonify(msg)
   
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria_id": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

# endpoint GET /productos/<id>
@app.route('/productos/<int:id>', methods=['GET'])
def producto_id(id):
    cursor = mysql.connection.cursor()
    sql = """SELECT id, nombre, precio, stock, categoria_id
             FROM producto
             WHERE id = %s"""
    cursor.execute(sql,(id,))
    datos = cursor.fetchone()

    if datos is None:
        msg = {
            "mensage": "No existe producto!!"
        }
        return jsonify(msg)
   
    productos = []
    productos.append(
        {
            "id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2]),
            "stock": datos[3],
            "categoria_id": datos[4]
        }
    )
    cursor.close()
    return jsonify(productos)

# endpoint POST /productos
@app.route('/productos', methods=['POST'])
def crear_producto():
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO producto (nombre, precio, stock, categoria_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (request.json['nombre'], request.json['precio'], request.json['stock'], request.json['categoria_id']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Producto creado con exito!!"})

# endpoint GET /productos_categoria
@app.route('/productos_categoria', methods=['GET'])
def producto_con_categoria():
    cursor = mysql.connection.cursor()
    sql = """SELECT p.id, p.nombre, p.precio, p.stock, c.nombre
             FROM producto p
             JOIN categoria c
             ON c.id = p.categoria_id"""
    cursor.execute(sql)
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": (fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

@app.route('/productos/categoria/<int:id>', methods=['GET'])
def producto_por_categoria(id):
    cursor = mysql.connection.cursor()
    sql = """SELECT p.id, p.nombre, p.precio, p.stock, c.nombre
             FROM producto p
             JOIN categoria c
             ON c.id = p.categoria_id
             WHERE c.id = %s"""
    cursor.execute(sql,(id,))
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

@app.route('/productos/caro',methods=['GET'])
def producto_mas_caro():
    cursor = mysql.connection.cursor()
    sql = '''SELECT p.id, p.nombre, p.precio
             FROM producto p
             WHERE p.precio = (
                SELECT MAX(precio)
                FROM producto
             )'''
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()

    resultado = []
    for fila in datos:
        resultado.append({
            "id": fila[0],
            "nombre": fila[1],
            "precio": float(fila[2])
        })

    return jsonify(resultado)

@app.route('/producto/menos_stock')
def producto_menor_stock():
    cursor = mysql.connection.cursor()
    sql = '''SELECT p.id, p.nombre, p.stock
             FROM producto p
             WHERE p.stock = (
                SELECT MIN(stock)
                FROM producto
             )
             '''
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()

    respuesta = []
    for fila in datos:
        respuesta.append({
            "id": fila[0],
            "nombre": fila[1],
            "stock": fila[2]
        })

    return jsonify(respuesta)

@app.route('/productos_por_categoria')
def productos_por_categoria():
    cursor = mysql.connection.cursor()
    sql = '''SELECT
                c.nombre AS categoria,
                COUNT(p.id) AS total_productos
             FROM categoria c
             JOIN producto p ON c.id = p.categoria_id
             GROUP BY c.id, c.nombre
          '''
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()

    respuesta = []
    for fila in datos:
        respuesta.append({
            "categoria": fila[0],
            "total_productos": fila[1]
        })

    return jsonify(respuesta)
    
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/categorias',methods=['POST'])
def insertar_categoria():
    data = request.json
    nombre = data['nombre']
    #insertar en la 80
    cursor = mysql.connection.cursor()
    sql = '''INSERT INTO categoria (nombre)
             VALUES (%s)'''
    cursor.execute(sql,(nombre,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Categoria registrada con exito"}),201

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']
    stock = data['stock']
    categoria_id = data['categoria_id']
    
    cursor = mysql.connection.cursor()
    sql = """INSERT INTO producto(nombre,precio,stock,categoria_id)
            VALUES (%s, %s, %s, %s)"""
    
    cursor.execute(sql, (nombre , precio, stock, categoria_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"Producto insertado"}),201
    
@app.route('/categorias/<int:id>',methods=['PUT'])
def modificar_categoria(id):
    data = request.get_json()
    nombre = data['nombre']
    cursor = mysql.connection.cursor()
    sql = '''UPDATE categoria SET nombre = %s WHERE id = %s'''
    cursor.execute(sql,(nombre,id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Categoria modificada"}),200

@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()

    nombre = data['nombre']
    precio = data['precio']
    stock = data['stock']
    categoria_id = data['categoria_id']

    cursor = mysql.connection.cursor()
    sql = """ UPDATE producto
                   SET nombre = %s,  precio = %s,  stock = %s, categoria_id = %s
                   WHERE id = %s """

    cursor.execute(sql, (nombre , precio, stock, categoria_id , id,))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

@app.route('/categoria/<int:id>',methods=['DELETE'])
def eliminar_categoria(id):
    cursor = mysql.connection.cursor()
    sql = '''DELETE FROM categoria WHERE id = %s'''
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"Categoria eliminada"}),200


if __name__ == "__main__":
    app.run(debug=True)