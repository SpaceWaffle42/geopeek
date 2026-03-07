from app.modules._Module_Creator import Module

class DatabaseModule(Module):
    def __init__(self):
        super().__init__(class_name="database")

    def create_card(self) -> str:
        search = self.create_input("db_search", "text", "Search term", "Search",col_size="s12 m12")
        platforms = self.create_checkbox("test",id_name="platforms")
        start_date = self.create_date(date_label="Start date",id_name="start_date",col_size="s6")
        end_date = self.create_date(date_label="End date",id_name="end_date",col_size="s6")
        country = self.create_select(["All"],"db_search",id_name="db_search",col_size="s12")

        lat = self.create_input("db_lat", "number", "0", "Latitude",step=0.000001)
        lng = self.create_input("db_lng", "number", "0", "Longitude",step=0.000001)


        run_btn = self.create_button("Search", "run_database()")
        
        return f"""
        <div class="col s12 card grey darken-2">
          <div class="row">
            <div class="nav grey darken-3 center-align">Search Database</div>
            <div> {search}</div>
            {lat}{lng}
            {country}
            {platforms}
            {start_date}
            {end_date}
            <div class="col s12 center-align">{run_btn}</div>
          </div>
        </div>
        """
