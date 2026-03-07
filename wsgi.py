from app.modules import Mapper
from app.modules import _Popups
from app.modules.youtube import YouTubeModule
from app.modules.x import XModule
from app.modules.Read_Database import DatabaseModule
from flask import Flask, redirect, render_template
# renderer = Mapper.MapRender()
# renderer.add_tile_layer("Esri WorldImagery")
# renderer.add_marker((51.5074, -0.1278), "London")
# renderer.add_marker((12.3456,7.8901),"HEHEHOHOHAHA")
# renderer.render()


from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_file,
    session,
    flash,
    send_from_directory,
    blueprints
)
import pathlib
import os

app = Flask(__name__)
app.secret_key = "7eb00e9bd0fd0310b36b92f8c45b59ae3b29349f36b6dc40d255bea847fdcd34"

py_path = pathlib.Path(__file__).parent.resolve()
db_path = os.environ.get('DB_PATH', os.path.join(py_path, "database.db"))

@app.route("/", methods=["GET", "POST"])
def index():
    youtube_module = YouTubeModule()
    x_module = XModule()
    database_module = DatabaseModule()
    return render_template("index.html",youtube_module=youtube_module,x_module=x_module,database_module=database_module) 
    
@app.route("/index", methods=["GET", "POST"])
def home():
    return redirect(url_for("index"))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')

@app.route("/map")
def map():
    popup = _Popups.Create_Popup()
    
    mapper = Mapper.MapRender()
    mapper.add_marker((0,100),tooltip="Angus",popup_context=popup.CreateImg(img_src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMrSKCU00zc6mm0j-T2Sgm6txurUiT1TMw85N1Rq2DUwc0x4Ln3jMurYwLiOmef1ECGvMw7GhAStqfp55hqI0663wsMHLD6lqR5bFj-w&s=10",desc="defualt description",lat="0",lng="100",url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMrSKCU00zc6mm0j-T2Sgm6txurUiT1TMw85N1Rq2DUwc0x4Ln3jMurYwLiOmef1ECGvMw7GhAStqfp55hqI0663wsMHLD6lqR5bFj-w&s=10",platform="YouTube"))

    mapper.add_tile_layer(layer_name="Esri WorldImagery")
    mapper.render()
    return render_template("_map.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)