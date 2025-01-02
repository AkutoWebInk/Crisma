import customtkinter
import cards.OriginalCard as OriginalCard



class User(OriginalCard):
    def __init__(self, master, image_path="icons/user.png",
                  local_db=None,**kwargs):

        # Pass image_path and image_side directly to HoverFrame
        super().__init__(master,
                         image_path=image_path, **kwargs)
        
        self.local_db=local_db
        


if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("900x500")
    card = User(app)
    card.pack()
    app.mainloop()