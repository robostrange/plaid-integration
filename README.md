# Plaid Integration Project

## Current Version: 2023.12.19.1

This is a personal project for managing financial transactions using Plaid API and updating them in an Excel workbook. It's a work in progress with features being added and refined over time.

### Features

- **Transaction Fetching**: Retrieves transaction data from Plaid.
- **Excel Integration**: Formats and updates transaction data into an Excel workbook without corrupting it.
- **Error Handling**: Manages API and file-related errors.

### Setup

1. Clone the repo.
2. Install dependencies in a virtual environment.
3. Set up `.env` with necessary Plaid API keys and tokens.
4. Run `main.py` to execute the script.

### Usage

Run `main.py` whenever you need to fetch and update transaction data. The script handles everything from fetching data from Plaid to writing it into an Excel workbook.

### Changelog for 2023.12.19.1

- Enhanced data fetching from Plaid API.
- Improved formatting for Excel output.
- Refined error handling mechanisms.
- Code refactoring for better structure and readability.
- Initiated basic versioning and documentation.

### To-Do List

- [ ] Add detailed comments and docstrings for better code understanding.
- [ ] Implement robust error handling and logging for efficient debugging.
- [ ] Enhance the data formatting process in `format_transactions` function.
- [ ] Explore options to append data to the Excel sheet instead of overwriting.
- [ ] Set up a system to automatically update version numbers with each commit.
- [ ] Consider automating the script to run at regular intervals.

### Notes

This project is tailored for personal use, focusing on functionality and learning. While it's not set up for external contributions, feedback or suggestions are always welcome.

### License

This project is for personal use and is not licensed for public distribution or use.

---

Remember to update this document as the project evolves, especially the version number and to-do list.
