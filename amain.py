import customtkinter
import cards.User
import personal_module
import login_window
import local_data.database.database as database
from cards import *
import slide_menu
import requests
import sound 


class InterfaceConfig:
        def __init__(self, master, db):
                self.master = master
                self.db = db
                self.centeronlaunch()
       
        def centeronlaunch(self):
                self.height = self.master.winfo_screenheight()
                self.width = self.master.winfo_screenwidth()
                self.widthoffset = (self.width-1820)//2 
                self.heightoffset = (self.height-450)//2
                self.master.geometry(f"1366x450+{self.widthoffset}+{self.heightoffset}")
                self.master.overrideredirect(False)
                self.master.attributes("-fullscreen", False)

                return self.height,self.width
        
        def initialize_main_program(self):
                self.master.mainloop()

class UserInterface(InterfaceConfig):
        def __init__(self, master, db):
                
                self.master = master
                self.master.update_idletasks()
                self.db=db
                
                InterfaceConfig.__init__(self, master, db)
                # current background on init set to none
                self.current_background = None
                # empty list of items currently packed in the background
                self.card_in_display=None
                self.packed_cards = []
                self.loaded_cards = []
                
                self.background_frame=customtkinter.CTkFrame(self.master,
                                                             width=self.master.winfo_width(),
                                                             height=self.master.winfo_height()-32,
                                                             fg_color="white",
                                                             border_color="#101010",
                                                             border_width=1)
                self.background_frame.pack(expand=True, fill="both",padx=0)
                
                self.search_widget = customtkinter.CTkEntry(self.master, width=120, height=25, fg_color="#101010", border_color="#202020", border_width=1)
                self.search_widget.pack(side="bottom", anchor="w", pady=5, padx=5)
               
                self.list_of_cards = [
                        cards.Inventory(master=self.background_frame, 
                                        local_db=self.db, 
                                        search_widget=self.search_widget,
                                        mainFile_path=self),

                        cards.User(master=self.background_frame,
                                   local_db=self.db, 
                                   mainFile_path=self),
                        
                        cards.Anaylytics(master=self.background_frame, 
                                         local_db=self.db, 
                                         search_widget=self.search_widget,
                                         mainFile_path=self),
                        
                        cards.OriginalCard(master=self.background_frame,
                                           mainFile_path=self),
                        ]
                
                self.initialize_cards()
                self.master.after(200, self.delayed_call)

        def terminal_cards(self):
                print(f"Loaded cards: {self.loaded_cards}")
                print(f"Packed cards: {self.packed_cards}")

        def initialize_cards(self):
                #load cards
                for card in self.list_of_cards:
                        self.loaded_cards.append(card)
                # pack cards
                for card in self.loaded_cards:
                        card.pack(side="left", anchor="n", pady=3,padx=3, fill=None, expand=False)
                        self.packed_cards.append(card)

        def delayed_call(self, event=None):
                # Don't trigger the resize if the Inventory card is active
                if self.card_in_display is not None and isinstance(self.card_in_display, cards.Inventory):
                        return
                self.master.unbind("<Configure>")
                self.master.after(10, self.resize_home_screen)
        
        def resize_home_screen(self):
                
                self.master_winfo = self.get_master_winfo()
                self.background_frame.configure(width=self.master_width, height=self.master_height-32)

                self.master.after(1000,lambda: self.master.bind("<Configure>",self.delayed_call))
                self.current_background=self.background_frame
                return self.current_background
        
        def get_master_winfo(self, event=None):
                self.master.update_idletasks()
                self.master_height = self.master.winfo_height()
                self.master_width = self.master.winfo_width()
                
                self.n_rows = self.master_width//200
                self.n_columns=self.master_height//300
                
                return self.master_height, self.master_width, self.n_rows, self.n_columns
        
class LoginValidation(database.Access):
        def __init__(self, master):

                self.master = master
                
                super(). __init__()
                
                #raise Login Window
                self.login_window = login_window.LoginWindow(self.master)
                self.login_window.username_entry.bind("<KeyRelease>", self.localDb_requestInfo)
                self.login_window.password_entry.bind("<KeyRelease>", self.localDb_requestPassword)
                self.slide_menu = None

        def localDb_requestInfo(self, event):
                #catches the username from the login-window-entry
                self.attempt_user = self.login_window.catch_username()
                #passes the user written inside the entry /\ as a paramether to a function inside the database that searchs for a match:
                self.user_info = database.Access.searchDb_username(self, username=f"{self.attempt_user}") #returns user id and pfp only
                # Update profile picture in the login window
                if self.user_info is not None:
                        try:
                                self._profilePic, self.userId = self.user_info
                                self.login_window.switch_green(widget=self.login_window.username_entry)
                                self.login_window.update_user_profilepic(self.user_profilePic)
                                self.login_window.slide_password()
                                return self.userId
                        except:
                                pass
                else:
                        # Update profile picture to default inside the login window
                        if self.login_window.username_entry.cget("fg_color") == "#002400":
                                self.login_window.return_fg_color(widget=self.login_window.username_entry)
                        self.login_window.update_user_profilepic()
                        self.login_window.unslide_password()
                        
        def localDb_requestPassword(self, event):
        # Catch the entered password
                self.attempt_password = self.login_window.catch_password()

                # Check the password in the database using the already set userId
                self.found_password = self.searchDb_userPassword(id=self.userId, password=self.attempt_password)

                if self.found_password is not None:
                        self.login_window.switch_green(widget=self.login_window.status_bar)
                        print(f"\nPassword matched with local Database: {self.found_password}"
                               "\nCALLING API for 2-step validation (server Database):")
                        
                        self.API_searchById(user_id=self.userId, user_password=self.found_password)
                else:
                        if self.login_window.status_bar.cget("fg_color") == "#002400":
                                self.login_window.return_fg_color(widget=self.login_window.status_bar)
                        print(f"Incorrect password: {self.attempt_password}")

        def API_searchById(self, user_id, user_password):
                try:
                        self.params = {f"id":user_id, "password": user_password}
                        self.api_response = requests.get("http://localhost:8080/api/userById", params=self.params)
                        
                        if self.api_response.status_code == 200:
                                print(f"\nAPI: method called-> findByID()"
                                      f"\nAPI RESPONSE:\n{self.api_response.text}")
                                if "Validated" in str(self.api_response.text):
                                        sound.play("sounds/uiLogin.mp3")
                                        self.login_window.master.deiconify()
                                        #self.login_window.master.attributes("-fullscreen",True)
                                        self.login_window.destroy()
                                        self.slide_menu=self.load_slide_menu(self.master, self.user_profilePic, username=None)
                                return self.slide_menu
                                
                except requests.RequestException:
                                self.login_window.switch_green(self.login_window.status_bar, color="red")
                                print("Api failed to respond.")

        def load_slide_menu(self, master, profilepic,username):
                if not hasattr(self,"slide_menu") or self.slide_menu is None:
                        self.slide_menu=slide_menu.SlideMenu(master=master,profile_picture=profilepic, user_name=username)


if __name__== "__main__":
        Customtkinter = customtkinter.CTk(fg_color="#101010")
        Local_DB = database.Access()
        #Login = LoginValidation(Customtkinter)
        Ui = UserInterface(Customtkinter, Local_DB)
        Customtkinter.mainloop()