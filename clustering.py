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
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import matplotlib
matplotlib.use('Agg')


application = Flask(__name__)

application.config["UPLOAD_FOLDER"] = "static/"


@application.route('/')
def upload_file():
    return render_template('index.html')

#Result page.
@application.route('/clustering', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
    
        filename = secure_filename(f.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))

        f.save(os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename))
        filepath=os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename)
        file = open(application.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        
     
        start = datetime.datetime.now()

        rango1=[i for i in range(2,12)]
        BCancer = pd.read_csv(filepath, usecols=rango1)
        #Evaluación visual
        BCancerConcavity=BCancer.groupby('Concavity').size()
        #seleccion de caracteristicas
        #Evaluación visual
        sns.pairplot(BCancer, hue='Concavity')
        plt.savefig('static/my_plot.png')

        sns.scatterplot(x='Radius', y ='Perimeter', data=BCancer, hue='Concavity')
        plt.title('Gráfico de dispersión')
        plt.xlabel('Radius')
        plt.ylabel('Perimeter')
        plt.show()
        plt.savefig('static/my_plot1.png')
        
        #calculating the algorithm execution time
        end = datetime.datetime.now()
        program_run_time = str((end - start))  
      
        

    return render_template('content2.html',  program_run_time= program_run_time, filename =filename, 
                           content=content, get_plot = True, plot_url = 'static/my_plot.png',  plot_url1 = 'static/my_plot1.png') 



if __name__ == '__main__':
    application.run()