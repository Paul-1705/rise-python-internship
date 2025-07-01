# Expense Tracker

A modern, user-friendly desktop app to track your expenses, visualize spending, and gain insights into your financial habits. Built with Python and Tkinter, featuring a beautiful UI, dark mode, charts, and summaries.

---

## Features
- **Add Expenses:** Enter category, amount, and date for each expense.
- **Recent Expenses:** View your latest expenses instantly.
- **Dashboard:** See total expenses and number of entries.
- **Monthly Summary:** View expenses grouped by month with monthly totals.
- **Charts:** Visualize your spending by category (pie chart).
- **Dark Mode:** Toggle between light and dark themes with one click.
- **Modern UI:** Clean, card-based layout inspired by web dashboards.

---

## Screenshots

> ![App Screenshot](screenshot.png)

---

## Installation

1. **Clone the repository or copy the files:**
   ```sh
   git clone <your-repo-url>
   cd expense_tracker
   ```

2. **Install required packages:**
   ```sh
   pip install tkcalendar matplotlib
   ```
   - `tkcalendar` is required for the date picker.
   - `matplotlib` is required for the charts tab (optional, but recommended).

---

## Running the App

```sh
python expense_tracker_app.py
```

---

## Usage

- **Add Expense:**
  - Fill in the category, amount, and date, then click "Add Expense".
  - Your entry will appear in the Recent Expenses list and update the totals.

- **Switch Tabs:**
  - Use the navigation bar at the top to switch between Dashboard, Add Expense, Monthly Summary, and Charts.

- **Dark Mode:**
  - Click the "🌙 Dark Mode" button (top right) to toggle dark/light themes.

- **Charts:**
  - The Charts tab shows a pie chart of your expenses by category (requires matplotlib).

---

## Credits
- Developed by [Your Name]
- UI inspired by modern web dashboards

---

## License

[Add your license here] 