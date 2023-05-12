from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas 
import os 
import contextily 
import matplotlib.pyplot as plt


provincie = geopandas.read_file("Province/ProvCM01012023_g_WGS84.dbf")
provincie3857 = provincie.to_crs(3857)
comuni = geopandas.read_file("Comuni/Com01012023_g_WGS84.dbf")
comuni3857 = comuni.to_crs(3857)
corsi_acqua = geopandas.read_file("Corsi_acqua/Corsi_acqua_Piano_di_Gestione.dbf")
corsi_acqua3857 = corsi_acqua.to_crs(epsg=3857)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/esercizio1', methods = ["GET"])
def esercizio():
    corsi_lunghi = corsi_acqua3857.sort_values('SHAPE_LEN', ascending=False)[:10]
    ax = corsi_lunghi.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6),markersize = 5)
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio1.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)