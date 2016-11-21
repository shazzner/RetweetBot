#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on tutorial here: http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

# The way I would imagine it would work, is it is run twice a day. It'll grab the day's tweets from the chosen accounts and retweet them
import tweepy, time, sys, string, subprocess
from apikeys import *

# Grab all the twitter accounts
argfile = str(sys.argv[1])
# Possibly grab the interval in seconds
#interval = str(sys.argv[2])
 
# Set API keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

while True:

    # This list should be all the twitter accounts we want to retweet
    filename=open(argfile,'r')
    f=filename.readlines()
    filename.close()

    # Then we go through each one and retweet each of their status updates
    for account in f:

        # Grab the twitter name and the last tweet id
        name,lastid = string.split(account,',')

        # Let's grab everything up to the lastid
        statuses = api.user_timeline(screen_name=name, since_id=lastid)

        statuses.reverse()

        for stat in statuses:
            try:
                api.retweet(stat.id)
            except:
                print "Tweet " + str(stat.id) + " already retweeted!"

            # Tweet every min
            time.sleep(60)

        try:
            newlastid = statuses[-1].id
        except:
            newlastid = lastid

        subprocess.Popen("sed -i 's/^"+name+","+str(lastid).strip()+"/"+name+","+str(newlastid).strip()+"/g' "+argfile,shell=True)
