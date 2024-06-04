#!/usr/bin/env python
# coding: utf-8

# # Using YouTubeAPI for generating dataset and Performing EDA

# This project involves analyzing data from a YouTube channel using the YouTube Data API v3. The main objectives are to fetch channel statistics, get details of videos uploaded to the channel, preprocess the data, and perform exploratory data analysis (EDA) to uncover insights.

# ## Objectives:
# 1) Initialize the YouTube Client: Set up the YouTube Data API client to interact with YouTube data.
# 2) Fetch Channel Statistics: Retrieve general statistics about the YouTube channel, such as the number of subscribers, total views, and total videos.
# 3) Get Video Details: Extract detailed information about each video in the channel's upload playlist, including video statistics and metadata.
# 4) Data Preprocessing: Clean and transform the data to make it suitable for analysis. This includes converting data types, handling missing values, and creating new features.
# 5) Exploratory Data Analysis (EDA): Visualize and analyze the data to discover patterns and insights about the channel's performance and audience engagement.

# ## Tools and Libraries
# 1) Python: Main programming language.
# 2) Google API Client: To interact with YouTube Data API.
# 3) Pandas: For data manipulation and analysis.
# 4) Matplotlib & Seaborn: For data visualization.
# 5) WordCloud: To create word cloud visualizations.
# 6) NLTK: For natural language processing tasks like removing stop words.

# ## Importing required libraries

# In[ ]:


from googleapiclient.discovery import build
import pandas as pd
from IPython.display import JSON
from dateutil import parser
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wordcloud import WordCloud
from nltk.corpus import stopwords


# ## Set the API key and channel ID

# In[26]:


api_key = 'AIzaSyCS8I0L5_DCXYiIF7ov9V29O2lo1ZVdHto' 
channel_ids = ["UCJcCB-QYPIBcbKcBQOTwhiA"]


# ## Function to initialize YouTube client

# In[27]:


def initialize_youtube_client(api_key):
    """
    Initialize YouTube client with the given API key.
    """
    print("Initializing YouTube client...")
    return build('youtube', 'v3', developerKey=api_key)


# ## Function to get channel statistics

# In[28]:


def get_channel_stats(youtube, channel_ids):
    """
    Fetch channel statistics such as subscriber count, view count, total videos, etc.
    """
    print("Fetching channel statistics...")
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids)
    )
    response = request.execute()
    
    for item in response['items']:
        data = {
            'channelName': item['snippet']['title'],
            'subscribers': item['statistics']['subscriberCount'],
            'views': item['statistics']['viewCount'],
            'totalVideos': item['statistics']['videoCount'],
            'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)
    
    return pd.DataFrame(all_data)


# ## Function to get uploads playlist ID

# In[29]:


def get_uploads_playlist_id(youtube, channel_id):
    """
    Get the playlist ID for the uploaded videos of a channel.
    """
    print(f"Getting uploads playlist ID for channel ID {channel_id}...")
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        print(f"No items found for channel ID {channel_id}")
        return None


# ## Function to get video IDs from the uploads playlist

# In[30]:


def get_video_ids(youtube, playlist_id):
    """
    Fetch video IDs from the given playlist ID.
    """
    print(f"Fetching video IDs from playlist ID {playlist_id}...")
    video_ids = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        if next_page_token:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
        else:
            break

    return video_ids


# ## Function to get details of each video

# In[31]:


def get_video_details(youtube, video_ids):
    """
    Fetch detailed statistics for each video given a list of video IDs.
    """
    print("Fetching video details...")
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
        
        for video in response['items']:
            stats_to_keep = {
                'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                'contentDetails': ['duration', 'definition', 'caption']
            }
            video_info = {'video_id': video['id']}
            
            for part, stats in stats_to_keep.items():
                for stat in stats:
                    try:
                        if part == 'snippet' and stat == 'tags':
                            video_info[stat] = ','.join(video[part][stat])
                        else:
                            video_info[stat] = video[part][stat]
                    except KeyError:
                        video_info[stat] = None

            all_video_info.append(video_info)
            
    return pd.DataFrame(all_video_info)


# ## Function to get comments from videos

# In[32]:


def get_comments_in_videos(youtube, video_ids):
    """
    Fetch top-level comments from each video given a list of video IDs.
    """
    print("Fetching comments from videos...")
    all_comments = []
    
    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id
            )
            response = request.execute()
        
            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:10]]
            comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}
            all_comments.append(comments_in_video_info)
            
        except:
            print(f'Could not get comments for video {video_id}')
        
    return pd.DataFrame(all_comments)


# ## Fetching all the data

# In[33]:


# Initialize YouTube client
youtube = initialize_youtube_client(api_key)

# Get channel stats
channel_stats = get_channel_stats(youtube, channel_ids)
print(channel_stats)

# Get uploads playlist ID
channel_id = 'UCJcCB-QYPIBcbKcBQOTwhiA'
uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)

if uploads_playlist_id:
    # Get video IDs from the playlist
    video_ids = get_video_ids(youtube, uploads_playlist_id)
    
    # Get details of each video
    video_data_df = get_video_details(youtube, video_ids)
    print(video_data_df)


# ## Saving the data into excel file format 

# In[36]:


# Save video data to Excel file
excel_file_path = "/Users/madhumitha/Desktop/Data Science subject/youtubeapi/video_data.xlsx"
print(f"Saving video data to Excel file at '{excel_file_path}'...")
video_data_df.to_excel(excel_file_path, index=False)
print(f"Excel file saved to '{excel_file_path}'")
    
# Read the Excel file into a DataFrame
print("Reading video data from Excel file...")
read_video_data_df = pd.read_excel(excel_file_path)
read_video_data_df.head()


# ## Data Preprocessing
# 
# 1) Convert columns to appropriate data types (e.g., numeric, datetime).
# 2) Handle missing or inconsistent data.
# 3) Create new features, such as the day of the week a video was published and the duration of videos in seconds.
# 

# In[37]:


# Data Preprocessing
print("Performing data preprocessing...")
    
## Check for null values
print("Checking for null values...")
print(read_video_data_df.isnull().any())
    
## Check data types
print("Checking data types...")
print(read_video_data_df.dtypes)


# In[39]:


## Convert 'publishedAt' to datetime format
print("Converting 'publishedAt' to datetime format...")
read_video_data_df['publishedAt'] = pd.to_datetime(read_video_data_df['publishedAt'])


## Add a new column 'publishDayName' with the day name
print("Adding 'publishDayName' column...")
read_video_data_df['publishDayName'] = read_video_data_df['publishedAt'].apply(lambda x: x.strftime("%A"))

## Convert 'duration' to seconds
print("Converting 'duration' to seconds...")
read_video_data_df['durationSecs'] = pd.to_timedelta(read_video_data_df['duration']).dt.total_seconds()

## Add a column 'tagCount' to count the number of tags
print("Adding 'tagCount' column...")
read_video_data_df['tagCount'] = read_video_data_df['tags'].apply(lambda x: 0 if x is None else len(x))


read_video_data_df.head()


# ## Exploratory Data Analysis (EDA)
# 
# 1) Best and Worst Performing Videos: Identify the videos with the highest and lowest view counts.
# 2) View Distribution: Visualize the distribution of views across different videos.
# 3) Engagement Metrics: Analyze the relationship between views, likes, and comments.
# 4) Word Cloud: Generate a word cloud to visualize the most common words in video titles.
# 5) Upload Day Analysis: Determine the distribution of video uploads by day of the week.

# In[40]:


# Exploratory Data Analysis (EDA)
print("Performing Exploratory Data Analysis (EDA)...")
    
## Best performing videos
print("Plotting best performing videos...")
ax = sns.barplot(x='title', y='viewCount', data=read_video_data_df.sort_values('viewCount', ascending=False)[0:9])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K'))


# In[41]:


## Worst performing videos
print("Plotting worst performing videos...")
ax = sns.barplot(x='title', y='viewCount', data=read_video_data_df.sort_values('viewCount', ascending=True)[0:9])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K'))


# In[42]:


## View distribution per video
print("Plotting view distribution per video...")
sns.violinplot(x=read_video_data_df['channelTitle'], y=read_video_data_df['viewCount'])
plt.show()


# In[43]:


## Views vs Likes and Comments
print("Plotting views vs likes and comments...")
fig, ax = plt.subplots(1,2)
sns.scatterplot(data=read_video_data_df,x='commentCount',y='viewCount',ax=ax[0])
sns.scatterplot(data=read_video_data_df,x='likeCount',y='viewCount',ax=ax[1])
sns.histplot(data=read_video_data_df,x='durationSecs',bins=30)


# In[44]:


## Wordcloud for video titles 
stop_words = set(stopwords.words('english'))
read_video_data_df['title_no_stopwords'] = read_video_data_df['title'].apply(lambda x: [item for item in str(x).split() if item not in stop_words])

all_words = list([a for b in read_video_data_df['title_no_stopwords'].tolist() for a in b])
all_words_str = ' '.join(all_words) 
def plot_cloud(wordcloud):
    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud) 
    plt.axis("off");

wordcloud = WordCloud(width = 2000, height = 1000, random_state=1, background_color='black', 
                      colormap='viridis', collocations=False).generate(all_words_str)
plot_cloud(wordcloud)


# In[45]:


## Days of Posting the videos
day_df = pd.DataFrame(read_video_data_df['publishDayName'].value_counts())
weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_df = day_df.reindex(weekdays)
ax = day_df.reset_index().plot.bar(x='index', y='publishDayName', rot=0)


# In[ ]:




