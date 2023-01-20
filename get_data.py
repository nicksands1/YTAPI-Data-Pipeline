import requests
from googleapiclient.discovery import build
import pandas as pd
import time
import boto3
import io

channel_id = 'your_channel_id'
api_key = 'your_api_key'

api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client.build(
youtube = build(api_service_name, api_version, developerKey=api_key)


def get_channel_stats(youtube, channel_id):

    all_data = []
    request = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    )
    response = request.execute()

    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'totalViews': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                }
        all_data.append(data)
    return pd.DataFrame(all_data)
channel_stats = get_channel_stats(youtube, channel_id)
print('Channel data collected...')

playlist_id = 'UULXzq85ijg2LwJWFrz4pkmw'

def get_vids(youtube, playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    
    while next_page_token is None:
        request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50,
                pageToken = next_page_token)
        response = request.execute()
    
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')

    return video_ids
video_ids = get_vids(youtube, playlist_id)
print('Video IDs collected...')



def get_video_details(youtube, video_ids): 
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['title', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)


        #print(all_video_data)
        return pd.DataFrame(all_video_info)
        print(all_video_data)
video_df = get_video_details(youtube, video_ids)
video_df.to_csv('youtube_data.csv')

bucket = 'nasdata-project' # already created on S3
csv_buffer = io.StringIO()
video_df.to_csv(csv_buffer)

s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, 'youtube_data.csv').put(Body=csv_buffer.getvalue())
print('CSV file created')
