from flask import Flask, render_template, request, json
from flask_mysqldb import MySQL

# Inicializacion del objeto MySQL
mysql = MySQL()
# Inicializacion de la app de Flask
app = Flask(__name__)
# Configuracion de MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
app.config.setdefault('MYSQL_UNIX_SOCKET', None)
app.config.setdefault('MYSQL_USE_UNICODE', True)
app.config.setdefault('MYSQL_CHARSET', 'utf8')
app.config.setdefault('MYSQL_SQL_MODE', None)
app.config.setdefault('MYSQL_CURSORCLASS', None)
app.config['MYSQL_PASSWORD'] = 'Icc3u0qk'
app.config['MYSQL_DB'] = 'BGP'


# Ruta basica y su handler
@app.route("/")
def main():
    return render_template("index.html")


# Ruta de lectura con su request handler
@app.route('/lectura', methods=['POST'])
def showLectura():
    try:
        # Se emplea el metodo POST para traer las variables obtener las variables
        if request.method == 'POST':
            red = request.form['red']
            dia = request.form['dia']
            # Se genera el cursor de MySQL
            cursor = mysql.connection.cursor()
            # Se compara con la red y la fecha de registro de las rutas
            cursor.execute("SELECT * FROM DatosBGP WHERE red = '%s' and fecha='%s'" % (red, dia))
            # Se extrae las cabeceras del cursor
            cabecera = [x[0] for x in cursor.description]
            # Se toma un registro de todos los datos de la ejecucion
            record = cursor.fetchall()
            # Json del resultado
            json_data = []
            for result in record:
                json_data.append(dict(zip(cabecera, result)))
            return json.dumps(json_data)
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    # Ejecucion de la app
    app.run(host='localhost', port=5000)
