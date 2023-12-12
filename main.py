# main.py
# Main file for the client side of the chat application

import tkinter as tk
from client_gui import ClientGUI


def main():
    root = tk.Tk() # Create the root window
    app = ClientGUI(root) 
    root.mainloop()


if __name__ == "__main__":
    main()
