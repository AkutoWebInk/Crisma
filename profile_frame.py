import customtkinter
import personal_module
import reminders


class ProfileFrame(customtkinter.CTkFrame):
    def __init__(self, 
                 master, 
                 width=200, 
                 height=400,
                 corner_radius=9,
                 user_picture=None,
                 reminders=None,
                 notifications=None,
                 fg_color="#101010",
                 border_color=None,
                 border_width=0,
                 **kwargs):
        
        self.user_picture=user_picture
        self.master=master
        self.reminders=reminders
        self.notifications=notifications
        self.border_color=border_color
        self.border_width=border_width
        self.fg_color=fg_color
        
        super().__init__(master,
                         width=width, 
                         height=height,
                         corner_radius=corner_radius,
                         border_color=border_color,
                         border_width=border_width,
                         **kwargs)
        
        self.pack_propagate(False)
        self.configure(fg_color=f"{self.fg_color}")
        self.userpfp_label = customtkinter.CTkLabel(self, text=" ",
                                                    width=140, height=160, corner_radius=10,
                                                    fg_color="#181818")
        self.userpfp_label.pack(side="top",pady=10)
        
        self.userpfp = personal_module.loadImageSQR(f"{self.user_picture}", label_size=(140,160), corner_radius=10)
        self.userpfp_label.configure(image=self.userpfp)
        
        self.scroll_frame = personal_module.ScrollFrame(self, height=288, width=200,corner_radius=5, border_width=10,
                                                        fg_color=f"{self.fg_color}", 
                                                        bg_color=f"{self.fg_color}",
                                                        border_color=f"{self.fg_color}", 
                                                        scrollbar=False)
        self.scroll_frame.pack(pady=10, padx=2, side="top")
        self.scroll_frame.canvas.configure(bg=f"{self.fg_color}")
        self.scroll_frame.frame.configure(bg_color=f"{self.fg_color}", corner_radius=40)
        
        self.reminders_test = ["Christian", "Leonardo", "Alex", "Lipe", "Marina", "Nita"]

        self.load_reminders(self.reminders_test)
    
    def load_reminders(self, qtt):
        for i, reminder in enumerate(qtt):
            self.reminder = reminders.Sticker(self.scroll_frame.frame, 
                                              height=50, corner_radius=5,
                                              stickertxt=f"{reminder}", fg_color="#181818")
            self.reminder.pack(pady=2, padx=10)




if __name__== "__main__":
        Customtkinter = customtkinter.CTk(fg_color="#181818")
        Customtkinter.geometry("220x620")
        Customtkinter.attributes("-topmost", True)

        frame1 = customtkinter.CTkFrame(Customtkinter, width=10, height=10)
        frame1.pack(expand=True, fill="both")

        Widget = ProfileFrame(frame1, width=200, height=500)
        Widget.pack(pady=10,padx=10)

        Customtkinter.mainloop()  