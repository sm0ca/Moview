# Name        : Moview application
# Programmers : Sanchaai, Aqib, & Landry
# Date        : 06/17/22
# Description : This is an application that allows users to maintain
#               a list of their previously watched movies, search and
#               view details for almost any movie, and get genre-based
#               recommendations with every movie viewed in the program.
#               The program also allows for separate user accounts, so
#               that multiple users can have their own lists within the
#               same application. This program also comes with a sample
#               user by default, with the account's username and password
#               both being "sample".

# Resources   : Background image from https://tiny.one/hexbg
#               Background music from https://tiny.one/musbg
#               Direction arrows from https://tiny.one/micons

# Import the Moview and Tkinter classes
from Moview import Moview
from tkinter import *

# Main function to create a new Tkitner window and instantiate a new
# Moview object using the window (and also set up the tkinter mainloop)
def main():
    root = Tk()
    window = Moview(root)
    root.mainloop()

main() # Call the main function