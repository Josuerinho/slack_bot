__all__ = ['EnhancedSlackBot'] # this restricts the import to only the EnhancedSlackBot class and nothing else when doing import *

from slack_sdk import WebClient  
from slack_sdk.errors import SlackApiError  
from datetime import datetime
import json
import os  

# Usage  
# SLACK_TOKEN = "xoxb-your-token-here"  
# client = WebClient(token=SLACK_TOKEN)  
# invite_bot_to_channel(client, "C0123456789")  # Replace with your channel ID  

class EnhancedSlackBot:  
    def __init__(self, config_path):  
        self.config = self._load_config(config_path)  
        self._client = WebClient(token=self.config['slack_token'])  

    def _load_config(self, config_path):  
        """Load configuration from JSON file"""  
        file_extension = os.path.splitext(config_path)[1].lower()  

        try:  
            with open(config_path, 'r') as file:  
                if file_extension == '.json':  
                    return json.load(file)  
                else:  
                    raise ValueError(f"Unsupported config file format: {file_extension}")  
        except FileNotFoundError:  
            raise FileNotFoundError(f"Config file not found: {config_path}")  
    
    def _send_message(self, channel_name, message):  
        
        try:  
            
            channel=self.config['channels'].get(channel_name)
            if not channel:  
                raise ValueError(f"Channel '{channel_name}' not found in config")  
            
            response = self._client.chat_postMessage(  
                channel=channel,  
                text=message  
            )  
            return response  
        except SlackApiError as e:  
            print(f"Error sending message: {e.response['error']}")  
            return None  

    def _send_formatted_message(self, channel_name, message, emoji=":robot_face:"):  
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        formatted_message = f"{emoji} *Bot Message* ({timestamp})\n{message}"  
        return self._send_message(channel_name, formatted_message)  

    def _send_block_message(self, channel_name, header, content, footer=""):  
        blocks = [  
            {  
                "type": "header",  
                "text": {  
                    "type": "plain_text",  
                    "text": header  
                }  
            },  
            {  
                "type": "section",  
                "text": {  
                    "type": "mrkdwn",  
                    "text": content  
                }  
            }  
        ]  

        if footer:  
            blocks.append({  
                "type": "context",  
                "elements": [  
                    {  
                        "type": "mrkdwn",  
                        "text": footer  
                    }  
                ]  
            })  

        try:

            channel=self.config['channels'].get(channel_name)
            if not channel:  
                raise ValueError(f"Channel '{channel_name}' not found in config")  

            response = self._client.chat_postMessage(  
                channel=channel,  
                blocks=blocks  
            )  
            return response  
        except SlackApiError as e:  
            print(f"Error sending message: {e.response['error']}")  
            return None  


    def _invite_bot_to_channel(self, channel_name):  
        try:  
            # Get your bot's user ID first  
            bot_info = self._client.auth_test() 
            bot_user_id = bot_info["user_id"]  

            channel=self.config['channels'].get(channel_name)
            if not channel:  
                raise ValueError(f"Channel '{channel_name}' not found in config")  
            
            # Invite the bot to the channel  
            result = self._client.conversations_invite(  
                channel=channel,  
                users=[bot_user_id]  
            )  
            print(f"Bot successfully invited to channel: {result['channel']['name']}")  
        except SlackApiError as e:  
            print(f"Error inviting bot: {e.response['error']}")

    def send_dm(self, user_name, message, emoji=":robot_face:", email = None):  
        """Send a direct message to a user using their name from config or email"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        formatted_message = f"{emoji} *Bot Message* ({timestamp})\n{message}"  

        try:  
            if email:
                user_id = self._get_user_id(email)

                if not user_id:  
                    raise ValueError(f"User mail: '{email}' doesn't have an associated Slack ID. Are you in the SimsLab group?")
                
                # This will create a DM channel if it doesn't exist  
                response = self._client.chat_postMessage(  
                    channel=user_id,  # You can directly use the user ID here  
                    text=formatted_message  
                )
            
            else:
                user_id = self.config['users'].get(user_name.lower())  
                if not user_id:  
                    raise ValueError(f"User '{user_name}' not found in config. Try email argument (Columbia email used for Slack Sign-up)")


                # This will create a DM channel if it doesn't exist  
                response = self._client.chat_postMessage(  
                    channel=user_id,  # You can directly use the user ID here  
                    text=formatted_message  
                )  
                print(f"DM sent to {user_name}: {datetime.fromtimestamp(float(response['ts'])).strftime('%Y-%m-%d %H:%M:%S')}")  
        except SlackApiError as e:  
            print(f"Error sending DM: {e.response['error']}")  

    def _get_user_id(self, email):  
        """Get user ID from email address"""  
        try:  
            response = self._client.users_lookupByEmail(email=email)  
            return response['user']['id']  
        except SlackApiError as e:  
            print(f"Error looking up user: {e.response['error']}")  
            return None

    def _get_channel_id(self, channel_name):  
        try:  
            cursor = None # is None by default by it's just for explainability. This way, we start with "page 1" of all list of channels
            while True:  
                result = self._client.conversations_list(cursor=cursor)
                for channel in result['channels']:  
                    if channel['name'] == channel_name:  
                        return channel['id']  
                cursor = result.get('response_metadata', {}).get('next_cursor') # whenever 'next_cursor' is empty, means we are in the last channels' page
                if not cursor:  
                    break  
            return None  
        except SlackApiError as e:  
            print(f"Error listing conversations: {e.response['error']}")  
            return None  

# Usage example  
# if __name__ == "__main__":
#     bot = EnhancedSlackBot(SLACK_TOKEN)  

#     # Simple message  
#     bot.send_message("#general", "Hello from Python Bot! 🐍")  

#     # Formatted message with timestamp  
#     bot.send_formatted_message("#general", "This is a formatted message!")  

#     # Block message with header and footer  
#     bot.send_block_message(  
#         "#general",  
#         "Important Announcement",  
#         "This is the main content of the message.\nIt can contain multiple lines!",  
#         "Sent by Python Bot"  
#     )  