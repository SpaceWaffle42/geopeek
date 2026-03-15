from app.modules._Module_Creator import Module
from flask import url_for

class YouTubeModule(Module):
    def __init__(self):
        super().__init__(class_name="youtube")

    def create_card(self) -> str:
        search = self.create_input("yt_search", "text", "Search term", "Search",col_size="s12 m12")
        lat = self.create_input("yt_lat", "number", "0", "Latitude",step=0.000001)
        lng = self.create_input("yt_lng", "number", "0", "Longitude",step=0.000001)
        run_btn = self.create_button("Search", is_submit=True)
        
        return f"""
        <div class="col s12 card grey darken-2">
            <form action="{url_for('run_database')}" method="POST" target="map_frame">
                <div class="row">
                    <div class="nav grey darken-3 center-align">Search YouTube</div>
                    <div class="col s12"> {search}</div>
                    {lat}{lng}
                    <div class="col s12 center-align">{run_btn}</div>
                </div>
            </form>
        </div>
        """
