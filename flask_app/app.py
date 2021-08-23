import traceback
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, Response
from config import config
import os
import localidad
import pytz



db = SQLAlchemy()

app = Flask(__name__)

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"
localidad.db.init_app(app)


@app.route("/reset")
def reset():
    try:
        localidad.create_schema()
        result = "<h3> Base de datos re-generada!</h3>"
        return render_template('tabla.html')
    except:
        return jsonify({'trade': traceback.format_exc()})
    
    
   
    
@app.route("/registro")
def registro():
    if request.method == 'GET':
        try:
            data = localidad.report()
            return render_template('tabla.html',data = data)
        except:
            return jsonify({'trace': traceback.format_exc()})
    



@app.route("/",methods=['GET','POST'])
def meli():
    if request.method == 'GET':
        try:
            return render_template('registro.html')
        except:
            return jsonify({'trice': traceback.format_exc()})
    if request.method == 'POST':
        try:
            time1 = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
            time = time1.strftime('%d/%m/%Y, %H:%M')
            location = str(request.form.get('location'))
            price_min = str(request.form.get('price_min'))
            price_max = str(request.form.get('price_max'))
            if (location is None or price_min.isdigit() and price_max.isdigit() is False):
                return Response(status=400)
            localidad.insert(location,int(price_min),int(price_max),time)
            
            min = int(price_min)
            max = int(price_max)
            dataset = localidad.fetch(location)
            data = localidad.transform(dataset,min,max)
            encoded_img = localidad.grafico(data,location)
            return render_template('grafico.html',overview_graph=encoded_img)
           
        except:
            return jsonify({'trace': traceback.format_exc()})


    
        

if __name__ == '__main__':
    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)
