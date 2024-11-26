import customtkinter
import personal_module
from PIL import Image, ImageDraw, ImageFilter
import warnings



class ProfileFrame(customtkinter.CTkFrame):
    def __init__(self, 
                 master, 
                 width=200, 
                 height=400,
                 corner_radius=10,
                 **kwargs):
        
        self.master = master
        super().__init__(master,
                         width=width, 
                         height=height,
                         corner_radius=corner_radius,
                         **kwargs)
        
        self.pack_propagate(False)
        self.configure(fg_color="#181818")

        self.userpfp_label = customtkinter.CTkLabel(self, width=140, height=160,
                                                    fg_color="#202020", 
                                                    corner_radius=10,
                                                    text=" ")
        self.userpfp_label.pack(side="top",pady=10)
        self.userpfp = personal_module.loadImageSQR("user_profile_pics/christian_pfp.png", label_size=(140,160), corner_radius=10)
        self.userpfp_label.configure(image=self.userpfp)
        
      



if __name__== "__main__":
        Customtkinter = customtkinter.CTk(fg_color="#181818")
        Customtkinter.geometry("1380x620")

        frame1 = customtkinter.CTkFrame(Customtkinter, width=10, height=10)
        frame1.pack(expand=True, fill="both")

        Widget = ProfileFrame(frame1, width=200, height=600)
        Widget.pack()

        Customtkinter.mainloop()  