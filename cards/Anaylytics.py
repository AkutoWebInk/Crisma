import customtkinter
import personal_module
import cards.OriginalCard as OriginalCard
 
class Anaylytics(OriginalCard):
    def __init__(self, master, 
                 image_path="icons/anaylytics.png",
                 local_db=None,
                 search_widget=None, 
                 **kwargs):
        super().__init__(master, image_path=image_path, **kwargs)