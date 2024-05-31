from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app=Flask(__name__)
conexion=MySQL(app)
# Configura CORS para permitir todas las solicitudes desde cualquier origen
CORS(app)

@app.route('/api/cursos/listar', methods=['GET'])

def listar_cursos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo,nombre,creditos FROM curso"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso={'codigo':fila[0],'materia':fila[1],'creditos':fila[2],}
            cursos.append(curso)
        return jsonify({'cursos':cursos,'mensaje':"Cursos Listados"})
    except Exception as ex:
        return "ERROR"
    
@app.route('/api/cursos/buscar/<codigo>',methods=['GET'])

def leer_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo,nombre,creditos FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()

        if datos is not None:
            curso={'codigo':datos[0],'materia':datos[1],'creditos':datos[2],}
            return jsonify({'curso':curso,'mensaje':"Curso Econtrado"})
        
        else:
            return jsonify({'mensaje':"Curso NO Encontrado"})

    except Exception as ex:
        return "ERROR"

@app.route('/api/cursos/alta',methods=['POST'])

def registrar_curso():
    try:
        print(request.json)
        cursor=conexion.connection.cursor()
        sql="INSERT INTO curso (codigo, nombre, creditos) VALUES ('{0}','{1}',{2})".format(request.json['codigo'],request.json['nombre'],request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Curso Registrado"})

    except Exception as ex:
        return "ERROR"

@app.route('/api/cursos/eliminar/<codigo>',methods=['DELETE'])

def eliminar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Curso Eliminado"})

    except Exception as ex:
        return "ERROR"

@app.route('/api/cursos/actualizar/<codigo>',methods=['PUT'])

def actualizar_curso(codigo):
    try:
        print(request.json)
        cursor=conexion.connection.cursor()
        sql="UPDATE curso SET nombre = '{0}', creditos = '{1}' WHERE codigo = '{2}'".format(request.json['nombre'],request.json['creditos'],codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Curso Actualizado"})

    except Exception as ex:
        return "ERROR"

def pagina_no_encontada(error):
    return "<h1>PAGINA NO ENCONTRADA...</h1>",404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontada)
    app.run()