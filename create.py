import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from crawling import channel_name

def signKeys():
    DEVELOPER_KEY = "AIzaSyC7C5ych7IJThsU4fB1cJhFWEKcmvZ4R8E"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    return youtube

def createResultFile(youtubeKey,channel_name):
    ids = []
    views=[]
    likes=[]
    dislikes=[]
    comments=[]
    mins =[]
    seconds=[]
    title=[]
    publishedAt=[]

    files = pd.read_csv(f'{channel_name}_queryList.csv')

    for idx in range(len(files)):
        request = youtubeKey.videos().list(
            part="snippet,contentDetails,statistics",
            id=files['query'][idx] # query for primiary key
        )
        response = request.execute()

        if response['items']==[]:
            ids.append("-")
            views.append("-")
            likes.append("-")
            dislikes.append("-")
            comments.append("-")
            publishedAt.append("-")

        else:
            title.append(response['items'][0]['snippet']['title'])
            views.append(response['items'][0]['statistics']['viewCount'])
            likes.append(response['items'][0]['statistics']['likeCount'])
            dislikes.append(response['items'][0]['statistics']['dislikeCount'])
            comments.append(response['items'][0]['statistics']['commentCount'])
            publishedAt.append(response['items'][0]['snippet']['publishedAt'])

    result_df=pd.DataFrame([title,views,likes,dislikes,comments,publishedAt]).T
    result_df.columns=['title','views','likes','dislikes','comments','publishedAt']

    result_df.to_csv(f"YoutubeData_{channel_name}.csv", encoding='utf-8-sig')

API_KEY = signKeys()
