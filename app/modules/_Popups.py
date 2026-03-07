from typing import Optional
class Create_Popup:
    # def __init__(self):
    #     pass
    def CreateText(self, desc : str= "", lat : str="", lng : str="", url : Optional[str]="", platform : Optional[str]=""):
        self.lat = lat
        self.lng = lng
        self.url = url
        self.desc = desc
        self.platform = platform

    def CreateVideo(self, video_src : str= "", desc : Optional[str]= "", lat : str="", lng : str="", url : Optional[str]="", platform : Optional[str]=""):
        self.lat = lat
        self.lng = lng
        self.video_src = video_src
        self.url = url
        self.desc = desc
        self.platform = platform

    def CreateImg(self, img_src : str= "", desc : Optional[str]= "", lat : str="", lng :str="", url : Optional[str]="", platform : Optional[str]=""):
        self.lat = lat
        self.lng = lng
        self.url = url
        self.desc = desc
        self.img_src = img_src
        self.platform = platform
        return f"""
      <div class="card" style="background-color: #424242; text-align: center; color: white; margin: 0;">
        <div class="card-image">
        <p class="center-align">{self.platform}</p>
          <img src="{self.img_src}"style="max-width: 35rem";>
          <span class="card-title center-align">Lat:    {self.lat}  Lng:    {self.lng}</span>
        </div>
        <div class="card-content">
          <p class="center-align">{self.desc}</p>
        </div>
        <div class="card-action"style="background-color: #333333;">
          <b><a href="{self.url}">LINK</a></b>
        </div>
      </div>
    """