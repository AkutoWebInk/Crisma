import customtkinter
import personal_module
import reminders


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

        self.userpfp_label = customtkinter.CTkLabel(self, text=" ",
                                                    width=140, height=160, corner_radius=10,
                                                    fg_color="#202020")
        self.userpfp_label.pack(side="top",pady=10)
        
        
        self.userpfp = personal_module.loadImageSQR("user_profile_pics/christian_pfp.png", label_size=(140,160), corner_radius=10)
        self.userpfp_label.configure(image=self.userpfp)
        
        self.scroll_frame = personal_module.ScrollFrame(self, height=288, width=200,corner_radius=5, border_width=10,
                                                        fg_color="#181818", 
                                                        bg_color="#181818",
                                                        border_color="#161616", 
                                                        scrollbar=False)
        self.scroll_frame.pack(pady=10, padx=2, side="top")
        self.scroll_frame.canvas.configure(bg="#181818")
        self.scroll_frame.frame.configure(bg_color="#181818", corner_radius=40)
        
        self.reminders_test = ["Christian", "Leonardo", "Alex", "Lipe","Marina","Nita","aijrojaroijia", "aiorjioajrio"]

        self.load_reminders(self.reminders_test)
    
    def load_reminders(self, qtt):
        for i, reminder in enumerate(qtt):
            self.reminder = reminders.Sticker(self.scroll_frame.frame, 
                                              height=50, corner_radius=5,
                                              stickertxt=f"{reminder}", fg_color="#202020")
            self.reminder.pack(pady=5, padx=10)




if __name__== "__main__":
        Customtkinter = customtkinter.CTk(fg_color="#181818")
        Customtkinter.geometry("220x620")
        Customtkinter.attributes("-topmost", True)

        frame1 = customtkinter.CTkFrame(Customtkinter, width=10, height=10)
        frame1.pack(expand=True, fill="both")

        Widget = ProfileFrame(frame1, width=200, height=500)
        Widget.pack(pady=10,padx=10)

        Customtkinter.mainloop()  