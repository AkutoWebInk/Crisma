import customtkinter
import personal_module

class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        self.master = master
        super().__init__()

        self.title("Login")
        
        self.resizable(False, False)
        
        self.attributes("-topmost", True)
        self.attributes("-alpha", 1)
        self.configure(fg_color="#101010")
        self.centeronlaunch()
        self.no_user_image = "icons/no_user_icon.png"

        self.left_side = personal_module.HoverFrame(self,
                                                    fg_color="#101010",
                                                    bg_color="transparent",
                                                    border_color="#101010",
                                                    width=200,
                                                    height=360, 
                                                    profile_image=f"{self.no_user_image}",
                                                    profile_image_side="top")
        
        self.right_side = personal_module.HoverFrame(self)
        
        self.left_side.pack(side="left")
        self.right_side.pack(side="right", expand=True, fill="both")
        
        self.right_side_image=personal_module.loadImage("user_profile_pics/login_background.jpg", size=(600,600))

        self.right_side_label=customtkinter.CTkLabel(self.right_side,
                                                     width=1,height=1,  corner_radius=5,
                                                     image=self.right_side_image, text=" ")
        self.right_side_label.pack(expand=True)



        
        self.username_entry = customtkinter.CTkEntry(self.left_side, corner_radius=20, fg_color="#121212",
                                                     border_width=0, placeholder_text="Funcionário", placeholder_text_color="white",
                                                     text_color="white",justify="center", font=("Monaspace", 16),
                                                     width=180)
        
        self.password_entry = customtkinter.CTkEntry(self.left_side, corner_radius=20, fg_color="#121212",
                                                     border_width=0, placeholder_text="Senha", placeholder_text_color="white",
                                                     text_color="white", justify="center", font=("Monaspace", 16), show="*",
                                                     width=180)
        

        self.x_value, self.xx_value = -210, -210    

        self.username_entry.place(x=self.x_value, y = 200)
        self.password_entry.place(x=self.xx_value, y = 240)

        self.slide_username()
        self.show_password()








    def update_user_profilepic(self, pic_path=None):
        if pic_path:
            self.user_pic = personal_module.loadImageC(f"{pic_path}", size=(155,155))
            self.left_side.profile_image_label.configure(image=self.user_pic)
        else:
            self.user_pic = personal_module.loadImageC(("icons/no_user_icon.png"), size=(180,180))
            self.left_side.profile_image_label.configure(image=self.user_pic)

    def slide_username(self):
        if self.x_value<10:
            self.x_value += 1
            self.username_entry.place_configure(x=self.x_value)
            self.after(1, self.slide_username)
    
    def show_password(self):
        if self.xx_value<10:
            self.xx_value +=1
            self.password_entry.place_configure(x=self.xx_value)
            self.after(1, self.show_password)

    def catch_username(self):
        self.user_username = self.username_entry.get()
        return self.user_username

    def catch_password(self):
        self.user_password=self.password_entry.get()
        return self.user_password

    def centeronlaunch(self):
        #return system screen info
        app=customtkinter.CTk()
        self.height = app.winfo_screenheight()
        self.width = app.winfo_screenwidth()
        self.widthoffset = (self.width-800)//2 
        self.heightoffset = (self.height-400)//2
        self.geometry(f"800x400+{self.widthoffset}+{self.heightoffset}")
        return 


if __name__=="__main__":
    app = customtkinter.CTk()
    login_window = LoginWindow(app)
    app.mainloop()