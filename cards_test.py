import customtkinter


class GridApp(customtkinter.CTk):
    def __init__(self, items):
        super().__init__()
        self.geometry("900x600")

        self.card_width = 200
        self.card_height = 100

        self.items = items  # List of items to arrange in a grid
        self.arrange_widgets()

    def arrange_widgets(self):
        # Get the master window dimensions
        self.update_idletasks()
        master_width = self.winfo_width()
        master_height = self.winfo_height()

        # Calculate number of rows and columns
        n_rows = master_width // self.card_width
        n_columns = master_height // self.card_height

        current_item_index = 0

        for col in range(n_columns):
            if current_item_index >= len(self.items):
                break

            # Create a frame for each row
            row_frame = customtkinter.CTkFrame(self)
            row_frame.pack(fill="x", anchor="n", pady=5)

            for row in range(n_rows):
                if current_item_index >= len(self.items):
                    break

                # Retrieve the current item
                item = self.items[current_item_index]

                # Create and pack the widget
                card = customtkinter.CTkFrame(row_frame, width=self.card_width, height=self.card_height, fg_color="#121212")
                card.pack(side="left", padx=5, pady=5)

                # Optionally add a label with the item's value
                label = customtkinter.CTkLabel(card, text=str(item), fg_color="transparent")
                label.pack(expand=True)

                current_item_index += 1


if __name__ == "__main__":
    # Example list of items
    items_list = [f"Item {i+1}" for i in range(15)]

    app = GridApp(items_list)
    app.mainloop()
