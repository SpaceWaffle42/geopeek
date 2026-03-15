from app.modules._Module_Creator import Module
from flask import url_for, redirect

class DatabaseModule(Module):
    def __init__(self, countries: list[tuple[str, str]] | None = None):
        super().__init__(class_name="database")
        self.countries = countries or []

    def create_card(self) -> str:
        search = self.create_input("db_search", "text", "Search term", "Search",col_size="s12 m12")
        platform_youtube = self.create_checkbox("YouTube", id_name="youtube", name="platforms", value="YouTube")
        platform_x = self.create_checkbox("X", id_name="x", name="platforms", value="Twitter")
        platform_g_news = self.create_checkbox("Google News", id_name="g_news", name="platforms", value="Google")
        platform_camera = self.create_checkbox("IP Camera", id_name="camera", name="platforms", value="IPCamera")
        platforms = f"""
        <div class="col s12">
          <label>Platforms</label>
          {platform_youtube}
          {platform_x}
          {platform_g_news}
          {platform_camera}
        </div>
        """
        media_image = self.create_checkbox("Image",id_name="image",name="type",value="image")
        media_video = self.create_checkbox("Video",id_name="video",name="type",value="video")
        media_text = self.create_checkbox("Text",id_name="text",name="type",value="text")
        media_types = f"""
        <div class="col s12">
          <label>Media</label>
          {media_image}
          {media_video}
          {media_text}
        </div>
        """

        start_date = self.create_date(date_label="Start date",class_name="start_date",id_name="start_date",col_size="s6")
        end_date = self.create_date(date_label="End date",class_name="end_date",id_name="end_date",col_size="s6")
        country_options = [("All", "All")] + self.countries
        country = self.create_select(country_options,"Country",id_name="country_search",col_size="s12")

        lat = self.create_input("db_lat", "number", "0", "Latitude",step=0.000001)
        lng = self.create_input("db_lng", "number", "0", "Longitude",step=0.000001)

        run_btn = self.create_button("Search", is_submit=True)
        
        return f"""
        <div class="col s12 card grey darken-2">
          <div class="row">
          <form action="{url_for('run_database')}" method="POST" target="map_frame">
            <div class="nav grey darken-3 center-align">Search Database</div>
            <div class="col s12">{search}</div>
            {lat}{lng}
            {country}
            {platforms}
            {media_types}
            {start_date}
            {end_date}
            <div class="col s12 center-align">{run_btn}</div>
          </form>
          </div>
        </div>
        """
