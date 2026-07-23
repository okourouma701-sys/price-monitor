# Price Monitor

A web scraping tool that tracks product prices over time, stores them in a SQLite database, and generates visual reports.

## The problem it solves

Businesses need to know how competitor prices change over time. Checking manually is slow and easy to forget. This tool collects prices automatically and builds the history for you.

## Features

- **Automated scraping** — collects product names and prices from a live website
- **Time-series storage** — every run is saved to SQLite with a timestamp, building price history
- **Instant insights** — total records, average price, cheapest and most expensive product
- **Visual report** — generates a bar chart of the top 10 most expensive products

## Demo

![Demo](price_report.png)

## How it works

1. Scrapes product data with `requests` + `BeautifulSoup`
2. Stores each record in a SQLite table with an auto-incrementing ID and timestamp
3. Runs SQL queries to calculate insights
4. Renders a chart with `matplotlib` and saves it as a PNG

## Built with

Python · `requests` · `BeautifulSoup` · `sqlite3` · `matplotlib` · `datetime`

## Usage

```
python3 price_monitor.py
```

Each run scrapes fresh prices, adds them to the database, prints insights, and regenerates the chart.
