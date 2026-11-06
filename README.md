# Personal Library Tracker

Catalog books, track reading status, manage checkouts and due dates, search your shelves, and export a CSV.

[![Build and verify](https://github.com/netcodermike/personal-library-tracker/actions/workflows/verify.yml/badge.svg)](https://github.com/netcodermike/personal-library-tracker/actions/workflows/verify.yml)

**Language:** Python · **Platform:** Windows, macOS, Linux desktop · **App type:** Desktop book catalog and lending app

First-release learning implementation, with explicit scope below. This is one independently runnable app, not a placeholder in a combined repository.

## Features

- Add titles/authors and track unread, reading, or finished status.
- Check books out to borrowers, record due dates, and return them.
- Literal substring search with overdue rows highlighted.
- Durable SQLite storage and spreadsheet-safe CSV export.

## Requirements

Python 3.11+ with SQLite and Tkinter (standard-library modules). Some Linux distributions package Tkinter separately as python3-tk. No pip packages.

## Quick start

```sh
git clone https://github.com/netcodermike/personal-library-tracker.git
cd personal-library-tracker
python library.py
# Separate catalog:
python library.py --store my-books.sqlite3
```

Commands run from the repository root. Lines marked for a particular operating system apply only there. Language tools are prerequisites, not installed by the app. Close desktop windows normally; terminal/server apps stop with Ctrl+C unless their usage notes say otherwise.

## Example workflow

Add Dune by Frank Herbert, set reading status, then check it out to a borrower with an ISO due date. A second checkout is rejected until the book is returned. Search for the author, export CSV, close/reopen, and verify the catalog persists.

## Architecture, configuration, and data

`library.py` separates a SQLite-backed Library model from the Tkinter view. The books table has id/title/author/status/borrower/due; schema version 1 is stored in PRAGMA user_version. Parameterized queries and transactions handle writes. Search escapes SQL LIKE wildcard characters and uses SQLite’s built-in case behavior. Due dates are canonical ISO dates; overdue means a checked-out book’s date precedes the current local date. The default file is library.sqlite3; --store changes it. CSV export prefixes formula-like text with an apostrophe. `test_library.py` covers lending/state transitions, validation, persistence, literal search, and export.

## Verification

Build with the quick-start command where needed, then run:

```sh
python -m unittest -v
```

Manual acceptance: Add two books, change reading status, lend/return one, test an overdue date and duplicate checkout, search for literal % or _, export CSV, and reopen the catalog.

See [validation record](docs/VALIDATION.md) for observed checks and their limits. CI results verify only what the workflow runs; they do not establish native GUI correctness or production readiness.

## Limitations and next steps

No ISBN lookup, cover download, editing/deleting books, reading statistics, lending history, multiple copies, or notifications. Duplicate titles are separate book records. Borrowers and reading status are independent. Search’s case folding is SQLite’s built-in behavior rather than full Unicode normalization. Data is plaintext. Back up the database while the app is closed. CSV export replaces the selected output file.

## Troubleshooting

Install Tkinter if importing it fails, and launch from a graphical desktop. A nonexistent parent folder for --store must be created first. Unknown schema versions are rejected. SQLite busy/permission errors indicate another writer or an unwritable store. Use YYYY-MM-DD for due dates. Preserve a damaged database before attempting recovery.

## Source map

- `library.py`
- `test_library.py`

## Development and license

Read [contributing](CONTRIBUTING.md) before changing the app, and [security/privacy](SECURITY.md) before supplying private data. Use synthetic fixtures for tests. No telemetry, paid API key, or account is required by the app itself. Dependencies, when present, are stated in Requirements.

[MIT license](LICENSE), copyright 2026 netcodermike.
