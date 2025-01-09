-- Schema for the Library Management System

-- Table for books
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);

-- Table for members
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
