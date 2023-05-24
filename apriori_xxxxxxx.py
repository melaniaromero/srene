import os
from itertools import chain, combinations
from collections import defaultdict
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import datetime
import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import csv
from apyori import apriori


application = Flask(__name__)

application.config["UPLOAD_FOLDER"] = "static/"

def format_results(items):
    i = []
    for item, count in sorted(items, key=lambda x: x[1]):
        i.append(item)
    return set(i)

@application.route('/')
def upload_file():
    return render_template('index.html')

#Result page.
@application.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        s = request.form['support']
        c =request.form['confidence']
        l =request.form['lift']
        #support =float(s)
        #confidence = float(c)
        #lift = int(l)
        filename = secure_filename(f.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))

        f.save(os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename))
        filepath=os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename)
        file = open(application.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        
       # infile = []


    #if infile is None:  
        start = datetime.datetime.now()
        DatosTransacciones = pd.read_csv(filepath, header=None)
        #Se incluyen todas las transacciones en una sola lista
        Transacciones = DatosTransacciones.values.reshape(-1).tolist() #-1 significa 'dimensión desconocida'
        Lista = pd.DataFrame(Transacciones)
        Lista['Frecuencia'] = 1
        #Se agrupa los elementos
        Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
        Lista = Lista.rename(columns={0 : 'Item'})
        TransaccionesLista = DatosTransacciones.stack().groupby(level=0).apply(list).tolist()
        items = apriori(TransaccionesLista,min_support =float(s),min_confidence = float(c),min_lift = int(l))
        #print(items)
        #calculating the algorithm execution time
        end = datetime.datetime.now()
        program_run_time = str((end - start))  


        #res= format_results(items)
        ResultadosC1 = list(items)

        total_item = len(ResultadosC1)

      
        

    return render_template('content.html', s=s,c=c, l=l, filename =filename,content=content, ResultadosC1=ResultadosC1, total_item=total_item) 



if __name__ == '__main__':
    application.run()