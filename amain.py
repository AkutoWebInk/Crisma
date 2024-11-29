import customtkinter
import personal_module
import login_window
import database
import background_card
import slide_menu


class InterfaceConfig:
        def __init__(self, master, server):
                self.master = master
                self.server = server
                self.master.title("Ákuto Manager")
                self.centeronlaunch()
        
        def centeronlaunch(self):
                self.height = self.master.winfo_screenheight()
                self.width = self.master.winfo_screenwidth()
                self.widthoffset = (self.width-1280)//2 
                self.heightoffset = (self.height-420)//2
                self.master.geometry(f"1280x420+{self.widthoffset}+{self.heightoffset}")
                return
                
class UserInterface(InterfaceConfig):
        def __init__(self, master, server):
                
                super().__init__(master, server)

                self.background_frame=customtkinter.CTkFrame(self.master,fg_color="#101010")
                self.background_frame.pack(expand=True, fill="both")
                
                self.current_background = None
                self.static_background()

                self.master.bind("<Button-3>", self.right_click_context_menu)
                self.master.bind("<Control-n>", self.load_add_item_window)
                


                self.items_returned_by_search = [] # List of items returned by the searchDb()
                
                self.search_widget = customtkinter.CTkEntry(self.master, width=120, height=25, fg_color="#101010", border_color="#202020", border_width=1)
                self.search_widget.pack(side="left", anchor = "s", pady=5, padx=5)
                self.search_widget.bind("<KeyRelease>", self.catch_user_search) 
                
                
                
                self.button1 = customtkinter.CTkButton(self.master, width=25, height=25, fg_color="#101010", text="Static", command=self.static_background)
                self.button2 = customtkinter.CTkButton(self.master, width=25, height=25, fg_color="#101010", text="Scrollable", command=self.initialize_scrollable_frame)
                
                self.button1.pack(anchor="s", side="left", pady=5,padx=2.5)
                self.button2.pack(anchor="s", side="left", pady=5,padx=2.5)

        
        def catch_user_search(self,event):

                self.user_search = self.search_widget.get()
                self.request_search = self.server.searchDb(user_search = f"{self.user_search}")
                self.load_items_list(self.request_search)
                
        def load_items_list(self,items):
                self.scrollable_frame.configure_frame(event=None)
                for item in self.items_returned_by_search:
                        item.destroy()         
                self.items_returned_by_search.clear()

                for i in items:
                        self.item_frame = personal_module.HoverFrame(self.scrollable_frame.frame,
                                                                     height= 32,
                                                                     width= self.scrollable_frame.cget("width"),
                                                                     expand_orientation="vertical",
                                                                     fg_color="#101010",
                                                                     hover_color="#202020",
                                                                     border_color= "#181818")
                        self.item_frame.pack(pady=1,padx=1,fill="both",expand=True)

                        self.items_returned_by_search.append(self.item_frame)
                self.scrollable_frame.canvas.yview_moveto(0)
                      
        def initialize_scrollable_frame(self):
                self.destroy_current_background()
                self.scrollable_frame = personal_module.ScrollFrame(self.background_frame,border_color="#181818")
                self.scrollable_frame.pack(pady=5, padx=1,fill="both", expand=True)
                self.load_items_list(self.server.searchDb())
                self.current_background = self.scrollable_frame
        
        def static_background(self):
                        self.destroy_current_background()
                        for i in range(5):
                        
                                self.card = background_card.AddNewUser(self.background_frame, 
                                                                width=200, height=300, 
                                                                image_path="icons/user.png", image_size=150, 
                                                                hover_color = "#121212", expand_orientation="card")
                                self.card.pack(pady=10, padx=10, side="top", anchor="nw")
                                self.current_background=self.card
                                return self.current_background
                       
                        '''
                        Create the cards with images on them and etc, with different sizes for cool effect,
                        (maybe inside personal_module), then on the main program i create a list of cards that will be on the static background,
                        and define a fuction as something like:
                        
                        list_of_cards = [personal_module.card1, 
                                                                personal_module.card2, 
                                                                                        personal_module.card3,...]
                        def load_cards(self):
                        
                                for i in range(list_of_cards):
                                        i.pack(after="i",pady=5, padx=5) obs: #i side by side with the previous i
                        '''
        
        def destroy_current_background(self):
                if self.current_background:
                        self.current_background.destroy()  # Destroy the widget
                        self.current_background = None  # Clear the reference
                return self.current_background

        def load_add_item_window(self,event=None):
                self.add_item_window = personal_module.AddItemWindow(self.master)
        
        def right_click_context_menu(self,event=None):
                self.context_menu = personal_module.ContextMenu(None)

class LoginValidation(database.ServerAccess):
        def __init__(self,master):
                self.master=master
                
                super(). __init__()

                self.login_window = login_window.LoginWindow(self.master)
                self.login_window.bind("<KeyRelease>", self.request_user_info)
                self.side_menu=None

        def request_user_info(self, event):
                self.user = self.login_window.catch_username()
                self.returned_user_info = database.ServerAccess.searchDb_username(self, username=f"{self.user}")

                if self.returned_user_info:
                        self.user_name = self.returned_user_info[0]
                        self.user_password = self.returned_user_info[1]
                        self.user_profilepic_path = self.returned_user_info[2]

                        # Update profile picture in the login window
                        self.login_window.update_user_profilepic(self.user_profilepic_path)

                        # Load side menu if it doesn't already exist
                        if not hasattr(self, 'side_menu') or self.side_menu is None:
                                self.side_menu = slide_menu.SlideMenu(self.master, 
                                                                      profile_picture=f"{self.user_profilepic_path}", 
                                                                      user_name=f"{self.user_name}")
                                

                else:
                        print("User not found.")
                        # Update profile picture to default in the login window
                        self.login_window.update_user_profilepic()

                        # Destroy the side menu if it exists
                        if hasattr(self, 'side_menu') and self.side_menu is not None:
                                self.side_menu.destroy()
                                self.side_menu = None

        
        def validate_password(self, event):
                self.password = self.login_window.catch_password()
                print(f"{self.password}")
                if self.user_password == self.password:
                        self.user = "Validated"
                        return self.user






if __name__== "__main__":
        Local_Server = database.ServerAccess()
        
        Customtkinter = customtkinter.CTk(fg_color="#181818")
        
        WindowConfig = InterfaceConfig(Customtkinter, Local_Server)
        
        Visual = UserInterface(Customtkinter, Local_Server)

        Login = LoginValidation(Customtkinter)

        Customtkinter.mainloop()        