import os
import csv
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load the .env file
load_dotenv()

# Set your Slack API token
slack_api_token = os.environ["SLACK_API_TOKEN"]

# Initialize the Slack API client
slack_client = WebClient(token=slack_api_token)

# Define the specific reactions you want to count
# Replace with the specific reactions you want to count
specific_reactions = ["kyoso_b", "kyoso_g", "kyoso_r", "kyoso_y"]


def get_channels():
    try:
        response = slack_client.conversations_list()
        channels = response["channels"]
        return channels
    except SlackApiError as e:
        print(f"Error: {e}")
        return []


def join_channel(channel_id):
    try:
        slack_client.conversations_join(channel=channel_id)
    except SlackApiError as e:
        print(f"Error: {e}")


def get_messages_with_specific_reactions(channel_id, specific_reactions):
    messages_with_specific_reactions = []
    cursor = None

    while True:
        try:
            response = slack_client.conversations_history(
              channel=channel_id, cursor=cursor)
            messages = response["messages"]
            messages_with_specific_reactions.extend(
              [msg for msg in messages if "reactions" in msg and any(
                reaction["name"] in specific_reactions for reaction in
                msg["reactions"])])

            cursor = response.get("response_metadata", {}).get("next_cursor")

            if not cursor:
                break
        except SlackApiError as e:
            print(f"Error: {e}")
            break

    return messages_with_specific_reactions


def get_users_and_counts_for_specific_reactions(messages, specific_reactions):
    user_counts = {}
    for message in messages:
        for reaction in message["reactions"]:
            if reaction["name"] in specific_reactions:
                for user in reaction["users"]:
                    user_counts[user] = user_counts.get(user, 0) + 1
    return user_counts


channels = get_channels()

# Prepare the CSV file
csv_filename = "reaction_counts.csv"
with open(csv_filename, "w", newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["user_id", "channel_id", "count"])

    for channel in channels:
        print(f"Channel: {channel['name']}")

        if not channel["is_member"]:
            join_channel(channel["id"])

        messages = get_messages_with_specific_reactions(
          channel["id"], specific_reactions)
        user_counts = get_users_and_counts_for_specific_reactions(
          messages, specific_reactions)

        if user_counts:
            for user_id, count in user_counts.items():
                # Write the user_id, channel_id, and count to the CSV file
                csv_writer.writerow([user_id, channel["id"], count])

    print(f"Reaction count data saved to {csv_filename}")
