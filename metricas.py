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
        #EUCLIDIANA
        DstEuclidiana = cdist(MEstandarizada, MEstandarizada, metric='euclidean')
        MEuclidiana = pd.DataFrame(DstEuclidiana)
        DstEuclidiana = cdist(MEstandarizada[0:10], MEstandarizada[0:10], metric='euclidean')
        MEuclidiana = pd.DataFrame(DstEuclidiana) 
        Objeto1 = MEstandarizada[colum]
        Objeto2 = MEstandarizada[filas]
        dstEuclidiana = distance.euclidean(Objeto1,Objeto2)

        #CHEBYSHEV
        DstChebyshev = cdist(MEstandarizada, MEstandarizada, metric='chebyshev')
        MChebyshev = pd.DataFrame(DstChebyshev)
        DstChebyshev = cdist(MEstandarizada[0:10], MEstandarizada[0:10], metric='chebyshev')
        MChebyshev = pd.DataFrame(DstChebyshev)
        CObjeto1 = MEstandarizada[colum]
        CObjeto2 = MEstandarizada[filas]
        dstChebyshev = distance.chebyshev(CObjeto1,CObjeto2)

        #Manhattan
        DstManhattan = cdist(MEstandarizada, MEstandarizada, metric='cityblock')
        MManhattan = pd.DataFrame(DstManhattan)
        DstManhattan = cdist(MEstandarizada[0:10], MEstandarizada[0:10], metric='cityblock')
        MManhattan = pd.DataFrame(DstManhattan)
        Objeto1M = MEstandarizada[colum]
        Objeto2M = MEstandarizada[filas]
        dstManhattan = distance.cityblock(Objeto1M,Objeto2M)

        #Minkowski
        DstMinkowski = cdist(MEstandarizada, MEstandarizada, metric='minkowski', p=1.5)
        MMinkowski = pd.DataFrame(DstMinkowski)
        DstMinkowski = cdist(MEstandarizada[0:10], MEstandarizada[0:10], metric='minkowski', p=1.5)
        MMinkowski = pd.DataFrame(DstMinkowski)
        Objeto1Mi = MEstandarizada[colum]
        Objeto2Mi = MEstandarizada[filas]
        dstMinkowski = distance.minkowski(Objeto1Mi,Objeto2Mi, p=1.5)
        

        #######################NORMALIZAMOS####################
        normalizar=MinMaxScaler()
        MNormalizada=normalizar.fit_transform(Hipoteca)
        #EUCLIDIANA
        DstNEuclidiana = cdist(MNormalizada, MNormalizada, metric='euclidean')
        MNEuclidiana = pd.DataFrame(DstNEuclidiana)
        DstNEuclidiana = cdist(MNormalizada[0:10], MNormalizada[0:10], metric='euclidean')
        MNEuclidiana = pd.DataFrame(DstNEuclidiana) 
        ObjetoEN1 = MNormalizada[colum]
        ObjetoEN2 = MNormalizada[filas]
        dstNEuclidiana = distance.euclidean(ObjetoEN1,ObjetoEN2)

        #CHEBYSHEV
        DstNChebyshev = cdist(MNormalizada, MNormalizada, metric='chebyshev')
        MNChebyshev = pd.DataFrame(DstNChebyshev)
        DstNChebyshev = cdist(MNormalizada[0:10], MNormalizada[0:10], metric='chebyshev')
        MNChebyshev = pd.DataFrame(DstNChebyshev)
        CNObjeto1 = MNormalizada[colum]
        CNObjeto2 = MNormalizada[filas]
        dstNChebyshev = distance.chebyshev(CNObjeto1,CNObjeto2)

        #Manhattan
        DstNManhattan = cdist(MNormalizada, MNormalizada, metric='cityblock')
        MNManhattan = pd.DataFrame(DstNManhattan)
        DstNManhattan = cdist(MNormalizada[0:10], MNormalizada[0:10], metric='cityblock')
        MNManhattan = pd.DataFrame(DstNManhattan)
        NObjeto1M = MNormalizada[colum]
        NObjeto2M = MNormalizada[filas]
        dstNManhattan = distance.cityblock(NObjeto1M,NObjeto2M)

        #Minkowski
        DstNMinkowski = cdist(MNormalizada, MNormalizada, metric='minkowski', p=1.5)
        NMMinkowski = pd.DataFrame(DstNMinkowski)
        DstNMinkowski = cdist(MNormalizada[0:10], MNormalizada[0:10], metric='minkowski', p=1.5)
        NMMinkowski = pd.DataFrame(DstNMinkowski)
        NObjeto1Mi = MNormalizada[colum]
        NObjeto2Mi = MNormalizada[filas]
        dstNMinkowski = distance.minkowski(NObjeto1Mi,NObjeto2Mi, p=1.5)
        

        #calculating the algorithm execution time
        end = datetime.datetime.now()
        program_run_time = str((end - start))  
      
        

    return render_template('content1.html',  program_run_time= program_run_time, filename =filename,colum=colum, filas=filas, content=content, dstEuclidiana=dstEuclidiana,MEuclidiana=MEuclidiana.to_html(),
                           dstChebyshev=dstChebyshev, MChebyshev=MChebyshev.to_html(),dstManhattan=dstManhattan, MManhattan=MManhattan.to_html(),
                           dstMinkowski=dstMinkowski, MMinkowski=MMinkowski.to_html(),dstNEuclidiana=dstNEuclidiana,MNEuclidiana=MNEuclidiana.to_html(),
                           dstNChebyshev=dstNChebyshev, MNChebyshev=MNChebyshev.to_html(),dstNManhattan=dstNManhattan, MNManhattan=MNManhattan.to_html(),
                           dstNMinkowski=dstNMinkowski, NMMinkowski=NMMinkowski.to_html()) 



if __name__ == '__main__':
    application.run()