# YoutubeAPI_EDA
## Using YouTubeAPI for generating dataset and Performing EDA

This project involves analyzing data from a YouTube channel using the YouTube Data API v3. The main objectives are to fetch channel statistics, get details of videos uploaded to the channel, preprocess the data, and perform exploratory data analysis (EDA) to uncover insights.

## Objectives:
1) Initialize the YouTube Client: Set up the YouTube Data API client to interact with YouTube data.
2) Fetch Channel Statistics: Retrieve general statistics about the YouTube channel, such as the number of subscribers, total views, and total videos.
3) Get Video Details: Extract detailed information about each video in the channel's upload playlist, including video statistics and metadata.
4) Data Preprocessing: Clean and transform the data to make it suitable for analysis. This includes converting data types, handling missing values, and creating new features.
5) Exploratory Data Analysis (EDA): Visualize and analyze the data to discover patterns and insights about the channel's performance and audience engagement.

## Tools and Libraries
1) Python: Main programming language.
2) Google API Client: To interact with YouTube Data API.
3) Pandas: For data manipulation and analysis.
4) Matplotlib & Seaborn: For data visualization.
5) WordCloud: To create word cloud visualizations.
6) NLTK: For natural language processing tasks like removing stop words.

## Data Preprocessing
1) Convert columns to appropriate data types (e.g., numeric, datetime).
2) Handle missing or inconsistent data.
3) Create new features, such as the day of the week a video was published and the duration of videos in seconds.

## Exploratory Data Analysis (EDA)
1) Best and Worst Performing Videos: Identify the videos with the highest and lowest view counts.
2) View Distribution: Visualize the distribution of views across different videos.
3) Engagement Metrics: Analyze the relationship between views, likes, and comments.
4) Word Cloud: Generate a word cloud to visualize the most common words in video titles.
5) Upload Day Analysis: Determine the distribution of video uploads by day of the week.
6) Trend Analysis between view counts over time period.
7) Correlation analysis between like counts,comment counts and View counts.

## Outcomes
1) The Best performing video is Vijay Antony Sir Food Delivery | Vj Siddhu Vlogs | #shorts (6,000K views)
2) The least views video is Best Crackers testing video which got around 320k views
3) While analysing view across different videos it shows a right skew, indicating a few videos have significantly higher view counts than most.
4) Analysing relationship among likes and comments, it reveals a right skew, suggesting a small number of videos have much higher viewership than most.It suggests a strategic reason behind it (viral content).
5) Analyzing video titles with a word cloud reveals prominent the keywords that can guide content strategy for appealing as suggestion for the users. The word cloud suggests content focuses on food, parties, and celebrities.
6) The videos are most likely to be uploaded on wednesday, Monday and Friday of the week.
7) The line graph shows an upward trend in view counts over time. The y-axis shows view count, labeled from 1 million to 6 million. The x-axis shows the published date, ranging from July 2023 to May 2024. The view count clearly increases over time.
8) It suggests that there may be an inverse relationship between view count/like count and comment count, and a positive relationship between view count and like count.
9) The selected features (durationSecs, commentCount, and likeCount) seem to be relevant predictors of view count, as evidenced by the high R² values. All three models achieved reasonable performance based on the R² metric.
