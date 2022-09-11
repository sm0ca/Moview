# Name        : Moview class file for the Moview application
# Programmers : Sanchaai, Aqib, & Landry
# Date        : 06/17/22
# Description : Contains Moview class, which serves most of the primary
#               functions for the Moview application. Note, "requests",
#               "pillow", and "pyglet" must be pip installed!

from tkinter import messagebox # Used to notify user of certain events
from tkinter import * # Used to create the primary GUI interface
from PIL import Image,ImageTk # Used to load non-.gif/.ppm format images in Tkinter
from io import BytesIO # Used to convert raw bytecode into BytesIO object for Pillow
import pyglet # Used to load custom fonts for Tkinter
import random # Used to shuffle the list of similar movies
import requests # Used for making internet requests
import warnings # Used to raise an error if images are too large
import winsound # Used to play background music

# Class for Moview Program
class Moview():

    # Attributes with the names of the fonts
    TITLE_FONT = "LIBRARY3AM"
    BODY_FONT = "Gidole Regular"

    # API key for IMDb-API
    KEY = "k_zax1xbn5"

    # Class initialization
    def __init__(self, win):
        
        # Set window variable
        self.win = win

        # Configure window title
        win.title("Moview")

        # Set window size
        win.geometry("1000x666")

        # Make it so that the window can't be resized
        win.resizable(False,False)

        # Create canvas in which the content will be placed, and pack it
        self.canvas = Canvas(self.win, width = 1000, height = 666, highlightthickness=0, bg="black")
        self.canvas.pack()

        # Create frame used for search results
        self.frame = Frame(self.canvas) # Used for search results

        # Local PhotoImage initializations (background + left & right arrows)
        # Uses Pillow's/Tkinter's modules to open jpg/png files and resize them (with antialising)
        self.img = ImageTk.PhotoImage(Image.open("assets/background.jpg").resize((1000, 666), Image.ANTIALIAS))
        self.left_arrow = ImageTk.PhotoImage(Image.open("assets/left.png").resize((35, 35), Image.ANTIALIAS))
        self.right_arrow = ImageTk.PhotoImage(Image.open("assets/right.png").resize((35, 35), Image.ANTIALIAS))

        # Use the Pyglet library to load locally stored fonts such that they can be used by Tkinter
        pyglet.font.add_file("assets/Gidole-Regular.ttf")
        pyglet.font.add_file("assets/library.ttf")

        # When using reading images from the internet using Pillow, the default behaviour is to display
        # a warning message if an image is too large. In order to avoid this, we can use the warnings
        # library (that comes with Python) to raise an error instead, so that it can be caught using a
        # try-except block.
        warnings.simplefilter('error', Image.DecompressionBombWarning)

        # Uses the winsound library to play jazz music in the background (looped asynchronously)
        winsound.PlaySound("assets/JazzMusic.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

        # Call method to start the program
        self.start()

    # Method to delete all items on screen and restore the background image + frame
    def clear_screen(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        self.frame.destroy()
        self.frame = Frame(self.canvas)

    # Function to get a PhotoImage from an online URL
    def image_object(self, url, dims):

        # Try and except used because sometimes images are too large,
        # which raises an error due to security reasons
        try:
            # Requests image from the internet
            poster_request = requests.get(url).content

            # Uses BytesIO to convert the received data into a BytesIO object,
            # a form of data that can be opened by Pillow
            bytes_poster = BytesIO(poster_request)

            # Uses Pillow's/Tkinter's modules to open the image (from BytesIO object format)
            # and resize them (with antialising)
            poster = ImageTk.PhotoImage(Image.open(bytes_poster).resize(dims, Image.ANTIALIAS))

            # Return the image object
            return poster
        
        # If the image is too large, repeat the above with the default placeholder image
        except:
            poster_request = requests.get("https://imdb-api.com/images/original/nopicture.jpg").content
            bytes_poster = BytesIO(poster_request)
            poster = ImageTk.PhotoImage(Image.open(bytes_poster).resize(dims, Image.ANTIALIAS))
            return poster

    # Method for creating start screen 
    def start(self):
        self.clear_screen()

        # Creates title text
        self.canvas.create_text(500, 290, text="MOVIEW", anchor=CENTER,
                                font=(self.TITLE_FONT, 50), fill="white")

        # Login button
        login_btn = Button(width=23, text="Login", font=(self.BODY_FONT, 20),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.login)

        # Places login button on canvas using a tkinter window
        self.canvas.create_window(500, 390, anchor=CENTER, window=login_btn)

    # Method for creating login screen 
    def login(self):
        self.clear_screen()

        # Creates login heading text
        self.canvas.create_text(500, 220, text="LOGIN", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Username entry box
        self.user_entry = Entry(width=23, relief="ridge", bd=0, bg="#060606", fg="white",
                                font=(self.BODY_FONT, 15), highlightbackground="grey", highlightthickness=1, insertbackground="white")

        # Places username entry on canvas using a tkinter window
        self.canvas.create_window(500, 320, window=self.user_entry)

        # Submit button
        submit_btn = Button(width=10, text="Submit", font=(self.BODY_FONT, 15),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.user_valid)

        # Places submit button on canvas using a tkinter window
        self.canvas.create_window(500, 410, anchor=CENTER, window=submit_btn)

    # Method to check if user is valid
    def user_valid(self):
        
        # Var to indicate the user has been found within list of users
        found = False

        # Gets username from entry box
        self.uname = self.user_entry.get()
        
        # Opens credentials file and searches for the user
        with open("database/creds.txt", "r") as f:
            while (found == False) and ((line := f.readline()) != ""):
                line = line.strip().split("|")

                # If the user does exist, save the correct password and
                # prompt the user to enter a password
                if line[0] == self.uname:
                    found = True
                    self.correct_pwd = line[1]
                    self.pwd_field()

        # If the entire list of users is searched to no avail, create new user
        if found == False:
            self.new_user()
            
    # Method for creating password entry screen
    def pwd_field(self):
        self.clear_screen()

        # Creates password heading text
        self.canvas.create_text(500, 220, text="ENTER PASSWORD", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Password entry box
        self.pwd_entry = Entry(width=23, relief="ridge", bd=0, bg="#060606", fg="white", show="•",
                                font=(self.BODY_FONT, 15), highlightbackground="grey", highlightthickness=1, insertbackground="white")

        # Places password entry on canvas using a tkinter window
        self.canvas.create_window(500, 320, window=self.pwd_entry)

        # Submit button
        submit_btn = Button(width=10, text="Submit", font=(self.BODY_FONT, 15),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.pwd_valid)

        # Places submit button on canvas using a tkinter window
        self.canvas.create_window(500, 410, anchor=CENTER, window=submit_btn)

    # Method to validate password
    def pwd_valid(self):

        # Gets password from entry box
        self.pwd = self.pwd_entry.get()

        # If the password matches the correct password, take user to home screen
        if self.pwd == self.correct_pwd:
            self.home()
        
        # Otherwise, display a message to show that the password was incorrect,
        # and take the user back to the login screen
        else:
            messagebox.showinfo("Error","Incorrect Password")
            self.login()

    # Method for creating a user-creation screen
    def new_user(self):
        self.clear_screen()

        # Creates text to explain the user isn't found, and prompts to create a new one
        self.canvas.create_text(500, 220, text="USER NOT FOUND", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        self.canvas.create_text(500, 320, text="Create new user?", anchor=CENTER,
                                font=(self.BODY_FONT, 20), fill="white")

        # Yes and No buttons
        no_btn = Button(width=10, text="No", relief="ridge",
                    font=(self.BODY_FONT, 15), bg="#060606", fg="white",
                    command=self.login)
        self.canvas.create_window(420, 410, anchor=CENTER, window=no_btn)

        yes_btn = Button(width=10, text="Yes", relief="ridge",
                    font=(self.BODY_FONT, 15), bg="#060606", fg="white",
                    command=self.create_pwd)
        self.canvas.create_window(580, 410, anchor=CENTER, window=yes_btn)

    # Method for creating a password-creation screen
    def create_pwd(self):
        self.clear_screen()

        # Creates password heading text
        self.canvas.create_text(500, 220, text="CREATE PASSWORD", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Password entry box
        self.pwd_entry = Entry(width=23, relief="ridge", bd=0, bg="#060606", fg="white", show="•",
                                font=(self.BODY_FONT, 15), highlightbackground="grey", highlightthickness=1, insertbackground="white")

        # Places password entry on canvas using a tkinter window
        self.canvas.create_window(500, 320, window=self.pwd_entry)

        # Submit button
        submit_btn = Button(width=10, text="Submit", font=(self.BODY_FONT, 15),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.create_user)

        # Places submit button on canvas using a tkinter window
        self.canvas.create_window(500, 410, anchor=CENTER, window=submit_btn)

    # Method to create a new user within the text files
    def create_user(self):

        # Append the new credentials to the "creds.txt" file, using "|" as a separator
        with open("database/creds.txt", "a") as f:
            f.write(f"{self.uname}|{self.pwd_entry.get()}\n")
        
        # Create a new file for the user's watchlist, and close it
        new_user = open(f"database/{self.uname}.txt", "w")
        new_user.close()

        # Take user to the home screen
        self.home()

    # Method for creating home screen
    def home(self):
        self.clear_screen()

        # Creates options heading text
        self.canvas.create_text(500, 200, text="WELCOME", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Button that lets the user search for movies
        search_btn = Button(width=23, text="Search", font=(self.BODY_FONT, 20),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.search)

        self.canvas.create_window(500,300, anchor=CENTER, window=search_btn)

        # Button that lets the user see their watchlist
        watchlist_btn = Button(width=23, text="Watchlist", font=(self.BODY_FONT, 20),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.display_watchlist)

        self.canvas.create_window(500, 400, anchor=CENTER, window=watchlist_btn)

        # Button that lets the user logout
        logout_btn = Button(width=14, text="Logout", font=(self.BODY_FONT, 16),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.start)
        self.canvas.create_window(800, 590, anchor=NW, window=logout_btn)

    # Method for getting the user's watchlist
    def get_list(self):
        self.clear_screen()

        # Empty array to store user's watchlist
        user_list = []
        
        # Opens the user's text file and stores all of the lines in a list
        with open(f"database/{self.uname}.txt", "r") as f:
            user_list = f.readlines()

        # For each item in the list, strip the newline character and split
        # it into a list (by the "|" separator)
        user_list = [i.strip().split("|") for i in user_list]

        # Convert the final element in each movie's list (the poster url)
        # into an actual image object using the self.image_object() method
        for i in range(len(user_list)):
            user_list[i][-1] = self.image_object(user_list[i][-1], (81, 123))

        # Return the user's watchlist
        return user_list

    # Method for creating the watchlist screen
    def display_watchlist(self):

        # Get the user's watchlist using the self.get_list() method
        self.watchlist = self.get_list()

        # Create watchlist heading text
        self.canvas.create_text(500, 130, text="Watchlist", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Place the frame used for displaying the list
        self.frame.place(x=500, y=180, anchor=N)

        # Calculate the region of scroll required using the number of items in the list
        region_height = 150*len(self.watchlist)

        # Create a canvas to go within the aforementioned frame, and configure
        # the dimensions of its scrollable region
        self.frame_canvas = Canvas(self.frame,width=600, height=350, bg="#060606",
                             scrollregion=(0,0,500,region_height),
                             highlightthickness=0)

        # Make it so that the frame is actually scrollable (in the vertical axis),
        # and pack the scrollbar
        scrollable = Scrollbar(self.frame, orient="vertical",
                                       command=self.frame_canvas.yview)
        scrollable.pack(side="right",fill="y")

        # Ensure that the canvas is also scrollable, and then pack the canvas
        # such that it fills the frame's canvas
        self.frame_canvas.configure(yscrollcommand=scrollable.set)
        self.frame_canvas.pack(fill="both")

        # Starting y-position for the items to be displayed in the scrollable region
        y_pos = 10
        
        # Iterate through the items in the watchlist
        for i in self.watchlist:
            
            # Store the movie's id in the movie_tag variable
            movie_tag = i[0]

            # Output the poster and movie title on the frame's canvas
            self.frame_canvas.create_image(10, y_pos, anchor=NW, image=i[-1], tags=movie_tag)
            self.frame_canvas.create_text(110, y_pos+35, anchor=NW, text=self.overflow(i[1], 25), font=(self.BODY_FONT, 30), fill="white", tags=movie_tag)

            # Binds everything with the same tag (of the current movie's id) to a lambda function (which calls the self.movie_display()
            # method with the movie's id as the argument). Explanation of the lambda function logic below:

            # lambda: Lets you write functions inline
            # event: When using lambdas in button commands, the first parameter is forcefully turned into one that
            # stores button-press event information, so we dump that into its own variable, "event"
            # movie_tag=movie_tag: Weird quirk with lambdas within loops, where they only end up using the final value in the
            # loop as the parameter value. This is remedied by "cementing" the value in the movie_tag variable in its own
            # parameter. Further reading can be found here: https://stackoverflow.com/a/13355291
            self.frame_canvas.tag_bind(movie_tag, "<ButtonPress-1>", lambda event, movie_tag=movie_tag: self.movie_display(movie_tag))

            # Increase the y-position for the next item
            y_pos += 150

        self.frame_canvas.update() # Update the frame canvas with the new items.
        
        # Button to return back to home
        home_btn = Button(width=23, text="Back to Home", font=(self.BODY_FONT, 18),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.home)

        self.canvas.create_window(500,580, anchor=CENTER, window=home_btn)

    # Method for creating search screen
    def search(self):
        self.clear_screen()

        # Create search heading text
        self.canvas.create_text(500, 220, text="SEARCH", anchor=CENTER,
                                font=(self.TITLE_FONT, 30), fill="white")

        # Searxh entry box
        self.search_box = Entry(width=23, relief="ridge", bd=0, bg="#060606", fg="white",
                                font=(self.BODY_FONT, 15), highlightbackground="grey", highlightthickness=1, insertbackground="white")

        # Places search entry on canvas using a tkinter window
        self.canvas.create_window(500, 320, window=self.search_box)

        # Places submit button on canvas using a tkinter window
        submit_btn = Button(width=10, text="Submit", font=(self.BODY_FONT, 15),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.search_results)
        self.canvas.create_window(500, 410, anchor=CENTER, window=submit_btn)

    # Method for displaying search results
    def search_results(self):

        # Get the search query from the search box
        user_query = self.search_box.get()

        # If the query is empty, display an appropriate error message
        if user_query == "":
            messagebox.showinfo("Error","Search box is empty.")
            self.search()
        
        # Otherwise (if there is a search query)
        else:
            self.clear_screen()

            # Get the search results using the self.movie_search() method
            self.results = self.movie_search(user_query)

            # Create search results heading text
            self.canvas.create_text(500, 130, text="SEARCH RESULTS", anchor=CENTER,
                                    font=(self.TITLE_FONT, 30), fill="white")

            # Place the frame used for displaying the list
            self.frame.place(x=500, y=180, anchor=N)

            # Calculate the region of scroll required using the number of results
            region_height = 150*len(self.results)

            # Create a canvas to go within the aforementioned frame, and configure
            # the dimensions of its scrollable region
            self.frame_canvas = Canvas(self.frame,width=600, height=350, bg="#060606",
                                scrollregion=(0,0,500,region_height),
                                highlightthickness=0)

            # Make it so that the frame is actually scrollable (in the vertical axis),
            # and pack the scrollbar
            scrollable = Scrollbar(self.frame, orient="vertical",
                                        command=self.frame_canvas.yview)
            scrollable.pack(side="right",fill="y")

            # Ensure that the canvas is also scrollable, and then pack the canvas
            # such that it fills the frame's canvas
            self.frame_canvas.configure(yscrollcommand=scrollable.set)
            self.frame_canvas.pack(fill="both")
    
            # Starting y-position for the items to be displayed in the scrollable region
            y_pos = 10

            # Iterate through the results
            for i in self.results:
                
                # Store the movie's id in the movie_tag variable
                movie_tag = i[0]

                # Output the poster, movie title, and description on the frame's canvas
                self.frame_canvas.create_image(10, y_pos, anchor=NW, image=i[-1], tags=movie_tag)
                self.frame_canvas.create_text(110, y_pos+5, anchor=NW, text=self.overflow(i[1], 25), font=(self.BODY_FONT, 30), fill="white", tags=movie_tag)
                self.frame_canvas.create_text(110, y_pos+55, anchor=NW, text=i[2], font=(self.BODY_FONT, 15), fill="white", tags=movie_tag)

                # Binds everything with the same tag (of the current movie's id) to a lambda function (which calls the self.movie_display()
                # method with the movie's id as the argument). Explanation of the lambda function logic can be found in the comments of the
                # self.display_watchlist() method:
                self.frame_canvas.tag_bind(movie_tag, "<ButtonPress-1>", lambda event, movie_tag=movie_tag: self.movie_display(movie_tag))

                # Increase the y-position for the next item
                y_pos += 150

            self.frame_canvas.update() # Update the frame canvas with the new items.
            
            # Button to go back to search screen again
            back_btn = Button(width=23, text="Search Again", font=(self.BODY_FONT, 18),
                        relief="ridge", bg="#060606", fg="white",
                        command=self.search)
            self.canvas.create_window(500,580, anchor=CENTER, window=back_btn)

    # Method used to search for movies
    def movie_search(self, query):

        # List to store the search results
        search_results = []

        # Get the raw results using the API link and requests.get()
        raw_results = requests.get(f"https://imdb-api.com/en/API/SearchMovie/{self.KEY}/{query}")

        # Since the data is in json format, turn it into a Python-useable dictionary
        # and get the results item from this dictionary
        results_dict = (raw_results.json())["results"]

        # Iterate through the results dictionary 
        for result in results_dict:
            
            # Create a list with the movie's id, title, description, and an image object
            # of the poster
            movie_info = [result["id"], result["title"], result["description"],
                        self.image_object((result["image"]), (81, 123))]
            
            # Append this list to the search results list
            search_results.append(movie_info)

        # Return the search results list
        return search_results

    # Method used to search for movies that match a certain genre
    def similar_movies(self, tags, avoid):

        # List to store the similar movies
        similars_results = []
    
        # Get the raw results using the API link and requests.get()
        raw_similars = requests.get(f"https://imdb-api.com/API/AdvancedSearch/{self.KEY}/?genres={tags}")
        
        # Since the data is in json format, turn it into a Python-useable dictionary
        # and get the results item from this dictionary
        similars_dict = raw_similars.json()["results"]

        # Iterate through the results dictionary
        for result in similars_dict:

            # As long as the movie is not the original movie provided (we wouldn't want to
            # recommend a movie that is the exact same as the one being viewed by the user)
            if result["id"] != avoid:

                # Create a list with the movie's id, title, description, and an image object
                # of the poster
                similars_info = [result["id"], result["title"], result["description"],
                                self.image_object((result["image"]), (81, 123))]

                # Append this list to the search results list
                similars_results.append(similars_info)

        # Shuffle the list of similar movies using random.shuffle()
        random.shuffle(similars_results)

        # Return the list of similar movies
        return similars_results

    # Method to cycle the list of similar movies to the right
    # (clicking the button also gives the method information
    # about the button-click event, hence the second parameter)
    def cycle_right(self, event):

        # Delete the similar movies currently on screen
        self.canvas.delete("sim")

        # Increase the starting point of the range of movies to
        # be displayed by 5
        self.sim_range += 5

        # If the index of the last movie that will be displayed
        # (starting index + 5) is out of range (larger than the
        # number of similar movies), reset the starting point to 0
        if (self.sim_range + 5) > len(self.similars):
            self.sim_range = 0

        # Use the self.display_similars() method to update the
        # display of similar movies on-screen
        self.display_similars()

    # Method to cycle the list of similar movies to the left
    # (clicking the button also gives the method information
    # about the button-click event, hence the second parameter)
    def cycle_left(self, event):

        # Delete the similar movies currently on screen
        self.canvas.delete("sim")

        # Decrease the starting point of the range of movies to
        # be displayed by 5
        self.sim_range -= 5

        # If the starting point is out of range (less than an index
        # of 0) set the starting point to be 6 fewer than the length
        # of the list (such that the movies to be displayed are from
        # the end of the list)
        if (self.sim_range) < 0:
            self.sim_range = len(self.similars) - 6

        # Use the self.display_similars() method to update the
        # display of similar movies on-screen
        self.display_similars()

    # Method for updating the display of similar movies on-screen
    def display_similars(self):

        # Iterates through 5 similar movies in the range starting
        # at the point specified by the sim_range variable
        for i in range(self.sim_range, (self.sim_range+5)):

            # Store the movie's id in the movie_tag variable
            movie_tag = self.similars[i][0]

            # Output the movie's poster on the canvas
            self.canvas.create_image((150+((i%5)*160)), 420, anchor=NW, image=self.similars[i][-1], tags=("sim", movie_tag))
            
            # Binds the poster with the tag of the current movie's id to a lambda function (which calls the self.movie_display()
            # method with the movie's id as the argument). Explanation of the lambda function logic below:
            self.canvas.tag_bind(movie_tag, "<ButtonPress-1>", lambda event, movie_tag=movie_tag: self.movie_display(movie_tag))

    # Method to trim long text and add "..." if required
    def overflow(self, text, space):

        # Checks if the given text fits within the provided space, and returns
        # the text unchanged if the above is true; otherwise, returns text trimmed
        # to the length of the given space with "..." concatenated to the end
        return text if (len(text) < space) else (text[:space] + "...")

    # Method to display details about the movie
    def movie_display(self, movie_id):
        self.clear_screen()
        
        # Get information about the movie using the self.movie_details() method
        self.movie_info = self.movie_details(movie_id)

        # Obtain the movies genres, and remove spacing between genres (so that the
        # string can be used in a url)
        genres = self.movie_info["genres"]
        genres = (''.join(genres.split()))

        # Get similar movies using the self.similar_movies() method
        self.similars = self.similar_movies(genres, movie_id)

        # Set the similar movies range to start at an index of 0
        self.sim_range = 0

        # Create the poster image
        self.canvas.create_image(50, 50, anchor=NW, image=self.movie_info["image"])

        # Create text with the movie's title
        self.canvas.create_text(200, 50, anchor=NW, text=self.overflow(self.movie_info["fullTitle"], 30),
                                font=(self.BODY_FONT, 30), fill="white")

        # Create text with the movie's runtime
        self.canvas.create_text(200, 105, anchor=NW, text=f'Runtime: {(self.movie_info["runtimeStr"])}',
                                font=(self.BODY_FONT, 15), fill="white")

        # Create text with the movie's genres
        self.canvas.create_text(200, 135, anchor=NW, text=f'Genres: {(self.movie_info["genres"])}',
                                font=(self.BODY_FONT, 15), fill="white")

        # Create text with the movie's IMDb rating
        self.canvas.create_text(750, 50, anchor=NW, text=f'IMDb: {(self.movie_info["imDb"])}',
                                font=(self.BODY_FONT, 15), fill="white")
        
        # Create text with the movie's Metacritic rating
        self.canvas.create_text(750, 80, anchor=NW, text=f'Metacritic: {(self.movie_info["metacritic"])}',
                                font=(self.BODY_FONT, 15), fill="white")

        # Create text with the movie's Rotten Tomatoes rating
        self.canvas.create_text(750, 110, anchor=NW, text=f'Rot. Tomatoes: {(self.movie_info["rottenTomatoes"])}',
                                font=(self.BODY_FONT, 15), fill="white")

        # Create text with the movie's content rating
        self.canvas.create_text(750, 140, anchor=NW, text=f'Content Rating: {(self.movie_info["contentRating"])}',
                                font=(self.BODY_FONT, 15), fill="white")

        # Create text with the movie's plot
        self.canvas.create_text(60, 250, anchor=NW, text=f'Plot: {self.overflow(self.movie_info["plot"], 280)}',
                                font=(self.BODY_FONT, 15), fill="white", width=900)

        # Create heading text for the movie recommendation 
        self.canvas.create_text(60, 350, anchor=NW, text="Recommendations",
                                font=(self.BODY_FONT, 20), fill="white")

        # Create left & right arrows to cycle through similar movies, and bind them to 
        # their respective methods
        self.canvas.create_image(910, 470, anchor=NW, image=self.right_arrow, tags="right")
        self.canvas.tag_bind("right", "<ButtonPress-1>", self.cycle_right)

        self.canvas.create_image(80, 470, anchor=NW, image=self.left_arrow, tags="left")
        self.canvas.tag_bind("left", "<ButtonPress-1>", self.cycle_left)

        # Create a button that allows the user to add/remove the current movie to/from
        # their watchlist
        add_rem = Button(width=20, text="Watchlist: Add/Remove", font=(self.BODY_FONT, 12),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.modify_list)
        self.canvas.create_window(200, 180, anchor=NW, window=add_rem)

        # Use the self.display_similars() display the similar movies on-screen
        self.display_similars()

        # Create a button to return back to the home screen
        go_home = Button(width=14, text="Back to Home", font=(self.BODY_FONT, 16),
                    relief="ridge", bg="#060606", fg="white",
                    command=self.home)
        self.canvas.create_window(800, 590, anchor=NW, window=go_home)

    # Method to obtain the details for a movie
    def movie_details(self, movie_id):

        # Tuple of all the relevant keys needed for movie information
        KEY_LIST = ("fullTitle",
                    "genres",
                    "runtimeStr",
                    "plot",
                    "contentRating")

        # Tuple of all the relevant keys needed for rating information
        RATING_LIST = ("imDb",
                    "metacritic",
                    "rottenTomatoes")

        # Get the raw results using the API link and requests.get()
        raw_details = requests.get(f"https://imdb-api.com/en/API/Title/{self.KEY}/{movie_id}")
        
        # Since the data is in json format, turn it into a Python-useable dictionary
        details_dict = raw_details.json()
        
        # Initialize the dictionary for storing key details
        key_details = {}

        # Create an "id" key, and set it to the movie's id
        key_details["id"] = movie_id

        # Get the raw ratings using the API link and requests.get()
        raw_ratings = requests.get(f"https://imdb-api.com/API/Ratings/{self.KEY}/{movie_id}")
        
        # Since the data is in json format, turn it into a Python-useable dictionary
        ratings_dict = raw_ratings.json()

        # Create an "image_url" key, and set it to the url of the movie's poster
        key_details["image_url"] = details_dict["image"]

        # Create an "image" key, and set it to an image object that comes from the url of the poster
        key_details["image"] = self.image_object((key_details["image_url"]), (122, 185))

        # Iterates through the tuple of movie information keys, and appends the corresponding
        # item from the details_dict (if it exists, otherwise set it to "N/A")
        for i in KEY_LIST:
            key_details[i] = (details_dict[i] if details_dict[i] != None else "N/A")

        # Iterates through the tuple of movie rating keys, and appends the corresponding
        # item from the ratings_dict (if it exists, otherwise set it to "N/A")
        for i in RATING_LIST:
            key_details[i] = (ratings_dict[i] if ratings_dict[i] not in (None, "") else "N/A")

        # Return the dictionary with the relevant information
        return key_details
    
    # Method to modify the user's watchlist
    def modify_list(self):

        # Variable to indicate if the movie was found within the list
        in_list = False
        
        # Create a string with information about the current movie to be added/removed
        current_movie = f'{self.movie_info["id"]}|{self.movie_info["fullTitle"]}|{self.movie_info["image_url"]}'

        # Opens the user's text file and stores all of the lines in a list
        with open(f"database/{self.uname}.txt", "r") as f:
            user_list = f.readlines()

        # Opens the user's text file in write mode
        with open(f"database/{self.uname}.txt", "w") as f:

            # Iterate through the user's watchlist
            for i in user_list:
                
                # Check if the movie (with the newline character stripped) is the same
                # as the one that needs to be added/removed
                if i.strip() == current_movie:

                    # If its the same, then change the in_list variable to True to
                    # indicate that the movie has been found (and do not write it to
                    # the file, since it needs to be removed)
                    in_list = True

                # Otherwise, write the movie back into the file
                else:
                    f.write(i)
            
            # If the movie to be added/removed was not found in the list,
            # that means it needs to be added to the list
            if not in_list:
                
                # Write the current movie to the file with a newline character
                f.write(current_movie+"\n")

                # Display a message to show that the movie has been added to the list
                messagebox.showinfo("List Modified","Added to list.")
            
            # Otherwise, if the movie was found in the list (and hence got removed),
            # display a message to show that the movie has been removed from the list
            else:
                messagebox.showinfo("List Modified","Removed from list.")
