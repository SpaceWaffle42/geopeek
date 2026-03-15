from typing import Optional
class Create_Popup:
    # def __init__(self):
    #     pass
    def _shared_attr(self, lat, lng, url, desc, platform)-> str:
        """Store shared fields used by all card types."""
        self.lat = lat
        self.lng = lng
        self.url = url
        self.desc = f"<b>{desc}</b>"
        self.platform = platform

    def CreateText(
        self,
        desc: str = "",
        lat: str = "",
        lng: str = "",
        url: Optional[str] = "",
        platform: Optional[str] = "",

    )-> str:
        self._shared_attr(lat, lng, url, desc, platform)
        return self.card_wrapper(
            self.card_media_text() + self.card_action()
        )

    def CreateImg(
        self,
        img_src: str = "",
        desc: Optional[str] = "",
        lat: str = "",
        lng: str = "",
        url: Optional[str] = "",
        platform: Optional[str] = "",
    )-> str:
        self._shared_attr(lat, lng, url, desc, platform)
        self.img_src = img_src
        return self.card_wrapper(
            self.card_media_image() + self.card_content() + self.card_action()
        )

    def CreateVideo(
        self,
        video_src: str = "",
        desc: Optional[str] = "",
        lat: str = "",
        lng: str = "",
        url: Optional[str] = "",
        platform: Optional[str] = "",
    )-> str:
        self._shared_attr(lat, lng, url, desc, platform)
        self.video_src = video_src
        return self.card_wrapper(
            self.card_media_video() + self.card_content() + self.card_action()
        )

    def card_wrapper(self,inner:str = "")-> str:
      return f'''
        <div class="card" style="background-color: #424242; text-align: center; color: white; margin: 0; font-size: 12px">
        {inner}
        </div>
      '''
    def card_header(self)-> str:
        """Platform label + lat/lng"""
        return f"""
        <p class="center-align">{self.platform}</p>
        <span class="card-title center-align">Lat: {self.lat} &nbsp; Lng: {self.lng}</span>
        """

    def card_content(self)-> str:
      return f'''
        <div class="card-content">
          <p class="center-align">{self.desc}</p>
        </div>
      '''

    def card_action(self)-> str:
      return f'''
        <div class="card-action"style="background-color: #333333;">
          <b><a href="{self.url}"target="_blank" rel="noopener noreferrer">LINK</a></b>
        </div>
        '''


    def card_media_text(self)-> str:
      return f"""
      <div class="card-image">
        {self.card_header()}
      </div>
      <div class="card-content" style="width: 35rem;">
        <p class="center-align">{self.desc}</p>
      </div>
      """

    def card_media_image(self)-> str:
      return f"""
      <div class="card-image">
        {self.card_header()}
        <img src="{self.img_src}" style="max-width: 35rem;">
      </div>
      """

    def card_media_video(self)-> str:
      return f"""
      <div class="card-image">
        {self.card_header()}
        <iframe width="320" height="240" src="{self.video_src}" title="Embedded video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      """