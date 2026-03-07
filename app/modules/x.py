from app.modules._Module_Creator import Module

class XModule(Module):
    def __init__(self):
        super().__init__(class_name="x")

    def create_card(self) -> str:
        search = self.create_input("x_search", "text", "Search term", "Search",col_size="s12 m12")
        lat = self.create_input("x_lat", "number", "0", "Latitude",step=0.000001)
        lng = self.create_input("x_lng", "number", "0", "Longitude",step=0.000001)
        run_btn = self.create_button("Search", "run_X()")
        
        return f"""
        <div class="col s12 card grey darken-2">
          <div class="row">
          <div class="nav grey darken-3 center-align">Search x</div>
            <div col s12> {search}</div>
            {lat}{lng}
            <div class="col s12 center-align">{run_btn}</div>
          </div>
        </div>
        """
