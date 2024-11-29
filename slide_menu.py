import customtkinter
import personal_module
import profile_frame
import warnings
from PIL import Image, ImageDraw, ImageTk, ImageOps

def loadImage(path, size=(50,50)):
    image = Image.open(path)
    image = image.resize(size)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(image)

def loadImageC(path, size=(50, 50)):
    image = Image.open(path).resize(size).convert("RGBA")
        # Create a fully transparent image as the base
    transparent_background = Image.new("RGBA", size, (0, 0, 0, 0))
    # Create a mask for circular cropping
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    
    circular_image = Image.composite(image, transparent_background, mask)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(circular_image)


class SlideMenu(customtkinter.CTkToplevel):
    def __init__(self, master, profile_picture, user_name, **kwargs):
        self.master = master
        self.user_name = user_name
        self.profile_picture = profile_picture
        
        super().__init__(master, **kwargs)
        
        self.pack_propagate(False)  # pack_propagates: shrinks accordingly to the size of its content, set to false

        self.return_master_winfo() #initialy returns the master w/h and configures itself accordingly
        
        # binds: return master width/height and reconfigures itself accordingly
        self.master.bind("<Configure>", self.return_master_winfo)

        self.attributes("-topmost", True)
        self.overrideredirect(True)

        # set an invisible color and configure the top level itself to it
        self.removed_color = "#111111"                               
        self.attributes("-transparentcolor", f"{self.removed_color}")
        self.configure(fg_color = f"{self.removed_color}")
        self.attributes("-alpha", 1) #alpha has nothing to do with it, i like to leave it here to control transparency as i code

        # divides the frame into 2 halves:
        self.top_side=customtkinter.CTkFrame(self, fg_color=f"{self.removed_color}", corner_radius=0)
        self.top_side.pack(fill="both",
                           side="top",
                           expand=True)

        self.bottom_side=customtkinter.CTkFrame(self, fg_color=f"{self.removed_color}", corner_radius=0)
        self.bottom_side.pack(fill="both",
                              side="bottom",
                              expand=True)
        
        self.profile_frame = profile_frame.ProfileFrame(self.top_side, width=180, height=500)
        self.profile_frame.pack(side="top",pady=10)


    def return_master_winfo(self,event=None):
            try:
                self.master.update_idletasks()

                self.master_width = self.master.winfo_width()
                self.master_height = self.master.winfo_height()
               
                
                self.side_menu_initial_place = self.master.winfo_x() + self.master.winfo_width() + 8 
                self.sided_menu_locked_height = self.master.winfo_y()
                self.config_geometry()
           
            except Exception:
                pass
            return

    def config_geometry(self):
        # Set initial width and height
        self.master.update_idletasks()
        self.geometry(f"200x{self.master_height}+{self.side_menu_initial_place - 200}+{self.sided_menu_locked_height+31}")

if __name__=="__main__":
    app=customtkinter.CTk()
    app.geometry("1380x720")
    slide_menu=SlideMenu(app, profile_picture="user_profile_pics/christian_pfp.png", user_name="Christian")
    app.mainloop()