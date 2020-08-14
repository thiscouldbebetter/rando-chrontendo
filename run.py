import cv2
import os
from random import randint
import twitter

videos_directory = os.environ['VIDEOS_DIR']

twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
twitter_access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

video_files = os.listdir(videos_directory)
file_to_grab = randint(0, len(video_files) - 1)
file_name = video_files[file_to_grab]

vid = cv2.VideoCapture('{}/{}'.format(videos_directory, file_name))

total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
frame_to_grab = randint(200, total_frames - 200)
vid.set(cv2.CAP_PROP_POS_FRAMES, frame_to_grab)

ret, curframe = vid.read()
cv2.imwrite('image.jpg', curframe)

api = twitter.Api(
    consumer_key=twitter_consumer_key,
    consumer_secret=twitter_consumer_secret,
    access_token_key=twitter_access_token_key,
    access_token_secret=twitter_access_token_secret,
    sleep_on_rate_limit=True
)

api.PostUpdate(status='', media='image.jpg')

vid.release()
cv2.destroyAllWindows()
