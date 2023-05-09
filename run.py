import logging
import math
import os
import time
from random import randint

import cv2
import pytumblr
from cohost.models.block import AttachmentBlock as CohostAttachmentBlock
from cohost.models.user import User as CohostUser
from mastodon import Mastodon
from twitter import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("randochrontendo.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


VIDEOS_DIRECTORY = os.environ.get("VIDEOS_DIR")

TWITTER_CREDENTIALS = {
    "token": os.environ.get("TWITTER_ACCESS_TOKEN_KEY"),
    "token_secret": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    "consumer_key": os.environ.get("TWITTER_CONSUMER_KEY"),
    "consumer_secret": os.environ.get("TWITTER_CONSUMER_SECRET"),
}
COHOST_CREDENTIALS = {
    "email": os.environ.get("COHOST_EMAIL"),
    "password": os.environ.get("COHOST_PASSWORD"),
}
MASTODON_CREDENTIALS = {
    "access_token": os.environ.get("MASTODON_ACCESS_TOKEN"),
    "api_base_url": os.environ.get("MASTODON_API_BASE_URL"),
}
TUMBLR_CREDENTIALS = {
    "consumer_key": os.environ.get("TUMBLR_CONSUMER_KEY"),
    "consumer_secret": os.environ.get("TUMBLR_CONSUMER_SECRET"),
    "oauth_token": os.environ.get("TUMBLR_OAUTH_TOKEN"),
    "oauth_secret": os.environ.get("TUMBLR_OAUTH_SECRET"),
}


def run():
    post = RandoChrontendoPost()

    try:
        post_twitter(post)
    except Exception as e:
        logger.error(f"Twitter post failed: {e}")

    try:
        post_cohost(post)
    except Exception as e:
        logger.error(f"Cohost post failed: {e}")

    try:
        post_tumblr(post)
    except Exception as e:
        logger.error(f"Tumblr post failed: {e}")

    try:
        post_mastodon(post)
    except Exception as e:
        logger.error(f"Mastodon post failed: {e}")


def post_twitter(post):
    twitter_upload = Twitter(
        domain="upload.twitter.com", auth=OAuth(**TWITTER_CREDENTIALS)
    )
    with open("image.jpg", "rb") as image_data:
        media_id = twitter_upload.media.upload(media=image_data.read())[
            "media_id_string"
        ]
    twitter_upload.media.metadata.create(
        _json={"media_id": media_id, "alt_text": {"text": post.get_alt_text()}}
    )
    twitter = Twitter(auth=OAuth(**TWITTER_CREDENTIALS))
    twitter.statuses.update(media_ids=media_id)


def post_cohost(post):
    user = CohostUser.login(**COHOST_CREDENTIALS)
    project = user.getProject("randochrontendo")

    blocks = [CohostAttachmentBlock("image.jpg", alt_text=post.get_alt_text())]
    project.post("", blocks)


def post_mastodon(post):
    mastodon = Mastodon(**MASTODON_CREDENTIALS)
    media = mastodon.media_post("image.jpg", description=post.get_alt_text())
    timeout = 1
    while media["url"] is None:
        time.sleep(timeout)
        media = mastodon.media(media)
        timeout *= 2
    mastodon.status_post("", media_ids=[media["id"]])


def post_tumblr(post):
    client = pytumblr.TumblrRestClient(**TUMBLR_CREDENTIALS)
    client.create_photo(
        "randochrontendo.tumblr.com", data="image.jpg", caption=post.get_alt_text()
    )


class RandoChrontendoPost:
    def __init__(self):
        self._get_video_file()
        self._write_image()

    def get_alt_text(self):
        return f"{self.video_name} ({self.timestamp})"

    def _get_video_file(self):
        video_files = os.listdir(VIDEOS_DIRECTORY)
        file_to_grab = randint(0, len(video_files) - 1)
        self.file_name = video_files[file_to_grab]
        self.video_name = (self.file_name.split(".")[0]).strip()

    def _write_image(self):
        video = cv2.VideoCapture("{}/{}".format(VIDEOS_DIRECTORY, self.file_name))
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        count_non_zero = 0
        while count_non_zero <= 2500:
            frame_to_grab = randint(1, total_frames)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_to_grab)
            _, curframe = video.read()
            cv2.imwrite("image.jpg", curframe)
            img = cv2.imread("image.jpg", 0)
            count_non_zero = cv2.countNonZero(img)

        self._get_timestamp(video.get(cv2.CAP_PROP_POS_MSEC))

        video.release()
        cv2.destroyAllWindows()

    def _get_timestamp(self, milliseconds):
        seconds = math.floor((milliseconds / 1000) % 60)
        minutes = math.floor((milliseconds / (1000 * 60)) % 60)
        hours = math.floor((milliseconds / (1000 * 60 * 60)) % 24)
        self.timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"


if __name__ == "__main__":
    run()
