# BookVerse

BookVerse is a user-friendly website designed for book lovers. It allows users to search for books by title, author, or keyword, and presents them with a list of related books. Users can access detailed information about each book, write reviews about a book and view reviews from other BookVerse members. Additionally, they can have access to a bookshelf where they can add books they want to read and remove them once finished, ensuring your reading list stays updated and organized.

## Contents

- [Teck Stack](#techstack)
- [API](#api)
- [Features](#features)
- [Installation](#installation)
- [For version 2.0](#version2)
- [About the developer](#about)

## <a name="techstack"></a>Tech Stack

- Python
- Flask
- Jinja
- PostgresSQL
- SQAlchemy
- Passlib
- Bootstrap
- Javascript
- AJAX
- HTML
- CSS

## <a name="api"></a> API

[Google books API](https://developers.google.com/books/docs/overview)

## <a name="features"></a> Features

### Book search and view details

Search for books by title, author or keywords. View results of search and details of a specific book. User account registration not required.

![Book search logged out](book-search-details.gif)
<br /> <br />

### Password hashing

When a user creates a new account their password is hashed using Passlib library and the PBKDF2-SHA256 algorithm, only the hashed password is saved to the database and when a user log in, it's used the verify() function from the library that returns a boolean value based on the success of the verification.

`hashed_password = pbkdf2_sha256.hash(password)`

`pbkdf2_sha256.verify(password, user.password)`

### Bookshelf

Create a account or login to have a bookshelf and add books you want to read to it. After reading the book you can remove it from the list.

![Bookshelf](bookshelf.gif)
<br /> <br />

### Reviews

To view reviews you don't need to be logged in.
To write a review you need to create an account or login.

![Reviews](reviews.gif)
<br /> <br />

## <a name="installation"></a> Intallation

### Requirements

- PostgreSQL
- Python
- Google Books API key

To have this app running on your local computer, please follow the below steps:

### Steps

1. Clone the github repository:

```
$ git clone https://github.com/Danieli-Costa/BookVerse.git
```

2. Create a virtual environment:

```
$ virtualenv env
```

3. Activate the virtual environment:

```
$ source env/bin/activate
```

4. Install dependencies:

```
pip3 install -r requirements.txt
```

5. Get an API key from Google Books API and add your API key to a `secrets.sh` file.

6. Create your database:

```
$ createdb databasename
```

7. Create your database tables:

```
$ python3 seed_database.py
```

8. Run the Flask server:

```
$ python3 server.py
```

## <a name="version2"> For version 2.0

- Goal setting (set quantity of books per year or per month that the user wants to read).
- Visual graphic showing how much of your goal you achieved.
- On the profile/goals display how many days the user have left to achieve their goal.
- Option to edit and remove reviews made by the user.
- Option to change password and edit informations from the user's account.

## <a name="about"></a> About the Developer

Danieli Chamberlain is a Software Engineer in the Bay Area. This is her first full-stack project.
She can be found on [LinkedIn](https://www.linkedin.com/in/danieli-chamberlain-14a530225/) and on [Github](https://github.com/Danieli-Costa)
