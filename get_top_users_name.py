import os
import csv
from collections import defaultdict
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load the .env file
load_dotenv()

# Set your Slack API token
slack_api_token = os.environ["SLACK_API_TOKEN"]

# Initialize the Slack API client
slack_client = WebClient(token=slack_api_token)

csv_filename = "reaction_counts.csv"

# Read the data from the CSV file
user_reaction_counts = defaultdict(int)
with open(csv_filename, "r", newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        user_id, _, count = row
        user_reaction_counts[user_id] += int(count)

# Sort the user_reaction_counts dictionary by count
sorted_user_reaction_counts = sorted(
  user_reaction_counts.items(), key=lambda x: x[1], reverse=True)


def get_user_name(user_id):
    try:
        response = slack_client.users_info(user=user_id)
        user = response["user"]
        user_name = user.get("real_name", user["name"])
        return user_name
    except SlackApiError as e:
        print(f"Error: {e}")
        return user_id


# Print the top 30 users with summarized reaction counts
print("User Name - Total Count")
for user_id, total_count in sorted_user_reaction_counts[:50]:
    user_name = get_user_name(user_id)
    print(f"{user_name} - {total_count}")
