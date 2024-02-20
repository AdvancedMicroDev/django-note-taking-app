# Note Taking App

This is a simple note taking app built with Django and Django Rest Framework.

## Features

- User Registration: Allows users to create an account by providing necessary information such as username, email, and password.
- User Login: Allows users to log in to their account by providing their credentials (username/email and password).
- Create New Note: Create a new note. Only authenticated users can create a new note.
- Get a Note: Retrieve a specific note by its ID. Only authenticated users can retrieve a note.
- Share a Note: Share a note with other users. Only the owner of the note can share it.
- Update a Note: Update an existing note. Only the owner of the note and users it is shared with can update it.
- Get Note Version History: Retrieve the version history of a note. Only the owner of the note and users it is shared with can retrieve the version history.

## Installation

1. **Clone this repository**: This will create a copy of this project on your local machine.
    ```bash
    git clone https://github.com/AdvancedMicroDev/django-note-taking-app.git
    ```
2. **Navigate to the project directory**: Change your current working directory to the project directory.
    ```bash
    cd NoteTakingApp
    ```
3. **Create a virtual environment**: A virtual environment is a way to keep the project's dependencies isolated from other projects.
    ```bash
    python3 -m venv venv
    ```
4. **Activate the virtual environment**: This command will change the context to the virtual environment.
    ```bash
    source venv/bin/activate
    ```
5. **Install the requirements**: This will install all the dependencies that the project needs to run.
    ```bash
    pip install -r requirements.txt
    ```
6. **Apply the migrations**: This will apply all the database migrations.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. **Run the server**: This will start the server.
    ```bash
    python manage.py runserver
    ```

Now you can access the API at `http://localhost:8000`.

## Testing 
> TODO Rewrite failing tests -> <mark>5P 2F</mark>

To run the tests, use the following command:

```bash
python manage.py test
```

## <mark>Admin</mark> Credentials:
* username: gautam
* password: Helloworld^^

## Usage Examples
Here are *some examples* of how you can use the API:

1. User Registration: To register a new user, send a POST request to /signup with the username, email, and password in the request body.
2. User Login: To log in a user, send a POST request to /login with the username and password in the request body.
3. Create New Note: To create a new note, send a POST request to /notes/create with the title and content in the request body.
4. Get a Note: To retrieve a specific note, send a GET request to /notes/{id}.
5. Share a Note: To share a note with other users, send a POST request to /notes/share with the note ID and usernames in the request body.
6. Update a Note: To update an existing note, send a PUT request to /notes/{id} with the new content in the request body.
7. Get Note Version History: To retrieve the version history of a note, send a GET request to /notes/version-history/{id}.

> You can also visit the admin panel `(http://localhost:8000/admin)` using the above admin credentials & do the same on an interactive UI.

**For more details about the API, please refer to the source code.**