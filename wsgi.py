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
from datetime import datetime
import json
app = Flask(__name__)
app.secret_key = "7eb00e9bd0fd0310b36b92f8c45b59ae3b29349f36b6dc40d255bea847fdcd34"

py_path = pathlib.Path(__file__).parent.resolve()
db_path = os.environ.get('DB_PATH', os.path.join(py_path, "database.db"))

@app.route("/", methods=["GET", "POST"])
def index():
    youtube_module = YouTubeModule()
    x_module = XModule()

    json_path = os.path.join(py_path, "example.json") # will switch to actual db when finished
    country_data_path = os.path.join(py_path, "country_data.json")
    country_options = []
    if os.path.exists(json_path) and os.path.exists(country_data_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        with open(country_data_path, 'r') as f:
            country_data = json.load(f)
        
        country_codes = {item.get("data", {}).get("country_code") for item in data if item.get("data", {}).get("country_code")}
        country_options = sorted([(code, country_data.get(code, {}).get('name', code)) for code in country_codes], key=lambda x: x[1])

    database_module = DatabaseModule(countries=country_options)
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
    mapper.add_tile_layer(layer_name="Esri WorldImagery")
    mapper.render()
    return render_template("_map.html")

@app.route("/run_database", methods=["GET", "POST"])
def run_database():
    db_search = request.form.get("db_search")
    lat = request.form.get("db_lat")
    lng = request.form.get("db_lng")
    country = request.form.get("country_search")
    start_date_str = request.form.get("start_date")
    end_date_str = request.form.get("end_date")
    platforms = request.form.getlist("platforms")
    media_types = request.form.getlist("type")

    start_date = None
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    end_date = None
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#temp dummy
    json_path = os.path.join(py_path, "example.json")
    if not os.path.exists(json_path):
        return "example.json not found", 404

    with open(json_path, 'r') as f:
        data = json.load(f)

    mapper = Mapper.MapRender()
    popup_creator = _Popups.Create_Popup()

    for item in data:
        entry = item.get("data", {})
        
        if db_search and db_search.lower() not in entry.get("text", "").lower():
            continue
        if country and country != "all" and entry.get("country_code", "").lower() != country:
            continue
        if platforms and entry.get("platform") not in platforms:
            continue
        if media_types and entry.get("type") not in media_types:
            continue

        entry_date_str = entry.get("date")
        if entry_date_str:
            entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue

        elif start_date or end_date:
            continue
            
        p_type = entry.get("type")
        if p_type == "video" and entry.get("platform") == "IPCamera":
            popup = popup_creator.CreateVideo(video_src=entry.get("url"), desc=entry.get("text"), lat=entry.get("lat"), lng=entry.get("lon"), platform=entry.get("platform"), url=entry.get("url"))
            icon, color = "camera", "purple"
        elif p_type == "video":
            popup = popup_creator.CreateVideo(video_src=entry.get("url"), desc=entry.get("text"), lat=entry.get("lat"), lng=entry.get("lon"), platform=entry.get("platform"), url=entry.get("url"))
            icon, color = "play", "red"
        elif p_type == "image":
            popup = popup_creator.CreateImg(img_src=entry.get("url"), desc=entry.get("text"), lat=entry.get("lat"), lng=entry.get("lon"), platform=entry.get("platform"), url=entry.get("url"))
            icon, color = "picture", "blue"
        else:
            popup = popup_creator.CreateText(desc=entry.get("text"), lat=entry.get("lat"), lng=entry.get("lon"), platform=entry.get("platform"), url=entry.get("url"))
            icon, color = "info-sign", "green"

        mapper.add_marker((entry.get("lat"), entry.get("lon")), tooltip=entry.get("text"), popup_context=popup, icon=icon, color=color)

    mapper.add_tile_layer(layer_name="Esri WorldImagery")
    mapper.render()
    return render_template("_map.html")           
if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)