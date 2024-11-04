
import os
from utils import read_json,save_json
class Youtube:
    def __init__(self, user_name, user_password):
        self.desc = {
            "desc": " ",
            "base_required_arguments": {  # base required arguments for almost all functions in this app
                "user_name (str)": "the user name of the current user",
                "user_password (str)": "the password of the current user"
            },
            "APIs": {
                "check_video_history": {
                    "desc": "check the video history of the current user",
                    "additional_required_arguments": {}, # no need for base required arguments
                    "optional_arguments": {},
                    "results_arguments": {
                        "video_history (list)": "a list of video ids of current user"
                    }
                },
                "find_video": {
                    "desc": "find a video for the current user",
                    "additional_required_arguments": {
                        "keyword (str)": "the keyword to be searched in the video list"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "search_results (str)": "the link of the video that includes the keyword"
                    }
                },
                "play_video": {
                    "desc": "play a video for the current user",
                    "additional_required_arguments": {
                        "link (str)": "the link of the video to be played"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "True if the video is played successfully, False otherwise"
                    }
                }
            }
        }
     
       
        self.user_name = user_name
        self.user_password = user_password
        if self.user_name is None or self.user_password is None:
            print(f"An error occurred: user name or password is not valid")
            return False
        else:
            # load other data from database according to user name and password
            
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "youtube_data.json")
            success,data=read_json(file_path)
            # print(json_file_path)

            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.video_history = user['video_history']
                    self.video_list = user['video_list']
                    self.video_title = user['video_title']
                    self.video_description = user['video_description']
                    print(f"User {user_name} is logged in successfully")
                return None

    def check_video_history(self):
     
        if self.video_history == []:
            print("video_history is empty")
            return None
        else:
            print("video_history is checked")
           # print(self.video_history)
            return self.video_history

    def find_video(self, keyword):
        for video in self.video_title:
            # print(video)
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "youtube_data.json")
            success, data = read_json(file_path)
            for user in data["users"]:
                # print(user)
                if user["username"] == self.user_name and user["password"] == self.user_password:
                    if keyword in user['video_title'][video]:
                        search_results = user['video_list'][video]
                        print(f"video include the keyword {keyword} is found in the video list and the link is  {search_results}")
                        return search_results

        #     if keyword in video:
        #         search_results = self.video_list[video_id]
        #         #print(search_results)
        #         print(f"video {video_id} is found in the video list at index {search_results}")
        #         return  search_results
        # print(f"video {video_id} is not found in the video list")
        
    def play_video(self, link):
        video_id = None
        for video in self.video_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "youtube_data.json")
            success,data=read_json(file_path)
            for user in data["users"]:
                # print(user)
                if user["username"] == self.user_name and user["password"] == self.user_password:
                    if link in user['video_list'][video]:
                        video_id = video
                        break
    
        if video_id in self.video_list:
            print(f"play video {video_id} and its html page is opened in browser window at  {link}")
            self.video_history.append(video_id)
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "youtube_data.json")
            success,data=read_json(file_path)
            for user in data["users"]:
                if user["username"] == self.user_name and user["password"] == self.user_password:
                    user["video_history"]=self.video_history
                    save_json(file_path,data)
            return True
        else:
            print(f"video {link} is not found in the video list")
            return False
            


if __name__ == "__main__":
    # Example usage of the YoutubeApp class
    YoutubeApp = Youtube("John", "123456")
    #YoutubeApp.check_video_history()
    YoutubeApp.find_video("code")
    YoutubeApp.play_video("https://www.youtube.com/watch?v=3")
  

