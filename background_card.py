import customtkinter
import personal_module


class AddNewUser(personal_module.HoverFrame):
    def __init__(self, master, image_path, width=200, height=400, image_side="bottom", **kwargs):
        # Pass image_path and image_side directly to HoverFrame
        super().__init__(
            master, 
            height=height, 
            width=width, 
            image=image_path, 
            image_side=image_side, 
            **kwargs)
        self.pack_propagate(False)

        # Add any additional customization for AddNewUser
        self.configure(width=width, height=height)
        
if __name__ == "__main__":
    app = customtkinter.CTk()
    add_new_user_card = AddNewUser(app, width=200, height=400, square_image="icons/user.png", image_size=150)
    add_new_user_card.pack()
    app.geometry("400x450")
    app.mainloop()
