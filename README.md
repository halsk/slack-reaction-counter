# Slack Reaction Counter

This repository contains Python scripts that use the Slack API to count specific reactions in a Slack workspace, and then display the top 30 users with the most reactions.

## Scripts

1. `count_reactions.py` - Fetches messages with specific reactions, counts reactions per user, and saves the data to a CSV file called `reaction_counts.csv`.

2. `summarize_and_display_top_users.py` - Reads the reaction counts from the `reaction_counts.csv` file, summarizes the counts by user, sorts the users by count, and displays the top 30 users with their user names and total counts.

## Prerequisites

- Python 3.6 or higher
- [slack-sdk](https://pypi.org/project/slack-sdk/) Python package
- [python-dotenv](https://pypi.org/project/python-dotenv/) Python package

## Setup

1. Create a virtual environment and activate it:

   ```bash
   source venv/bin/activate (Linux/Mac)
   venv\Scripts\activate (Windows)
   ```

2. Install the required packages:

   ```bash
   pip install -r requirement.txt
   ```

3. Create a `.env` file in the project directory and add your Slack API token:

   ```ini
   SLACK_API_TOKEN=your_slack_api_token
   ```

Replace `your_slack_api_token` with your actual Slack API token.

## Usage

1. Run the `get_count.py` script to fetch messages with specific reactions and save the reaction counts to the `reaction_counts.csv` file:

   ```bash
   python get_count.py
   ```

2. Run the `get_top_users_name.py` script to read the reaction counts from the `reaction_counts.csv` file, summarize the counts by user, and display the top 30 users with their user names and total counts:

   ```bash
   python get_top_users_name.py
   ```

## Customization

- To count different specific reactions, modify the `specific_reactions` list in the `get_count.py` script.
- To change the number of top users displayed, modify the slice in the `for` loop in the `get_top_users_name.py` script.
