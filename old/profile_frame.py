import customtkinter
import personal_module
from PIL import Image, ImageDraw, ImageFilter
import warnings



class ProfileFrame(customtkinter.CTkFrame):
    def __init__(self, 
                 master, 
                 width=100, 
                 height=110, 
                 username=None,
                 userprofilepicture=None,
                 canvas_color=None,
                 **kwargs):
        
        self.master = master
        self.username=username
        self.userprofilepicture=userprofilepicture
        self.canvas_color=canvas_color

        super().__init__(master,
                         width=width, 
                         height=height, 
                         **kwargs)
        self.pack_propagate(False)

        self.configure(fg_color="transparent")
        
        self.canvas_height=int(height-20)

        self.profile_background_canvas = customtkinter.CTkCanvas(self,highlightthickness=0,bg="#111111",height=f"{self.canvas_height}")
        self.profile_background_canvas.pack(fill="both", pady=0)

        # Bind the <Configure> event to resize image when the canvas size changes
        self.profile_background_canvas.bind("<Configure>", self.resize_image)
        
        self.username_label = customtkinter.CTkLabel(self,
                                                     text=f"{self.username}",
                                                     fg_color="transparent",
                                                     bg_color="transparent",
                                                     font=("Monaspace", 16, "bold"),
                                                     corner_radius=10)
        self.username_label.pack(expand=False,fill="x", side="bottom")

   
   
    def resize_image(self, event):
            
            canvas_width = event.width
            canvas_height = event.height

            
            # Clear any previous images on the canvas
            self.profile_background_canvas.delete("all")
            
            
            # Create and center the image on the canvas
            self.canvas_image = personal_module.loadImage("utilities/green_circle.png", size=(100, 100))
            self.profile_background_canvas.create_image(canvas_width/2, 
                                                        canvas_height/2, 
                                                        image=self.canvas_image)
            
            self.canvas_userprofilepicture = personal_module.loadImageC(f"{self.userprofilepicture}", size=(80,80))

            self.profile_background_canvas.create_image(canvas_width/2,
                                                        canvas_height/2,
                                                        image=self.canvas_userprofilepicture)

            
            # Keep a reference to the image to prevent garbage collection
            self.profile_background_canvas.image = self.canvas_image
            self.profile_background_canvas.image = self.profile_background_canvas
            return
      



if __name__== "__main__":
        Customtkinter = customtkinter.CTk(fg_color="#181818")
        Customtkinter.geometry("1380x720")
        frame1 = customtkinter.CTkFrame(Customtkinter, width=200, height=600)
        frame1.pack()
        Widget = ProfileFrame(frame1,userprofilepicture="user_profile_pics/tio_christio.png", username="Christian")
        Widget.pack()

        Customtkinter.mainloop()  