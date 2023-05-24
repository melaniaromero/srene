import os
from itertools import chain, combinations
from collections import defaultdict
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import datetime
import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales         
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

application = Flask(__name__)

application.config["UPLOAD_FOLDER"] = "static/"


@application.route('/')
def upload_file():
    return render_template('index.html')

#Result page.
@application.route('/metricas', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        colu =request.form['columna']
        fil =request.form['fila']
        colum =int(colu)
        filas = int(fil)
    
        filename = secure_filename(f.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))

        f.save(os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename))
        filepath=os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename)
        file = open(application.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        
     
        start = datetime.datetime.now()
        Hipoteca = pd.read_csv(filepath)
        ###################ESTANDARIZAMOS########################
        estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler o MinMaxSca
        MEstandarizada = estandarizar.fit_transform(Hipoteca) 
        DstEuclidiana = cdist(MEstandarizada, MEstandarizada, metric='euclidean')
        MEuclidiana = pd.DataFrame(DstEuclidiana)
        DstEuclidiana = cdist(MEstandarizada[0:10], MEstandarizada[0:10], metric='euclidean')
        MEuclidiana = pd.DataFrame(DstEuclidiana)

        
        Objeto1 = MEstandarizada[colum]
        Objeto2 = MEstandarizada[filas]
        dstEuclidiana = distance.euclidean(Objeto1,Objeto2)
        

        #######################NORMALIZAMOS####################
        normalizar=MinMaxScaler()
        MNormalizada=normalizar.fit_transform(Hipoteca)
        

        #calculating the algorithm execution time
        end = datetime.datetime.now()
        program_run_time = str((end - start))  
      
        

    return render_template('content1.html', filename =filename,colum=colum, filas=filas, content=content, dstEuclidiana=dstEuclidiana,MEuclidiana=MEuclidiana.to_html()) 



if __name__ == '__main__':
    application.run()