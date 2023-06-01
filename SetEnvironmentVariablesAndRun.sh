#!/bin/sh

export MASTODON_ACCESS_TOKEN=substitute_access_token_here
export MASTODON_API_BASE_URL=https://substitute_mastodon_instance_host_here/
export VIDEOS_DIR=./Content/

python3 Source/run.py

