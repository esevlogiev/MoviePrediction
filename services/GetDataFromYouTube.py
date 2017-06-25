import httplib2
import os
import sys
import json
from pprint import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.


class GetDataFromYouTube:
  

  # This OAuth 2.0 access scope allows for full read/write access to the
  # authenticated user's account and requires requests to use an SSL connection.

  def __init__(self, api_key):
    YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    # This variable defines a message to display if the CLIENT_SECRETS_FILE is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0" 
    self.service = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)

  # Build a resource based on a list of properties given as key-value pairs.
  # Leave properties with empty values out of the inserted resource.

  # Remove keyword arguments that are not set
  def remove_empty_kwargs(self, **kwargs):
    good_kwargs = {}
    if kwargs is not None:
      for key, value in kwargs.items():
        if value:
          good_kwargs[key] = value
    return good_kwargs

  ### END BOILERPLATE CODE

  # Sample python code for search.list

  def search_list_by_keyword(self,  **kwargs):
    kwargs = self.remove_empty_kwargs(**kwargs) # See full sample for function
    results = self.service.search().list(
      **kwargs
    ).execute()
    if len(results['items']) == 1 and results['items'][0]['id'].get('videoId'):
      return results['items'][0]['id']['videoId']
    return None


  def videos_list_by_id(self, **kwargs):
    kwargs = self.remove_empty_kwargs(**kwargs) # See full sample for function
    results = self.service.videos().list(
      **kwargs
    ).execute()
    if len(results['items']) > 0:
      return { **results['items'][0]['statistics'], **results['items'][0]['snippet']['localized'] }
    return None


  def get_comment_threads(self, **kwargs):
    results = self.service.commentThreads().list(
      **kwargs
    ).execute()
    result_comments = []
    if len(results['items']) > 0:
      for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        if comment:
          result_comments.append({
            'text': comment['textOriginal'],
            'publishedAt': comment['publishedAt'],
            'likeCount': comment['likeCount'],
            'totalReplyCount': item['snippet']['totalReplyCount']
          }) 
      return result_comments
    return None



  def get_info_for_movie(self, name, year, date):
    name += '({0}) Offical Trailer'.format(year)
    trailer_id = self.search_list_by_keyword(
      part='snippet',
      maxResults=1,
      q=name,
      type='title',
      publishedBefore=date,
      order='viewCount'
    )
    
    if not trailer_id:
      return None
    
    video_data = self.videos_list_by_id(
      part='snippet, statistics',
      id=trailer_id
    )

    try:
      comments = self.get_comment_threads(
        part="snippet",
        videoId=trailer_id,
        textFormat="plainText",
        maxResults=100,
        order="relevance"
        )
      if video_data or comments:
        return { 'name': name, 'video_data': video_data, 'comments' : comments, 'id': trailer_id }
      return None
    
    except:
      return None 
