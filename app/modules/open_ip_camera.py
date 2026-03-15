from app.modules._Module_Creator import Module
from flask import url_for

class IPCameraModule(Module):
    def __init__(self):
        super().__init__(class_name="ip_camera")

    def create_card(self) -> str:
        ip_camera = self.create_input("ip_camera", "text", "camera Url", "url",col_size="s12 m12")
        add_camera = self.create_button("Add Camera", is_submit=True)
        return f"""
        <div class="col s12 card grey darken-2">
            <form action="{url_for('run_database')}" method="POST" target="map_frame"> """
