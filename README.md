# My Movie Ratings

#### (Click to redirect to deployed app)[https://my-movie-ratings.herokuapp.com]

My Movie Ratings is an app for tracking, rating and commenting movies and shows you have watched.

This is a terminal app, where you can Add your movie, Edit or Delete them, and view all movie entries to see what you watched.


## How to Use

- Go to https://my-movie-ratings.herokuapp.com and the app should be ready touse.
- To choose what to do in the app, you need to navigate in menu with options from 1 to 5.
- 



## Features:

### Existing Features: 

- Menu
    - Menu acts as a point where users can choose what actions they need to complete
    - A short welcome message is displayed to show app name and its purpose
    - Navigation thru menu is done by inputting a number between 1 and 5.
    - Following actions are available in menu:
        - Add a new moview rating
        - Edit an existing movie rating
        - Delete an existing movie rating
        - See all movie ratings
        - Exit


- Adding Movie Rating
    - This feature allows users to input info about movie and store them in Google Sheet
    - Data is stored as table with following categoruies:
        - ID
        - Title
        - Genre
        - Rating
        - Comments
    - User is asked to input Title, Genre, Rating and Comments, while Comments is optional
    - Rating input must be an integer between 0 and 5
    - Also, some confirmation messages are displayed to let user know that action completed successfully

- Editing Movie Rating
    - This feature allows to edit the data already stored in Google Sheets, in case of user changed mind, or made a mistake
    - To make editing convenient, if users want to changed only a certain category they can easily skip a step by pressing Enter

- Deleting Movie Rating
    - In case user decided to remove existing data, this feature will allow user with ease to do so only by entering ID of the movie
    - For users convenience, table with existing movies displayed

- Seeing All Movies
    - Finally, users can see all entries they made. This way they can see and compare movies/shows they watched and rated

- Data Validations and Error Handling
    - Each input that made by a user is validated to make sure that correct data type and format are entered
    - In case, user entered wrong input they will see a message explaining what is wrong and how to fix

