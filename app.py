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
quartieri = geopandas.read_file("Quartieri/NIL_WM.dbf")
quartieri3857 = quartieri.to_crs(epsg=3857)

@app.route('/')
def home():
    listaComune = list(comuni3857["COMUNE"])
    listaComune.sort()
    return render_template("home.html",lista = listaComune)

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

@app.route('/esercizio2', methods = ["GET"])
def esercizio2():
    navigli = corsi_acqua3857[corsi_acqua3857["NOME"].str.contains("Naviglio")]
    Navigli_interseca= corsi_acqua3857[corsi_acqua3857.touches(navigli.unary_union)]
    ax = navigli.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6))
    Navigli_interseca.plot(ax=ax,edgecolor =  "blue", facecolor = "None",figsize=(12,6))
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio2.html")

@app.route('/esercizio3', methods = ["GET"])
def esercizio3():
    comuneInput = request.args.get("comuneInput")
    comu = comuni3857[comuni3857["COMUNE"]== comuneInput]
    comuni_in_corsi = corsi_acqua3857[corsi_acqua3857.intersects(comu.geometry.item())]
    ax = comu.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6))
    comuni_in_corsi.plot(ax=ax, edgecolor =  "blue", facecolor = "None",figsize=(12,6))
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio3.html")


@app.route('/esercizio4', methods = ["GET"])
def esercizio4():
    fiumeInput = request.args.get("fiumeInput")
    fiu = corsi_acqua3857[corsi_acqua3857["NOME"].str.contains(fiumeInput)]
    comuni_in_corsi = comuni3857[comuni3857.intersects(fiu.unary_union)]
    quartieri_in_corsi = quartieri3857[quartieri3857.intersects(fiu.unary_union)]
    ax = comuni_in_corsi.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6))
    quartieri_in_corsi.plot(ax=ax,edgecolor =  "green", facecolor = "None")
    fiu.plot(ax=ax,edgecolor =  "blue", facecolor = "None")
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es4.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio4.html")

 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)