import customtkinter
import personal_module

class OriginalCard(personal_module.HoverFrame):
    def __init__(self, master, image_path="icons/config_icon.png",
                  width=200, height=400, fg_color="#181818", border_color= "#181818",
                  image_side="bottom",
                  mainFile_path=None,
                 **kwargs):
        
        super().__init__(master, 
                         height=height, 
                         width=width, 
                         image=image_path, 
                         image_side=image_side, 
                         fg_color=fg_color,
                         border_color=border_color,
                        **kwargs)
        
        self.initial_fg_color=fg_color
        self.initial_border_color = self._border_color

        self.expanded = False
        self.mainFile_path = mainFile_path
        self.holder = None
        self.configure(width=width, height=height)
        self.pack_propagate(False)
        
        self.bind("<Button-1>", self.expand_card)
        self.image_label.bind("<Button-1>", self.expand_card)
        

    def load_internal_contents(self):
        self.contents_holder = personal_module.HoverFrame(self,
                                                          fg_color="#101010",
                                                          border_color="#101010",
                                                          corner_radius=0,
                                                          width=self.master_width-32,
                                                          height=self.master_height)
        self.contents_holder.pack(side="right", fill="both",expand=True)
        # creates a frame ocupying the left side of the screen
        self.return_frame = personal_module.HoverFrame(self, 
        fg_color="#101010", 
        border_color="#101010",
        corner_radius=0,
        width=30)
        self.return_frame.pack(side="left", fill="y",padx=0,pady=0)
        
        # creates two more frames inside in order to divide the main on
        # (it's for organization purposes only, no need for funcionality, 
        # and frames usualy take little computing power when empty)
        self.top_half=personal_module.HoverFrame(self.return_frame,
                                                 fg_color="#101010",
                                                 border_color="#101010",
                                                 corner_radius=0)
        self.bottom_half=personal_module.HoverFrame(self.return_frame, 
                                                    fg_color="#101010",
                                                    border_color="#101010",
                                                    corner_radius=0, 
                                                    image="icons/backIcon.png",
                                                    image_size=25)
        
        # packs the two frames inside the self.return_frame
        self.top_half.pack(expand=True, 
                           fill="both", 
                           pady=0, padx=0)
        self.bottom_half.pack(expand=True, 
                              fill="both", 
                              pady=0, padx=0)
        
        #binding the return_card method to the return frame and the frames inside it
        self.return_frame.bind("<Button-1>", self.return_card)
        self.top_half.bind("<Button-1>", self.return_card)
        self.bottom_half.bind("<Button-1>", self.return_card)
        
        self.bottom_half.image_label.bind("<Button-1>", self.return_card)
        self.bottom_half.image_label.pack_configure(pady=0,padx=0)
        
        #if the master has a master, binds the return_card to it too
        if hasattr(self, "master"):
            try:
                self.master.bind("<Button-1>", self.return_card)
            except:
                pass

        self.holder = self.contents_holder
        return self.contents_holder
    
    def expand_card(self, event):
        if not self.expanded:
            #configures the border color to be the same as the background (aesthetics)
            self.configure(fg_color="#101010",border_color="#101010")
            self.hide_other_cards()
            
            #updates master's/parent current info before calling methods to retrieve them (functionality)
            self.master.update_idletasks()
            self.master_height=self.master.winfo_height()
            self.master_width=self.master.winfo_width()
            
            self.image_label.pack_forget()
            self.configure(height=self.master_height-10, width=self.master_width)
            self.pack_configure(side="left",anchor="n",pady=3,padx=3,expand=True,fill="both")
            self.mainFile_path.card_in_display=self
            self.after(1, self.load_internal_contents)

        return self.expanded, self.master_width, self.master_width
            
    def return_card(self, event):

        if hasattr(self,"contents_holder"):
            self.contents_holder.destroy()
            self.return_frame.destroy()

        # returns the card to its original form as firstly instantiated inside the main program
        # the logics are the same, but now the program reverses stuff and a few things are per default values
        self.configure(fg_color=self.initial_fg_color,border_color=self.initial_border_color)
       
        # in order to update their values before calling informations not up to date
        # (usualy good to call before retrieving values from changing variables)
        self.master.update_idletasks()

        # configures itself to its default values as firstly instantiated 
        # when cards.Inventory(value1, value2, ...) was called:

        
        # re-packs the image_label inside cards.Inventory(value1, value2, ...)
        # no need to configure image_label since the inital values instantiated haven't changed,
        # just put it back on screen: 
        self.image_label.pack_configure(pady=5,padx=5, side="bottom", anchor="center")
        
        self.master.unbind("<Button-1>")
        
        self.unhide_other_cards()
        self.pack_configure(side="left", anchor="n", pady=3,padx=3, fill=None, expand=False)
        self.master.after(250, self.configure(height=400, width=200))
        self.mainFile_path.card_in_display=None
        self.expanded=False
        
        return self.expanded
        
    def hide_other_cards(self):
        for card in self.mainFile_path.packed_cards:
            if card != self:
                card.pack_forget()
    
    def unhide_other_cards(self):
        for card in self.mainFile_path.packed_cards:
            card.pack_configure(side="left", anchor="n",pady=3,padx=3, fill=None, expand=False)

if __name__=="__main__":
    app = customtkinter.CTk()
    app.geometry("900x500")
    card = OriginalCard(app, border_color="#121212")
    card.pack()
    app.mainloop()