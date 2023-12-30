import tkinter as tk
from PIL import Image, ImageTk
import random

class GuessMasterNumberChallenge:
    def __init__(self, master):
        self.master = master
        self.master.title("GuessMaster: Number Challenge")

        self.grid = self.generate_grid()
        self.target_number = self.select_random_number()

        self.player_score = 0
        self.chances = 5
        self.play_again_button = None
        self.quit_button = None

        self.label = tk.Label(master, text="Welcome to GuessMaster: Number Challenge!", font=("Helvetica", 20), fg="darkblue")
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

        self.canvas = tk.Canvas(master, width=600, height=600, bg="lightgray", bd=5, relief="ridge")
        self.canvas.grid(row=1, column=0, columnspan=4, pady=10)

        self.display_grid()

        self.result_label = tk.Label(master, text="", font=("Helvetica", 18), fg="black")
        self.result_label.grid(row=2, column=0, columnspan=4, pady=10)

        # Initially hide the buttons
        self.play_again_button = tk.Button(self.master, text="Play Again", command=self.play_again, font=("Helvetica", 16), bg="green", fg="white")
        self.play_again_button.grid(row=3, column=0, columnspan=4, pady=20, sticky="n")
        self.play_again_button.grid_remove()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, font=("Helvetica", 16), bg="red", fg="white")
        self.quit_button.grid(row=4, column=0, columnspan=4, pady=20, sticky="n")
        self.quit_button.grid_remove()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def generate_grid(self):
        """Generate a 4x4 grid with random numbers."""
        return [[random.randint(1, 100) for _ in range(4)] for _ in range(4)]

    def select_random_number(self):
        """Select a random number from the grid."""
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        return self.grid[row][col]

    def display_grid(self):
        """Display the 4x4 grid on the canvas."""
        for i, row in enumerate(self.grid):
            for j, number in enumerate(row):
                cell_id = self.get_cell_id(i, j)
                self.canvas.create_rectangle(j * 150, i * 150, (j + 1) * 150, (i + 1) * 150, fill="lightblue", outline="white", tags=cell_id)
                self.canvas.create_text(j * 150 + 75, i * 150 + 75, text=str(number), font=("Helvetica", 20), fill="darkblue")

    def on_canvas_click(self, event):
        """Handle canvas click event."""
        if self.chances > 0:
            row = event.y // 150
            col = event.x // 150
            guess = self.grid[row][col]

            if guess == self.target_number:
                self.player_score += 1
                self.end_game()
                self.result_label.config(text="Congratulations! You guessed the correct number.", fg="green")
                self.canvas.itemconfig(self.get_cell_id(row, col), fill="green")
            else:
                self.chances -= 1
                self.result_label.config(text=f"Sorry, wrong guess. Chances left: {self.chances}", fg="red")
                self.canvas.itemconfig(self.get_cell_id(row, col), fill="red")
                

            if self.chances == 0:
                self.result_label.config(text=f"Game Over! Your lost the game.", fg="blue")
                self.end_game()

            # Update the target number for the computer
            self.target_number = self.select_random_number()

    def get_cell_id(self, row, col):
        """Get the canvas item ID for the specified cell."""
        return f"cell_{row}_{col}"

    def end_game(self):
        self.canvas.unbind("<Button-1>") 
        self.quit_button.grid()  
        self.play_again_button.grid()
        self.show_popup()

    def show_popup(self):
        """Display a popup with the game result."""
        popup = tk.Toplevel(self.master)
        popup.title("Game Result")
        popup.geometry("500x400")

        if self.player_score > 0:  
            label = tk.Label(popup, text="Congratulations! You won the game!", font=("Helvetica", 16), fg="green")
            img_path = "win_image.jpg" 
        else:
            label = tk.Label(popup, text="Sorry! Better luck next time.", font=("Helvetica", 16), fg="red")
            img_path = "lose_image.jpg"  

        label.pack(pady=20)

        img = Image.open(img_path)
        img = img.resize((330, 220), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(popup, image=img)
        img_label.image = img
        img_label.pack()

        ok_button = tk.Button(popup, text="OK", command=popup.destroy, font=("Helvetica", 16), bg="blue", fg="white")
        ok_button.pack(pady=20)

    def display_image(self, image_path):
        """Display an image on the canvas."""
        img = Image.open(image_path)
        img = img.resize((600, 600), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def play_again(self):
        self.chances = 5
        self.player_score = 0
        self.target_number = self.select_random_number()
        self.grid = self.generate_grid() 
        self.canvas.delete("all")
        self.display_grid()
        self.result_label.config(text="")
        self.quit_button.grid_remove() 
        self.play_again_button.grid_remove()  
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def quit_game(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessMasterNumberChallenge(root)
    root.mainloop()
