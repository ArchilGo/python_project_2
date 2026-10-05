# Personal Library

A console-based Personal Library Management System built with Python.

## Features

- Add books to a personal library
- Support for Printed Books, eBooks, and AudioBooks
- Search books by title
- Display all books
- Store books permanently in a JSON file
- Automatically load books from JSON when the program starts
- Track book status:
  - Wish List
  - In Library
  - Borrowed Out
- Track borrower and borrowed date for printed books

## Book Types

### Printed Book

Contains:
- Title
- Author
- Publication year
- Genre
- Number of pages
- Status
- Borrower information when borrowed

### eBook

Contains:
- Title
- Author
- Publication year
- Genre
- Number of pages
- Status

### AudioBook

Contains:
- Title
- Author
- Publication year
- Genre
- Duration
- Status

## Technologies

- Python
- Object-Oriented Programming (OOP)
- JSON

## Run the Project

Run:

```bash
python3 main.py
```

## Requirements

- Python 3.8 or newer
- No third-party packages (see `requirements.txt`)
