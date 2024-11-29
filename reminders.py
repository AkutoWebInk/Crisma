import customtkinter
import personal_module


class Sticker(customtkinter.CTkFrame):
    def __init__(self, master, 
                 witdth=200, 
                 height=100,
                 fg_color="#181818",
                 stickertxt=None,
                 corner_radius=5,
                 **kwargs):

        self.width=witdth
        self.height=height
        self.fg_color=fg_color
        self.text = stickertxt
        self.corner_radius=corner_radius

        super().__init__(master, 
                         height=self.height, 
                         width=self.width,
                         corner_radius=self.corner_radius,
                         fg_color=f"{self.fg_color}",
                         **kwargs)

        self.pack_propagate(False)
        
        self.button_ico = personal_module.loadImage("icons/no_user_icon.png", size=(20,20))
        self.button = customtkinter.CTkButton(self, width=15, height=15,
                                              fg_color="transparent", hover=False,
                                              text=None, image=self.button_ico,
                                              command=self.destroy)
        
        self.button.pack(side="right", anchor="n")

        self.inside = customtkinter.CTkLabel(self, fg_color=f"{self.fg_color}", corner_radius=10, text=f"{self.text}")
        self.inside.pack(fill="both", expand= True, pady=5, padx=5)











if __name__=="__main__":
    app = customtkinter.CTk()
    app.geometry("400x400")

    sticker = Sticker(app, witdth=300, height=200)
    sticker.pack()

    app.mainloop()
