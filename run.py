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
            delete_movie()
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