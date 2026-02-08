import folium
from folium.plugins import MarkerCluster

from typing import Optional, Union

class MapRender:
    """Folium setup, change width and height here"""

    maplayers = {
    "Stadia Dark": ("https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png", 
                   '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors', 
                   "Stadia Dark"),
    "ArcGIS Street": ("https://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", 
                     '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>', 
                     "ArcGIS Street"),
    "MtbMap": ("http://tile.mtbmap.cz/mtbmap_tiles/{z}/{x}/{y}.png", 
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & USGS', 
              "MtbMap"),
    "Esri WorldImagery": ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
                         'Tiles &copy; Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, GIS User Community', 
                         "Esri Satellite"),
    }
    # mapoverlays = {
    #     # UK
    #     "UK LiDAR": ("https://services.magic.gov.uk/wms", "lidar_composite_dtm_1m", "© MAGIC/EA"),
    #     "Wales LiDAR": ("https://mapservices.nrw.gov.uk/arcgis/services/LiDAR/LiDAR_WMS/MapServer/WMSServer", "LiDAR_Composite_DTM_1m", "© NRW"),
        
    #     # USA
    #     "US Hillshade": ("https://elevationarcgis.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/WMSServer", "3DEPElevation_Hillshade", "© USGS"),
    #     "US Coastal": ("https://coast.noaa.gov/arcgis/rest/services/2021_LiDAR_USA/MapServer/WMSServer", "LiDAR_USA", "© NOAA"),
        
    #     # EUROPE
    #     "Netherlands LiDAR": ("https://service.pdok.nl/brt/ahn3/v1_0/ahn3_05m_dsm/wms/v1_0", "ahn3_05m_dsm", "© PDOK/AHN"),
    #     "Germany LiDAR": ("https://sgx2.kartenserver.de/services/DGM_10/WMS", "DGM_10", "© Kartenserver.de"),
    #     "France LiDAR": ("https://wms.ign.fr/r/geoportail/wms?SERVICE=WMS", "GEOGRAPHICALGRIDSYSTEMS.MAPS@STREETS", "© IGN France"),
        
    #     # AUSTRALIA
    #     "Aus LIDAR": ("https://elevation.fsdf.org.au/arcgis/rest/services/ELVIS/Elevation_Contours_5m/MapServer/WMSServer", "Elevation_Contours_5m", "© Geoscience Australia"),
        
    #     # CANADA
    #     "Canada LiDAR": ("https://maps.canada.ca/arcgis/rest/services/CanadaElevation/HRDEM/MapServer/WMSServer", "HRDEM", "© Natural Resources Canada"),
        
    #     # NEW ZEALAND
    #     "NZ LiDAR": ("https://basemaps.linz.govt.nz/v1/Topo50hillshade/tiles/512/png/{z}/{x}/{y}.png", "© LINZ", "NZ Hillshade")
    # }


    def __init__(self, width : int = 100, height : int = 100, location : tuple[float, float] = (0.0000,0.0000),zoom_start : int = 2, max_zoom : int = 18, min_zoom : int = 2):
        self.width = f"{width}%"        
        self.height = f"{height}%"
        self.location = location
        self.m = None
        self.markers = []
        self.circle_markers = []
        self.tiles = []
        # self.overlays = []
        self.zoom_start = zoom_start
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.marker_cluster = None
        
    def render(self):
        """Folium render, the markers and layers are added here"""

        self.m = folium.Map(
        width = self.width,
        height = self.height,
        location = self.location,
        zoom_start=self.zoom_start,
        max_zoom=self.max_zoom,
        min_zoom=self.min_zoom
        )
        self.marker_cluster = MarkerCluster(name="Markers").add_to(self.m)

        for tiles, name, attr, overlay in self.tiles:
            folium.TileLayer(
                tiles=tiles, attr=attr or f"© {name}", name=name, overlay=overlay
            ).add_to(self.m)

        # for tiles, name, attr in self.overlays:
        #     folium.raster_layers.WmsTileLayer(
        #         url = tiles.split('?')[0],
        #         layers = name,
        #         fmt = 'image/png',
        #         transparent = True,
        #         overlay = True,
        #         control = True,
        #         attr = attr,
        #         name = name
        #     ).add_to(self.m)
        
        for loc, text, color, tooltip, icon in self.markers:
            folium.Marker(
                loc, popup=text, tooltip=tooltip,
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(self.marker_cluster)
            
        for loc, text, radius, color, weight, fill, fill_color, fill_opacity, tooltip in self.circle_markers:
            folium.CircleMarker(
                loc, popup=text,
                radius=radius,
                color=color,
                weight=weight,
                fill=fill,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                tooltip=tooltip
            ).add_to(self.m)

        folium.LayerControl().add_to(self.m)

        html_content = self.m.get_root().render()
        with open("map_test.html", "w") as f:
            f.write(html_content) 
        return self

    def add_tile_layer(self, layer_name: str = "OpenStreetMap"):
        """Select layer by name, for example: 'Esri', 'OpenStreetMap', 'Stamen Terrain'"""
        if layer_name not in self.maplayers:
            raise ValueError(f"Choose from {list(self.maplayers)}")
        tiles, attr, name = self.maplayers[layer_name]
        self.tiles.append((tiles, name, attr, False))

    def add_overlay(self, overlay_name: Optional[str] = "LiDAR UK"):
        """Adds an overlay"""
        if overlay_name not in self.mapoverlays:
            raise ValueError(f"Overlays: {list(self.mapoverlays)}")
        tiles, attr, name = self.mapoverlays[overlay_name]
        self.overlays.append((tiles, name, attr))

    def add_marker(self, popup_location: tuple, popup_context: str = "Marker", 
                color: str = "darkred", tooltip: str = None, icon: str = "info-sign"):
        self.markers.append((popup_location, popup_context, color, tooltip, icon)) 

    def add_circle_marker(
        self,
        popup_location: tuple,
        popup_context: str = "Default",
        radius: int = 10,
        color: str = "blue",
        weight: int = 2,
        fill: bool = True,
        fill_color: str = "blue",
        fill_opacity: float = 0.6,
        tooltip : str = None
        ):
        self.circle_markers.append((popup_location, popup_context, radius, color, weight, fill, fill_color, fill_opacity,tooltip))



renderer = MapRender()
renderer.add_tile_layer("ArcGIS Street")

renderer.add_marker((51.5074, -0.1278), "London", tooltip="ASS", color="red")
renderer.add_marker((21.5074, -0.1278), "DWWDW", tooltip="SSSdsSS", color="red")
renderer.add_marker((51.5074, -0.1278), "London", color="red", tooltip="ASS", icon="info-sign")
renderer.add_marker((21.5074, -0.1278), "DWWDW", color="black", tooltip="SSSSS", icon="cloud")
renderer.add_circle_marker((11.5074, -0.1278), "Circle", radius=20, color="green")
renderer.render()
