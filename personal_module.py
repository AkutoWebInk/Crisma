import customtkinter
from PIL import Image, ImageDraw, ImageTk, ImageOps
import warnings


def loadImage(path, size=(50,50)):
    image = Image.open(path)
    image = image.resize(size)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(image)

def loadImageC(path, size=(50, 50)):
    image = Image.open(path).resize(size, Image.LANCZOS).convert("RGBA")
    
    # Create a fully transparent image as the base
    transparent_background = Image.new("RGBA", size, (0, 0, 0, 0))
    
    # Create a high-resolution mask
    upscale_factor = 4
    high_res_size = (size[0] * upscale_factor, size[1] * upscale_factor)
    high_res_mask = Image.new("L", high_res_size, 0)
    draw = ImageDraw.Draw(high_res_mask)
    draw.ellipse((0, 0, high_res_size[0], high_res_size[1]), fill=255)
    
    # Downscale the mask to the target size for anti-aliasing
    mask = high_res_mask.resize(size, Image.LANCZOS)
    
    # Create the circular image using the anti-aliased mask
    circular_image = Image.composite(image, transparent_background, mask)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(circular_image)

def loadImageSQR(path, label_size=(160, 200), corner_radius=15):
    # Ensure the image is square to fit within the smallest dimension
    size = min(label_size)  # Take the smaller of the width or height
    square_size = (size, size)

    # Open and resize the image to the calculated square size
    image = Image.open(path).resize(square_size, Image.LANCZOS).convert("RGBA")

    # Create a transparent square base for the mask
    transparent_background = Image.new("RGBA", square_size, (0, 0, 0, 0))

    # Create a rounded rectangular mask
    upscale_factor = 4  # High resolution for anti-aliasing
    high_res_size = (square_size[0] * upscale_factor, square_size[1] * upscale_factor)
    high_res_mask = Image.new("L", high_res_size, 0)
    draw = ImageDraw.Draw(high_res_mask)

    # Draw a rounded rectangle
    draw.rounded_rectangle((0, 0, high_res_size[0], high_res_size[1]), radius=corner_radius * upscale_factor, fill=255)

    # Downscale the mask for anti-aliasing
    mask = high_res_mask.resize(square_size, Image.LANCZOS)

    # Apply the rounded mask to the image
    rounded_image = Image.composite(image, transparent_background, mask)
    warnings.filterwarnings("ignore")
    return ImageTk.PhotoImage(rounded_image)


class HoverFrame(customtkinter.CTkFrame):
    def __init__(self, 
                 master,
                 height=10, 
                 width=10,
                 bg_color="transparent", 
                 fg_color="#181818", 
                 border_color="#242424", 
                 border_width=1, 
                 corner_radius=5, 
                 hover_color=None,
                 expand_orientation=None,
                 image=None,
                 image_side=None,
                 profile_image=None,
                 profile_image_side=None,
                 image_size=None,
                 pimage_size=None):

        self.expanded = False
        self.original_frame_width = width
        self.original_frame_height = height
        self.orignal_fg_color = fg_color
        self.hover_color = hover_color
        self.image_path = image
        self.image_side = image_side
        self.profile_image_path = profile_image
        self.profile_image_side = profile_image_side
        self.image_size=image_size
        self.pimage_size = pimage_size

        super().__init__(master=master, 
                         height=height,  
                         width=width,  
                         bg_color=bg_color, 
                         fg_color=fg_color, 
                         border_color=border_color, 
                         corner_radius=corner_radius,
                         border_width=border_width)
        self.pack_propagate(False)
        
        
        


        if self.profile_image_path:
            if not self.pimage_size:
                self.profile_image = loadImageC(f"{self.profile_image_path}", size=(180,180))
                self.profile_image_label= customtkinter.CTkLabel(self,
                                                        width=180,
                                                        height=180,
                                                        text=" ",
                                                        image=self.profile_image,
                                                        bg_color="transparent",
                                                        fg_color="transparent")
                self.profile_image_label.pack(pady=1,padx=1, side = "bottom")
                self.profile_image_label.bind("<Enter>", self.on_hover)
                self.profile_image_label.bind("<Leave>", self.off_hover)
            else:
                self.profile_image = loadImageC(f"{self.profile_image_path}", size=(int(f"{self.pimage_size}"),int(f"{self.pimage_size}")))
                self.profile_image_label= customtkinter.CTkLabel(self,
                                                        width=180,
                                                        height=180,
                                                        text=" ",
                                                        image=self.profile_image,
                                                        bg_color="transparent",
                                                        fg_color="transparent")
                self.profile_image_label.pack(pady=0,padx=0, side = "bottom")
       
        if self.profile_image_side is not None and self.profile_image_path is not None:
            self.profile_image_label.pack_configure(pady=0,padx=0, side=f"{self.profile_image_side}")
        
        if self.image_path is not None:
            if not self.image_size:
                self.item_image = loadImage(f"{self.image_path}", size=(180,180))
                self.image_label = customtkinter.CTkLabel(self,width=180,height=180,text=" ",image=self.item_image)
                self.image_label.pack(pady=5,padx=5)
            
            elif image_size=="total":
                self.item_image = loadImage(f"{self.image_path}", size=(180,180))
                self.image_label = customtkinter.CTkLabel(self,text=" ",image=self.item_image)
                self.image_label.pack(expand=True, fill="both")
            
            else:
                self.item_image = loadImage(f"{self.image_path}", size=(int(f"{self.image_size}"),int(f"{self.image_size}")))
                self.image_label = customtkinter.CTkLabel(self,width=180,height=180,text=" ",image=self.item_image)
                self.image_label.pack(pady=5,padx=5)

            self.image_label.bind("<Enter>", self.on_hover)
            self.image_label.bind("<Leave>", self.off_hover)
            
        if self.image_side is not None and self.image_path is not None:
            self.image_label.pack_configure(pady=5,padx=5, side=f"{self.image_side}")

        if hover_color is not None:
            self.bind("<Enter>", self.on_hover)
            self.bind("<Leave>", self.off_hover)
        
        if expand_orientation is not None:
            
            if expand_orientation == "horizontal":
                self.bind("<Enter>", self.expand_width)
                self.bind("<Leave>", self.return_width)
            
            elif expand_orientation == "vertical":
                self.bind("<Button-1>",self.expand_height)
                self.bind("<Double-1>", self.return_height)
            
            elif expand_orientation =="card":
                self.bind("<Button-1>", self.expand_height)
                self.bind("<Button-1>", self.expand_width)
                self.bind("<Double-1>", self.return_width)
                self.bind("<Double-1>", self.return_height)
                

    def expand_height(self,event, h=None):
        if not h:
            self.configure(height = self.original_frame_height+80)
        else:
            self.configure(height = self.original_frame_height+int(f"{h}"))

    def expand_width(self, event, w=None):
        if not w:
            self.configure(width=self.original_frame_width + 80)
        else:
            self.configure(width = self.original_frame_width+int(f"{w}"))
    
    def return_height(self,event):
        self.configure(height = self.original_frame_height)
   
    def return_width(self, event):
        self.configure(width=self.original_frame_width)

    def on_hover(self, event):
        try:
            self.configure(fg_color=self.hover_color)
        except Exception:
            pass 

    def off_hover(self, event):
        try:
            self.configure(fg_color=self.orignal_fg_color)
        except Exception:
            pass

class ScrollFrame(customtkinter.CTkFrame):
    def __init__(self,
                 master, 
                 height=200,
                 width=200,
                 fg_color="#101010",
                 bg_color="#101010",
                 border_color="#242424",
                 border_width=1,
                 corner_radius=5,
                 scrollbar = True):
        
        super().__init__(master=master,
                         height=height,
                         width=width,
                         fg_color=fg_color,
                         bg_color=bg_color,
                         border_color=border_color,
                         border_width=border_width,
                         corner_radius=corner_radius)
        
        self.pack_propagate(False)

        self.canvas = customtkinter.CTkCanvas(self,
                                              bg="#101010",
                                              highlightthickness=0)
        self.canvas.pack(side="left", expand=True, fill="both", pady=3, padx=2)
        
        if scrollbar:
            self.scrollbar = customtkinter.CTkScrollbar(self, 
                                                    bg_color="transparent",
                                                    fg_color="transparent",
                                                    height=self.cget("height"),
                                                    button_color="#202020",
                                                    button_hover_color="#222222",
                                                    command=self.canvas.yview)
            self.scrollbar.pack(side="right", pady=3,padx=1,fill="y", expand=False)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = customtkinter.CTkFrame(self.canvas,
                                            fg_color="transparent",bg_color="transparent")
        
        self.frame.bind("<Configure>",self.configure_frame)
        self.canvas.bind("<Configure>", self.configure_canvas)
        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", self.scroll_with_mouse))
        self.canvas.bind("<Leave>", lambda evevnt: self.canvas.unbind("<MouseWheel>"))
        
        self.frame_id = self.canvas.create_window((0,0), window=self.frame, anchor="nw")
    

    def configure_frame(self, event):
        self.frame_xy = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
        self.canvas.configure(scrollregion=(0,0, self.frame_xy[0], self.frame_xy[1]))
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.configure(width=self.frame.winfo_reqwidth())
    
    def configure_canvas(self, event):
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
       
    def scroll_with_mouse(self, event):
        try:
            if self.canvas and self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception as e:
            print(f"Error during try on scroll_with_mouse:{e}")

class LogInWindow(customtkinter.CTkToplevel):
    def __init__(self,master):
        
        self.master=master
        
        super().__init__(master)
        
        self.user_username=None
        
        
        self.title("LogIn")
        self.geometry("200x200")
        self.resizable(False,False)
        self.focus()
        self.lift()

        self.attributes("-topmost", True)

        self.removed_color = "#111111"
        self.attributes("-transparentcolor", f"{self.removed_color}")

        self.configure(fg_color="#101010")
        self.pack_propagate(False)

        self.login_image = loadImageC("icons/edna_mode.png", size=(100,100))

        self.upper_half = customtkinter.CTkLabel(self,
                                                fg_color="#101010",
                                                image=self.login_image,
                                                text=None)
        self.upper_half.pack(side="top", pady=2, padx=10)

        self.lower_half= HoverFrame(self, fg_color="#141414")
        
        self.lower_half.pack(side="bottom", expand=True, fill="both")


        self.username_entry = customtkinter.CTkEntry(self.lower_half, 
                                                     placeholder_text="Usuário",
                                                     placeholder_text_color="#606060",
                                                     fg_color="#101010",
                                                     border_color="#606060",
                                                     border_width=1,
                                                     corner_radius=5,
                                                     width=100,
                                                     justify="center")
        
        self.password_entry = customtkinter.CTkEntry(self.lower_half, 
                                                     placeholder_text="Senha",
                                                     placeholder_text_color="#606060",
                                                     fg_color="#101010",
                                                     border_color="#606060",
                                                     border_width=1,
                                                     corner_radius=5,
                                                     width=100,
                                                     justify="center")
        self.x_value, self.xx_value = -110, -110
        
        self.username_entry.place(x=self.x_value, y = 20)
        self.password_entry.place(x=self.xx_value, y = 50)
        # self.username_entry.bind("<KeyRelease>", lambda event: self.slide_password())
        self.username_entry.bind("<KeyRelease>", lambda event: self.catch_username())
        self.password_entry.bind("<KeyRelease>", lambda event: self.catch_password())
        
        self.slide_username()

    def slide_username(self):
        if self.x_value < 50:
            self.x_value += 1
            self.username_entry.place_configure(x=self.x_value)
            self.after(1, self.slide_username)
    
    def show_password(self):
        if self.xx_value<50:
            self.xx_value +=1
            self.password_entry.place_configure(x=self.xx_value)
            self.after(1, self.show_password)
    
    def hide_password(self):
        if self.xx_value > -110:  
            self.xx_value -= 5
            self.password_entry.place_configure(x=self.xx_value)
            self.after(10, self.hide_password)

    def catch_username(self):
        self.user_username = self.username_entry.get()
        return self.user_username

    def catch_password(self):
        self.user_password=self.password_entry.get()
        return self.user_password

    def return_master_winfo(self,event=None):
        if self.master:
            self.master.update_idletasks()
            self.master_width = self.master.winfo_width()
            self.master_height = self.master.winfo_height()
            self.geometry(f"200x200+{self.master_width}+{self.master_height}")
            return

class AddItemWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        self.master = master
        
        super().__init__(master)

        self.title("Add New Item")
        self.geometry("300x500+200+200")
        self.resizable(False,False)
        self.focus()
        self.lift()
        self.attributes("-topmost", True)
        self.configure(fg_color="#181818")


        self.upper_side=HoverFrame(self, 
                                   fg_color="#181818",
                                   bg_color="transparent",
                                   border_color="#202020",
                                   corner_radius=3)
        self.lower_side=HoverFrame(self,fg_color="#181818",
                                   bg_color="transparent",
                                   border_color="#181818",
                                   corner_radius=0)
        
        self.upper_side.pack(expand=True, fill="both",
                             pady=5,
                             padx=5)
        self.lower_side.pack_propagate(False)
        self.lower_side.pack(expand=True, fill="both")

        self.load_entries()

    def load_entries(self):
        self.item_image=customtkinter.CTkLabel(self.upper_side, 
                                               image=loadImage("icons/no_image_icon.png",size=(100,100)),
                                               text=None)
        self.item_image.pack(expand=True, fill="both",
                             padx=1,pady=1)
        
        self.add_item_image=customtkinter.CTkButton(self.upper_side,
                                                    width=10,
                                                    height=20,
                                                    text=" Add Item Image ",
                                                    fg_color="#181818",
                                                    hover_color="#191919",
                                                    corner_radius=2)
        self.add_item_image.pack(side="bottom",
                                 fill="x",
                                 padx=1,
                                 pady=1.5)

        self.item_name=customtkinter.CTkEntry(self.lower_side,
                                              placeholder_text="Name",
                                              placeholder_text_color="white",
                                              width=100,
                                              height=15,
                                              fg_color="#181818",
                                              border_width=1,
                                              corner_radius=3)
        self.item_name.pack(anchor="nw",side="left",padx=5, pady=1)

        self.item_line=customtkinter.CTkEntry(self.lower_side,
                                              placeholder_text="Line",
                                              placeholder_text_color="white",
                                              width=100,
                                              height=15,
                                              fg_color="#181818",
                                              border_width=1,
                                              corner_radius=3)
        self.item_line.pack(anchor="nw",side="left",padx=0,pady=1)

        self.item_reference=customtkinter.CTkEntry(self.lower_side,
                                                   placeholder_text="Reference",
                                                   placeholder_text_color="white",
                                                   width=100,
                                                   height=15,
                                                   fg_color="#181818",
                                                   border_width=1,
                                                   corner_radius=3)
        self.item_reference.pack(anchor="nw",padx=5,pady=1)

        self.item_capacity=customtkinter.CTkEntry(self.lower_side,
                                                  placeholder_text="Capacity",
                                                  placeholder_text_color="white",
                                                  width=100,
                                                  height=15,
                                                  fg_color="#181818",
                                                  border_width=1,
                                                  corner_radius=3)
        self.item_capacity.pack(anchor="nw",padx=5,pady=5)

class ContextMenu(customtkinter.CTkToplevel):
    # Class-level variable to track the menu state
    current_menu = None

    def __init__(self, master):

        super().__init__(master)

        # Configs for the window
        self.overrideredirect(True)
        self.focus()
        self.resizable(False, False)
        self.configure(fg_color="#191919")
        self.attributes("-transparentcolor", "#191919")
        self.attributes("-topmost", True)

        # Bindings
        self.master.bind("<Button-3>", self.pop_up)  
        self.bind("<Configure>", self.catch_click_position)
        self.bind("<Button-1>", lambda event: self.destroy())
        self.master.bind("<Button-1>", lambda event: self.destroy())

        # Objects inside the window
        self.interior = customtkinter.CTkFrame(self,
                                               fg_color="#181818", 
                                               border_width=1,
                                               corner_radius=7,
                                               border_color="#404040",
                                               bg_color="#191919")
        self.interior.pack(expand=True, fill="both")

        self.button1 = customtkinter.CTkButton(self.interior,
                                               fg_color="#181818",
                                               bg_color="#191919",
                                               hover_color="#101010",
                                               height=10,
                                               border_color="#141414",
                                               corner_radius=5,
                                               text="Open Side Menu")
        self.button1.pack(padx=1, pady=1, fill="x", side="top")
   

    def catch_click_position(self, event):
        self.x_pos = event.x_root
        self.y_pos = event.y_root
        self.geometry(f"150x150+{self.x_pos}+{self.y_pos}")

    def pop_up(self, event):

        if ContextMenu.current_menu:
            # If another context menu is open, close it
            ContextMenu.current_menu.destroy()

        # Create a new context menu at the click position
        ContextMenu.current_menu = ContextMenu(None)
        ContextMenu.current_menu.catch_click_position(event)

    def destroy(self):
        ContextMenu.current_menu = None
        super().destroy()

class SideMenu(customtkinter.CTkToplevel):
    def __init__(self, master, profile_picture, **kwargs):
        self.master = master
        self.profile_picture = profile_picture
        self.master_width = 0
        self.master_height = 0
        self.side_menu_initial_place = 0
        self.sided_menu_locked_height = 0
        super().__init__(master, **kwargs)
        self.pack_propagate(False)  # Prevents resizing

        self.return_master_winfo() #initialy returns the master winfo
        
        # returns the master wingo after any event realted to resizing or config
        self.master.bind("<Configure>", self.return_master_winfo) 

        self.attributes("-topmost", True)
        self.overrideredirect(True)

        self.removed_color = "#030303"                               
        self.attributes("-transparentcolor", f"{self.removed_color}")
        self.attributes("-alpha", 1)
        

        # Create and pack the transparent frame
        self.invisible_frame = HoverFrame(self,
                                          profile_image=f"{profile_picture}",
                                          pimage_size=100,
                                          fg_color=f"{self.removed_color}",
                                          bg_color=f"{self.removed_color}",
                                          width=110,
                                          height=self.master.winfo_height(),
                                          corner_radius=5,
                                          border_color=f"{self.removed_color}",
                                          border_width=1)
        self.invisible_frame.pack(fill="y", side="left")

        self.frame = HoverFrame(self,
                                            width=10,
                                            height=10,
                                            fg_color="#181818",
                                            bg_color=f"{self.removed_color}",
                                            border_color="#323232",
                                            border_width=1)
        self.frame.pack(pady=1,expand=True, fill="both")

        self.side_line = HoverFrame(self.frame,
                                        width=10,
                                        height=200,
                                        fg_color="#141414",
                                        hover_color="#323232",
                                        border_color="#323232",
                                        corner_radius=0.5)
        self.side_line.pack(side="left", fill="y")
        
        self.side_line.bind("<ButtonRelease-1>", self.expand_side_menu_horizontally)
        self.master.bind("<Configure>", self.return_master_winfo)
        self.bind("<Configure>", self.configure_profile_picture)

    def configure_profile_picture(self,event):
        if self.profile_picture:
            try:
                self.invisible_frame.profile_image_path = f"{self.profile_picture}"
                self.invisible_frame.profile_image_side = "bottom"
            except Exception:
             self.invisible_frame.profile_image_path = None
             self.invisible_frame.profile_image_side = None
        
    def expand_side_menu_horizontally(self, event):
        self.master.update_idletasks()

    # Get the current pointer position relative to the screen
        pointer_x = self.master.winfo_pointerx()

    # Calculate the relative position to the master window
        relative_x = pointer_x - self.master.winfo_rootx()

    # Ensure the width is constrained within valid bounds
        new_width = max(100, min(self.master_width - relative_x, 400))  # Min 100, Max 400

    # Update the geometry
        self.geometry(f"{new_width}x{self.master_height}+{self.side_menu_initial_place - new_width}+{self.sided_menu_locked_height+30}")
        return

    def return_master_winfo(self, event=None):
        if self.master_width != self.master.winfo_width() or self.master_height != self.master.winfo_height():
            self.master_width = self.master.winfo_width()
            self.master_height = self.master.winfo_height()
            self.side_menu_initial_place = self.master.winfo_x() + self.master_width + 8
            self.sided_menu_locked_height = self.master.winfo_y()
            self.config_geometry()


    def config_geometry(self):
        # Set initial width and height
        self.master.update_idletasks()
        self.geometry(f"200x{self.master_height}+{self.side_menu_initial_place - 200}+{self.sided_menu_locked_height+30}")

      