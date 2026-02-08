from app.module import Mapper

renderer = Mapper.MapRender()
renderer.add_tile_layer("Esri WorldImagery")
renderer.add_marker((51.5074, -0.1278), "London")
renderer.add_marker((12.3456,7.8901),"HEHEHOHOHAHA")
renderer.render()
