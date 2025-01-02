import customtkinter
import personal_module
import cards.OriginalCard as OriginalCard


class Inventory(OriginalCard):
    def __init__(self, master, image_path="icons/package.png",
                  local_db=None,
                  search_widget=None,
                  mainFile_path=None,
                 **kwargs):
        
        super().__init__(master,
                         image_path=image_path,
                        **kwargs)
        
        self.search_widget=search_widget
        self.local_db=local_db
        self.items_returned_by_search=[]
        self.mainFile_path=mainFile_path
        self.scrollable_frame = None
       
        self.bind("<Button-1>", lambda event: self.after(1,self.initialize_scrollable_frame))

    def catch_user_search(self,event=None):
        try:
            self.user_search=self.search_widget.get()
            self.request_user_search = self.local_db.searchDb_item(user_search = f"{self.user_search}")
            self.load_inventory(self.request_user_search)
        except Exception as e:
            print({e})
    
    def load_inventory(self, items):
        self.frame_width=self.scrollable_frame.frame.cget("width")
        # destroy any items inside scrollable_frame (any older search)
        for item in self.items_returned_by_search:
            item.destroy()
        self.items_returned_by_search.clear()
        # load current search anew:
        # for every item returned by the searchDb(), creates a frame for the item and packs it on screen
        for i in items:
            self.item_frame=personal_module.HoverFrame(self.scrollable_frame.frame,
                                                       height=50,
                                                       width=self.frame_width,
                                                       expand_orientation="vertical",
                                                       fg_color="#181818",
                                                       hover_color="#141414",
                                                       border_color="#101010")
            self.item_frame.pack(pady=1,padx=1, fill="x")
            # store the items packed on screen inside a list to guide the program of what is currently on screen,
            # when a new search if triggered, the initial loop before this one will know which items to remove from the screen:
            # (line 34)
            self.items_returned_by_search.append(self.item_frame)
        # moves the scrollable_frame/canvas inside it to the top again 
        # to display the new search
        self.scrollable_frame.canvas.yview_moveto(0)

    def initialize_scrollable_frame(self, event=None):
        self.holder_height=self.holder.winfo_height()
        self.holder_width=self.holder.winfo_width()
        #print(self.holder_height,self.holder_width)
        # loads the scrollable_frame which will countain the searches returned by the database
        self.scrollable_frame = personal_module.ScrollFrame(self.holder,fg_color="#101010",border_color="#101010", width=self.holder_width, height=self.holder_height)
        self.scrollable_frame.pack(side="right",fill="both",expand=True)
        self.catch_user_search()
        self.search_widget.bind("<KeyRelease>", self.catch_user_search)
        
        self.master.after(100, lambda: self.bind("<Configure>", self.search_widget_bind_control))
        
        return self.scrollable_frame

    def search_widget_bind_control(self,event=None):
        #print("\nsearch_widget_bind_control() called:")
        if self.expanded is False:
            self.unbind("<Configure>")
            self.master.after(10, self.search_widget.unbind("<KeyRelease>"))
            #print("Search-Widget un-binded")










if __name__=="__main__":
    app = customtkinter.CTk()
    app.geometry("900x500")
    card = Inventory(app, border_color="#121212")
    card.pack()
    app.mainloop()