from app.module import Mapper
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
    return render_template("index.html")

@app.route("/index", methods=["GET", "POST"])
def home():

    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')

@app.route("/map")
def map():
    return render_template("_map.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)
