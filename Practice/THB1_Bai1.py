import facebook
import pandas as pd
import json
from datetime import datetime
import os


class FacebookCollector:
    def __init__(self, access_token):
        """
        Initializes the FacebookCollector instance with the provided access token.
        """
        try:
            self.access_token = access_token
            self.graph = facebook.GraphAPI(access_token)
            print("FacebookCollector initialized successfully.")
        except Exception as e:
            print(f"Initialization error: {e}")

    def check_token_validity(self):
        """
        Checks whether the access token is valid.
        """
        try:
            me = self.graph.get_object('me', fields='id,name')
            print(f"Token is valid. User: {me.get('name')}, ID: {me.get('id')}")
            return True
        except Exception as e:
            print(f"Invalid token: {e}")
            return False

    def collect_data(self, limit=10):
        """
        Collects posts from the user's Facebook feed up to the specified limit.
        """
        try:
            posts = self.graph.get_object(
                "me/feed",
                fields="id,message,created_time,comments.limit(100),reactions.limit(100),shares,type",
                limit=limit
            )
            print("Posts collected successfully:")
            for post in posts.get('data', []):
                print(f"Id: {post.get('id')}")
                print(f"Message: {post.get('message')}")
                print(f"Created Time: {post.get('created_time')}")
                print(f"Comments: {post.get('comments')}")
                print(f"Reactions: {post.get('reactions')}")
                print(f"Shares: {post.get('shares')}")
                print(f"Type: {post.get('type')}")
                print('______________________')
            return posts
        except Exception as e:
            print(f"Error in collect_data: {e}")
            return None

    def json_to_excel(self, my_json, excel_file=None, output_dir=None):
        """
        Converts JSON data to an Excel file and saves it to the specified directory.
        """
        try:
            # Prepare data for DataFrame
            posts = []
            for post in my_json.get('data', []):
                post_data = {
                    'id': post.get('id', ''),
                    'message': post.get('message', ''),
                    'created_time': post.get('created_time', '')
                }
                posts.append(post_data)

            # Create DataFrame
            df = pd.DataFrame(posts)
            if 'created_time' in df.columns:
                df['created_time'] = pd.to_datetime(df['created_time']).dt.strftime('%Y-%m-%d %H:%M:%S')

            # Set file name and directory
            if not excel_file:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                excel_file = 'FacebookPost.xlsx'
            
            # Define the output path
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                excel_file = os.path.join(output_dir, excel_file)

            # Export to Excel
            df.to_excel(excel_file, index=False)
            print(f"Data saved to {excel_file}")
            return excel_file
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None
def main():
    ACCESS_TOKEN = 'EAAIJ42vdvZAcBOz2YBrP8C53PRxpox8P9L2PMQZCZCb0FdnpwOaU5ZCyNDsG1WXalLsVP0HKDS3RQy6lUTwxWxIG3iMIqy7EYu3oSE1M5wkhCSXr7WqptNRTc7SFcTLRLaFlRoTnIfwiQcCPva3dupZCHz8sbNYsZALAjXPseSxATRVZBLPSgq5f64kFYpjZBcZCfVzGAF3Cl8HLZCzrgVQQZDZD'
    output_dir = "C:/Users/tanthanh/Desktop/SocialNetwork"

    collector = FacebookCollector(ACCESS_TOKEN)

    # Check if the token is valid
    if collector.check_token_validity():
        # Collect data
        posts = collector.collect_data()

        # Save collected data to an Excel file
        if posts:
            collector.json_to_excel(posts, output_dir=output_dir)

if __name__ == "__main__":
    main()