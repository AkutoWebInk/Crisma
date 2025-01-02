import customtkinter
import profile_frame
import warnings
from PIL import Image, ImageDraw, ImageTk, ImageOps

def loadImage(path, size=(50, 50)):
    image = Image.open(path)
    image = image.resize(size)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(image)

def loadImageC(path, size=(50, 50)):
    try:
        image = Image.open(path).resize(size, Image.LANCZOS).convert("RGBA")
        # Create a fully transparent image as the base
        transparent_background = Image.new("RGBA", size, (0, 0, 0, 0))
        
        # Create a high-resolution mask
        upscale_factor = 4
        high_res_size = (size[0] * upscale_factor, size[1] * upscale_factor)
        high_res_mask = Image.new("L", high_res_size, 0)
        draw = ImageDraw.Draw(high_res_mask)
        draw.ellipse((0, 0, high_res_size[0], high_res_size[1]), fill=255)
        
        # Downscale the mask to the target size for anti-aliasing
        mask = high_res_mask.resize(size, Image.LANCZOS)
        
        # Create the circular image using the anti-aliased mask
        circular_image = Image.composite(image, transparent_background, mask)
        warnings.filterwarnings("ignore")
        return ImageTk.PhotoImage(circular_image)
    except Exception as e:
        print(f"loadImageC: Error encountered - {e}")
        return None

def loadImageSQR(path, label_size=(160, 200), corner_radius=15):
    try:
        # Ensure the image is square to fit within the smallest dimension
        size = min(label_size)  # Take the smaller of the width or height
        square_size = (size, size)

        # Open and resize the image to the calculated square size
        image = Image.open(path).resize(square_size, Image.LANCZOS).convert("RGBA")
        # Create a transparent square base for the mask
        transparent_background = Image.new("RGBA", square_size, (0, 0, 0, 0))

        # Create a rounded rectangular mask
        upscale_factor = 4  # High resolution for anti-aliasing
        high_res_size = (square_size[0] * upscale_factor, square_size[1] * upscale_factor)
        high_res_mask = Image.new("L", high_res_size, 0)
        draw = ImageDraw.Draw(high_res_mask)

        # Draw a rounded rectangle
        draw.rounded_rectangle((0, 0, high_res_size[0], high_res_size[1]), radius=corner_radius * upscale_factor, fill=255)
        # Downscale the mask for anti-aliasing
        mask = high_res_mask.resize(square_size, Image.LANCZOS)

        # Apply the rounded mask to the image
        rounded_image = Image.composite(image, transparent_background, mask)
        warnings.filterwarnings("ignore")
        return ImageTk.PhotoImage(rounded_image)
    except Exception as e:
        print(f"loadImageSQR: Error encountered - {e}")
        return None


class SlideMenu(customtkinter.CTkToplevel):
    def __init__(self, master, profile_picture, user_name, **kwargs):
        self.master = master
        self.user_name = user_name
        self.profile_picture = profile_picture
        
        super().__init__(master, **kwargs)
        
        self.pack_propagate(False)  # pack_propagates: shrinks accordingly to the size of its content, set to false
  
        # binds: return master width/height and reconfigures itself accordingly
        self.master.bind("<Configure>", self.updateSlideMenu_pos)

        self.attributes("-topmost", True)
        self.overrideredirect(True)

        # set an invisible color and configure the top level itself to it
        self.removed_color = "#111111"                               
        self.attributes("-transparentcolor", f"{self.removed_color}")
        self.configure(fg_color = f"{self.removed_color}")
        self.attributes("-alpha", 1) #alpha has nothing to do with it, i like to leave it here to control transparency as i code

        # divides the frame into 2 halves:
        # self.top_side=customtkinter.CTkFrame(self, fg_color=f"{self.removed_color}", corner_radius=0)
        # self.top_side.pack(fill="both",
        #                     side="top",
        #                     expand=True)

        # self.bottom_side=customtkinter.CTkFrame(self, fg_color=f"white", corner_radius=0)
        # self.bottom_side.pack(fill="both",
        #                         side="bottom",
        #                         expand=True)
        
        self.profile_frame = profile_frame.ProfileFrame(self, 
                                                        user_picture=self.profile_picture,
                                                        fg_color="#101010",
                                                        border_color="#181818",
                                                        border_width=1,
                                                        width=180, 
                                                        height=500)
        self.profile_frame.pack(pady=0, expand=True, fill="both")
        
        self.updateSlideMenu_pos()

    def updateSlideMenu_pos(self,event=None):
            
            self.master_width = self.master.winfo_width()
            self.master_height = self.master.winfo_height()
            
            self.master_x = self.master.winfo_x()
            self.master_y = self.master.winfo_y()
            
            self.slide_menu_width=self.winfo_width()
            self.slide_menu_height=self.master_height
            
            #print(f"Master's Width:{self.master_width}\nMasters Height: {self.master_height}")
            #print(f"Slide_menu width:{self.slide_menu_width}\nSlide_menu height:{self.slide_menu_height}")
            
            self.x_position = self.master_x+self.master_width-200
            self.y_position = self.master_y

            self.geometry(f"{self.slide_menu_width}x{self.master_height}+{self.x_position+7}+{self.y_position+32}")


if __name__=="__main__":
    app=customtkinter.CTk()
    app.geometry("1380x720")
    slide_menu=SlideMenu(app, profile_picture="local_data/user_profile_pics/christian_pfp.png", user_name="Christian")
    app.mainloop()