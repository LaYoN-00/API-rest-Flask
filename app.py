from flask import Flask, jsonify, request, json
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

app=Flask(__name__)
conexion=MySQL(app)
# Configura CORS para permitir todas las solicitudes desde cualquier origen
CORS(app)


#RUTAS PARA HACER CRUD SOBRE ALGUNA TABLA DE LA DB

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
        return jsonify(cursos)
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
            return jsonify(curso)
        
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
    
#RUTAS PARA USAR EL ARBOL DE DECISION
@app.route('/api/arbol-decision/global',methods=['GET'])

def ArbolDecisionGlobal():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT numeros_primos, tiempo_numeros_primos, criterios_de_divisibilidad, tiempo_criterios_divisibilidad, ecuaciones_cuadraticas, tiempo_ecuaciones_cuadraticas, teorema_de_pitagoras, tiempo_teorema_pitagoras, algebra, tiempo_algebra, funciones, tiempo_funciones, trigonometria, tiempo_trigonometria, geometria, tiempo_geometria, calculo, tiempo_calculo, tema_tipo_refuerzo FROM calificaciones_examenes"
        cursor.execute(sql)
        datos=cursor.fetchall()
        # Obteniendo los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        # Creando el DataFrame
        df = pd.DataFrame(datos, columns=columnas)
        # Supongamos que 'mi_objetivo' es la columna que quieres predecir y el resto son las características
        X = df.drop('tema_tipo_refuerzo', axis=1)
        y = df['tema_tipo_refuerzo']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)
        arbol = DecisionTreeClassifier(criterion='entropy', max_depth=4)
        # Entrenar el modelo con el conjunto de entrenamiento
        arbol.fit(X_train, y_train)
        # Realizar predicciones en el conjunto de prueba
        y_pred = arbol.predict(X_test)
        print("PREDICCION DEL MODELO: ", y_pred[0:5])
        # Calcular la precisión
        precision = accuracy_score(y_test, y_pred)
        print("La precisión del modelo es: ", precision)
        # Crear un diccionario con los resultados
        resultados = {
            "prediccion": y_pred.tolist(),  # Convertir el array numpy a lista
            "precision": precision
        }

        # Retornar los resultados en formato JSON
        return jsonify(resultados)
    
    except Exception as ex:
        return "ERROR"
    
@app.route('/api/arbol-decision/local',methods=['GET'])


def pagina_no_encontada(error):
    return "<h1>PAGINA NO ENCONTRADA...</h1>",404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontada)
    app.run()