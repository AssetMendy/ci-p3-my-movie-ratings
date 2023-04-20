import gspread
import time
from google.oauth2.service_account import Credentials
from tabulate import tabulate

# Define the scope of the API access
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Define the credentials and authorize the API access
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheet (change Spreadsheet and Worksheet names with yours )
SHEET = GSPREAD_CLIENT.open('my_movie_ratings').worksheet('movies')


def add_movie_rating():

    """
        This function gets Movie Title, Genre, Rating, and Comment.
        Then ID is assigned to a row of data based on other data in
        Google Sheets. After, it sends the data to Google Sheets.
    """

    print(
        """
            Let's get started! Here you can store your ratings!
        """
    )
    time.sleep(1)

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
                print("Rating must be between 0 and 5. Enter a valid rating.")
            else:
                break
        except ValueError:
            print("Rating must be an integer. Please enter a valid rating.")
    movie_comment = input("Enter your comment (optional): ")
    movie_id = len(SHEET.get_all_values())  # exclude the first row
    if movie_id == 0:
        movie_id = 1  # start with ID 1 if sheet is empty
    row = [movie_id, movie_title, movie_genre, movie_rating, movie_comment]
    SHEET.append_row(row)
    time.sleep(1)
    print("\nSending your inputs to database...")
    time.sleep(2)
    print("\nMovie added successfully!")
    time.sleep(2)


def edit_movie_rating():

    """
        This function allows user to edit a certain movie rating.
        1. It runs get_all_movies() to show existing data as a table.
        2. User refers to the table and chooses ID of data to edit.
        3. User is asked to update the data for chosen row, if no changes
        needed user can press Enter to skip
        4. Finally, new inputs are sent to Google Sheet to update rows
        5. get_all_movies() runs again to show table with updated data
        6. User is returned to menu section
    """

    get_all_movies()  # Show table with current movies in library for reference

    # Get the movie ID to edit from the user
    while True:
        try:
            movie_id = int(input("\nEnter the ID of the movie to edit: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid ID.")

    # Get the row corresponding to the movie ID
    values = SHEET.get_all_values()
    rows = values[1:]
    row_index = -1
    for i in range(len(rows)):
        if int(rows[i][0]) == movie_id:
            row_index = i
            break
    if row_index == -1:
        print("Movie ID not found.")
        return

    # Get the updated title, can be left blank to not change anything
    updated_title = input("Enter new movie title (leave blank to skip): ")
    if updated_title == "":
        updated_title = rows[row_index][1]

    # Get the updated genre, can be left blank to not change anything
    updated_genre = input("Enter new genre (leave blank to skip): ")
    if updated_genre == "":
        updated_genre = rows[row_index][2]

    # Get the updated rating, can be left blank to not change anything
    # Validated that rating value is correct data type
    while True:
        try:
            updated_rating_str = input("Enter new rating (0-5) (leave blank to skip): ")
            if not updated_rating_str:
                updated_rating = rows[row_index][3]
            else:
                updated_rating = int(updated_rating_str)
                if updated_rating < 0 or updated_rating > 5:
                    print("Rating must be between 0 & 5. Enter a valid rating")
                    continue
            break
        except ValueError:
            print("Rating must be an integer. Please enter a valid rating.")

    # Get the updated comment, can be left blank to not change anything
    updated_comment = input("Enter new comment (leave blank to skip): ")
    if updated_comment == "":
        updated_comment = rows[row_index][4]

    # Update the row in the sheet with corresponding changes from user side
    # add 2 to row index to account for header row
    SHEET.update_cell(row_index + 2, 2, updated_title)
    SHEET.update_cell(row_index + 2, 3, updated_genre)
    SHEET.update_cell(row_index + 2, 4, updated_rating)
    SHEET.update_cell(row_index + 2, 5, updated_comment)

    print("\nMovie updated successfully!\n")
    time.sleep(1)
    get_all_movies()  # Return updated table to show user choices applied
    time.sleep(3)
    print("\nReturning to menu...")
    time.sleep(2)


def delete_movie_rating():

    """
        This function allows user to delete a certain row of data
        from Google Sheet. To choose which row to delete function
        asks for its ID. Finally, it runs update_ids() to update
        all IDs to make sure that ID are in order
    """

    get_all_movies()
    # Get the ID of the movie to be deleted from the user
    movie_id = input("\nEnter the ID of the movie to delete: ")

    # Find the row index of the movie with the given ID
    row_index = None
    for i in range(1, len(SHEET.get_all_values())+1):
        row = SHEET.row_values(i)
        if row[0] == movie_id:
            row_index = i
            break

    # If the movie with the given ID is found,
    # delete the row and update the IDs of remaining rows
    if row_index is not None:
        SHEET.delete_rows(row_index)
        # Update the IDs of remaining rows
        for i in range(row_index, len(SHEET.get_all_values())):
            SHEET.update_cell(i+1, 1, i)
        print(f"Movie with ID {movie_id} deleted successfully.")
        time.sleep(1)
        update_ids()  # Updates IDs for the data in Google Sheet
    else:
        print(f"No movie found with ID {movie_id}.")
        time.sleep(1)
        print("Returning to menu...")
        time.sleep(2)


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


def update_ids():

    """
        This function iterates thru ID column in Google Sheet
        and updates them to be in sequential order from 1.
    """

    # Loop over all rows in the worksheet, skipping the header row
    for i, row in enumerate(SHEET.get_all_values()[1:], start=1):
        # Update the ID value in the first column of the row
        SHEET.update_cell(i + 1, 1, i)
    print("IDs updated successfully.")
    time.sleep(2)


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
            edit_movie_rating()
        elif user_choice == '3':
            delete_movie_rating()
        elif user_choice == "4":
            print("Ok... Here are the movies you watched and rated so far: \n")
            time.sleep(1)
            get_all_movies()
            time.sleep(5)
        elif user_choice == "5":
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def main():
    menu()


main()
