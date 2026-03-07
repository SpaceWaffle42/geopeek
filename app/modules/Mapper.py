import folium
from folium.plugins import MarkerCluster

from typing import Optional


class MapRender:
    """Folium setup, change width and height here"""

    maplayers = {
        "OSM": (
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            "OSM",
        ),
        "OpenTopoMap": (
            "https://a.tile.opentopomap.org/{z}/{x}/{y}.png",
            'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (CC-BY-SA)',
            "TopoMap",
        ),
        "Wikimedia": (
            "https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png",
            '<a href="https://wikimediafoundation.org/wiki/Maps_Terms_of_Use">Wikimedia</a>',
            "Wikimedia",
        ),
        "OpenFreeMap": (
            "https://tiles.openfreemap.org/osm/{z}/{x}/{y}.png",
            '&copy; <a href="https://openfreemap.org">OpenFreeMap</a>',
            "OpenFreeMap",
        ),
        "Stadia Alidade Smooth": (
            "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png",
            '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            "Stadia Smooth",
        ),
        "Stadia Alidade Smooth Dark": (
            "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
            '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            "Stadia Dark",
        ),
        "ArcGIS Street": (
            "https://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            "ArcGIS Street",
        ),
        "Esri WorldImagery": (
            "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "Tiles &copy; Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, GIS User Community",
            "Esri Satellite",
        ),
        "MtbMap": (
            "http://tile.mtbmap.cz/mtbmap_tiles/{z}/{x}/{y}.png",
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & USGS',
            "MtbMap",
        ),
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

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        location: tuple[float, float] = (0.0000, 0.0000),
        zoom_start: int = 2,
        max_zoom: int = 18,
        min_zoom: int = 2,
    ):
        self.width = f"{width}%"
        self.height = f"{height}%"
        self.location = location
        self.m = None
        self.markers = []
        self.circle_markers = []
        self.circle = []
        self.tiles = []
        # self.overlays = []
        self.zoom_start = zoom_start
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.marker_cluster = None

    def render(self):
        """Folium render, the markers and layers are added here and this should be called last"""

        self.m = folium.Map(
            width=self.width,
            height=self.height,
            location=self.location,
            zoom_start=self.zoom_start,
            max_zoom=self.max_zoom,
            min_zoom=self.min_zoom,
        )
        self.marker_cluster = MarkerCluster(name="Markers").add_to(self.m)

        for tiles, name, attr, overlay, min_zoom, max_zoom in self.tiles:
            folium.TileLayer(
                tiles=tiles,
                attr=attr or f"© {name}",
                name=name,
                overlay=overlay,
                min_zoom=min_zoom,
                max_zoom=max_zoom,
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
                loc,
                popup=text,
                tooltip=tooltip,
                icon=folium.Icon(color=color, icon=icon),
            ).add_to(self.marker_cluster)

        for (
            loc,
            text,
            radius,
            color,
            weight,
            fill,
            fill_color,
            fill_opacity,
            tooltip,
        ) in self.circle_markers:
            folium.CircleMarker(
                loc,
                popup=text,
                radius=radius,
                color=color,
                weight=weight,
                fill=fill,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                tooltip=tooltip,
            ).add_to(self.m)

        for (
            loc,
            text,
            radius,
            color,
            weight,
            fill,
            fill_color,
            fill_opacity,
            tooltip,
        ) in self.circle:
            folium.Circle(
                loc,
                popup=text,
                radius=radius,
                color=color,
                weight=weight,
                fill=fill,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                tooltip=tooltip,
            ).add_to(self.m)

        folium.LayerControl().add_to(self.m)

        html_content = self.m.get_root().render()
        with open("templates/_map.html", "w") as f:
            f.write(html_content)
        return self

    def add_tile_layer(
        self,
        layer_name: str = "OSM",
        min_zoom: Optional[int] = None,
        max_zoom: Optional[int] = None,
    ):
        """Select layer by name, for example: 'OpenTopoMap', 'OSM', 'Esri WorldImagery'"""
        if layer_name not in self.maplayers:
            raise ValueError(f"Choose from {list(self.maplayers)}")
        tiles, attr, name = self.maplayers[layer_name]
        self.tiles.append((tiles, name, attr, False, min_zoom, max_zoom))

    def add_overlay(self, overlay_name: Optional[str] = "LiDAR UK"):
        """Adds an overlay"""
        if overlay_name not in self.mapoverlays:
            raise ValueError(f"Overlays: {list(self.mapoverlays)}")
        tiles, attr, name = self.mapoverlays[overlay_name]
        self.overlays.append((tiles, name, attr))

    def add_marker(
        self,
        popup_location: tuple,
        popup_context: str = "Marker",
        color: str = "darkred",
        tooltip: str = None,
        icon: str = "info-sign",
    ):
        """Add a marker.
        For all bootstrap Icons, visit: https://getbootstrap.com/docs/3.3/components/
        """
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
        tooltip: str = None,
    ):
        """Add a circle marker (measured in pixels)"""

        self.circle_markers.append(
            (
                popup_location,
                popup_context,
                radius,
                color,
                weight,
                fill,
                fill_color,
                fill_opacity,
                tooltip,
            )
        )

    def add_circle(
        self,
        popup_location: tuple,
        popup_context: str = "Default",
        radius: int = 10,
        color: str = "blue",
        weight: int = 2,
        fill: bool = True,
        fill_color: str = "blue",
        fill_opacity: float = 0.6,
        tooltip: str = None,
    ):
        """Add a circle marker (measured in KM)"""

        self.circle.append(
            (
                popup_location,
                popup_context,
                radius,
                color,
                weight,
                fill,
                fill_color,
                fill_opacity,
                tooltip,
            )
        )
