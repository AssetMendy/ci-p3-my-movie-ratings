import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

# Define the scope of the API access
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Define the credentials and authorize the API access
CREDS  = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT  = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheet
SHEET = GSPREAD_CLIENT.open('my_movie_ratings').worksheet('movies')


def add_movie_rating():

    """
        This function gets Movie Title, Genre, Rating, and Comment.
        Then ID is assigned to a row of data based on other data in
        Google Sheets. After, it sends the data to Google Sheets.
    """

    while True:
        movie_title = input("Enter the movie title: ")
        if not movie_title:
            print("Title cannot be empty. Please enter a valid title.")
        else:
            break
    movie_genre = input("Enter the genre: ")
    while True:
        try:
            movie_rating = int(input("Enter your rating (0-5): "))
            if movie_rating < 0 or movie_rating > 5:
                print("Rating must be between 0 and 5. Please enter a valid rating.")
            else:
                break
        except ValueError:
            print("Rating must be an integer. Please enter a valid rating.")
    movie_comment = input("Enter your comment: ")
    movie_id = len(SHEET.get_all_values())  # exclude the first row
    if movie_id == 0:
        movie_id = 1  # start with ID 1 if sheet is empty
    row = [movie_id, movie_title, movie_genre, movie_rating, movie_comment]
    SHEET.append_row(row)
    print("Movie added successfully!")


# Function to delete an existing movie rating from the sheet
def delete_movie_rating():
    get_all_movies()
    # Get the ID of the movie to be deleted from the user
    movie_id = input("Enter the ID of the movie to delete: ")
    
    # Find the row index of the movie with the given ID
    row_index = None
    for i in range(1, len(SHEET.get_all_values())):
        row = SHEET.row_values(i)
        if row[0] == movie_id:
            row_index = i
            break


# Get all the rows from the sheet
def get_all_movies():

    """
    Gets ID, Title, Genre, Rating and Comment from Google Sheet,
    then displays it to a user in a clean table view with help of
    tabulate module
    """
    # Get all the rows from the sheet
    rows = SHEET.get_all_values()
    # Exclude the header row
    headers = rows.pop(0)
    # Display the rows as a table
    table = tabulate(rows, headers=headers, tablefmt='orgtbl')
    print(table)
    return table


def menu():
    """
        This function is main point of interaction of user with the app.
        It shows welcome message for the app. Then it opens the menu.
        Menu has Add, Edit, Delete, See all and Exit options.
        User can navigate in menu choosing from 1 to 5.
    """

    print(
    """
    Welcome to My Movie Ratings app!

    This is your library to keep track of
    movies you have watched and rate them.
    """
    )
    while True:
        print('\n==== MENU ====')
        print("\nSelect an option:")
        print('1. Add a new movie rating')
        print('2. Edit an existing movie rating')
        print('3. Delete an existing movie rating')
        print('4. See all movie ratings')
        print('5. Exit')
        user_choice = input("Enter your choice (1-5): ")

        if user_choice == "1":
            add_movie_rating()
        elif user_choice == "2":
            edit_movie()
        elif user_choice == '3':
            delete_movie_rating()
        elif user_choice == "4":
            movies = get_all_movies()
            if movies:
                print("Movies watched:")
                for movie in movies:
                    print(movie[0], movie[1])
            else:
                print("No movies found.")
        elif user_choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    menu()

menu()