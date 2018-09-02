#!/usr/bin/env python
# coding: utf-8

from requests_oauthlib import OAuth1Session
import json
import slackweb
import AppConf

url = "https://api.twitter.com/1.1/trends/place.json"
# url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

headerStr = "現在のtwitterトレンドワードは、" + "\n"
trendWord = ""

# 東京
params = {"id":"1118370"}

# OAuthでget
twitter = OAuth1Session(AppConf.ConsumerKey, AppConf.ConsumerSecret, AppConf.AccessToken, AppConf.AccessTokenSecret)
req = twitter.get(url, params = params)

if req.status_code == 200:
    # レスポンスはjsonなのでparse
    trendDic = json.loads(req.text)

    # print(timeline['trends'][0])
    # trend word
    for i, trendList in enumerate(trendDic):
        # tweet_volumeでソート
        sortedVolumeList = sorted(trendList['trends'], key=lambda x: (x['tweet_volume'] is not None, x['tweet_volume']), reverse=True)

        for j, trend in enumerate(sortedVolumeList):
            print("-" + trend['name'] + "  tweet_valume:" + str(trend['tweet_volume']))
            print(trend['url'])
            # print()
            trendWord += "-" + trend['name'] + "  tweet_valume:" + str(trend['tweet_volume']) + "\n"
            trendWord += trend['url'] + "\n"
            if(j == 20): 
                break
else:
    # error
    print("Error: %d" % req.status_code)

if trendWord != "":
    postStr = headerStr + trendWord
    # slack投稿 
    slack = slackweb.Slack(url=AppConf.webhook)
    slack.notify(text=postStr)



