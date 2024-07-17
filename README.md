
# LibraryDB

This repository contains a database management system for a library, implemented in Python.

## Overview

The LibraryDB project aims to provide a simple yet effective database system for managing library records. It includes functionalities for adding, removing, and searching for books within the library's collection.

## Features

- Add new books to the database
- Remove books from the database
- Search for books by title, author, or ISBN
- Display all books in the database

## Getting Started

### Prerequisites

- Python 3.x
- SQLite

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/MatijaMikulic/LibraryDB.git
   ```
2. Navigate to the project directory:
   ```sh
   cd LibraryDB
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. Initialize the database:
   ```sh
   python init_db.py
   ```
2. Run the main application:
   ```sh
   python main.py
   ```

### Directory Structure

- `db/`: Contains the SQLite database file.
- `scripts/`: Contains scripts for database initialization and manipulation.
- `main.py`: Main application script.
- `init_db.py`: Script to initialize the database.
- `requirements.txt`: Python dependencies.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Open-source community for their support and contributions.

