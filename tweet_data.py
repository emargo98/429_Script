import tweepy as tw
import json
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil.parser import parse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import final_project_credentials
import numpy as np
from collections import defaultdict

# All credentials
chart_studio.tools.set_credentials_file(username='maliikthegreat',
										api_key=final_project_credentials.chart_studio_api_key)

consumer_key = final_project_credentials.consumer_key
consumer_secret = final_project_credentials.consumer_secret
access_token = final_project_credentials.access_token
access_token_secret = final_project_credentials.access_token_secret

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
analyser = SentimentIntensityAnalyzer()

# Initializing Twitter API
api = tw.API(auth, wait_on_rate_limit=True)

# Twitter username list of Top 10 Football players
user_list = ['@DangeRussWilson', '@JJWatt', '@TimTebow', '@AaronRodgers12', '@ochocinco',
             '@DezBryant', '@drewbrees', '@ReggieBush', '@MichaelVick', '@RobGronkowski']

colors = {1: 'green', 2: 'yellow', 3: 'blue', 4: 'purple', 5: 'orange',
          6: 'turquoise', 7: 'red', 8: 'pink', 9: 'gold', 10: 'lavender'}
# pol_file = json.load(open('nfl-tweet-polarities.json'))
trace_list = []
avg_trace_list = []
max_tweets = 150
pol_dict = defaultdict(dict)
ovr_pol = []
avg_pol_list = []
for user in user_list:
	user_x_axis = []
	user_y_axis = []
	color_counter = 1
	color = colors[color_counter]
	pos_pol = []
	neu_pol = []
	neg_pol = []
	pol_list = []
	# Grabs Tweets, and finds sentiment scores
	for tweet in tw.Cursor(api.search, q=user).items(max_tweets):
		tweet_obj = tweet._json
		if user in tweet_obj['text']:
			pol_score = analyser.polarity_scores(tweet_obj['text'])
			pol_score = pol_score['compound']
			date = parse(tweet_obj['created_at'])
			user_x_axis.append(date)
			user_y_axis.append(pol_score)
			if pol_score >= .05:
				pos_pol.append(pol_score)
			elif pol_score <= -.05:
				neg_pol.append(pol_score)
			else:
				neu_pol.append(pol_score)
	pol_dict[user]['Polarity Scores'] = defaultdict(dict)
	pol_dict[user]['Polarity Scores'] = defaultdict(dict)
	pol_dict[user]['Polarity Scores'] = defaultdict(dict)
	pol_dict[user]['Polarity Scores']['Positive'] = pos_pol
	pol_dict[user]['Polarity Scores']['Negative'] = neg_pol
	pol_dict[user]['Polarity Scores']['Neutral'] = neu_pol
	avg_user_score = np.mean(user_y_axis)
	pol_dict[user]['Average Score'] = avg_user_score
	avg_pol_list.append(avg_user_score)
	trace = go.Scatter(x=user_x_axis, y=user_y_axis, mode='markers', name=user, fillcolor=color, text=user)
	trace_list.append(trace)
	color_counter += 1

# pol_file = json.load(open('nfl-tweet-polarities.json'))
with open('nfl-tweet-polarities.json', 'w') as outfile:
	json.dump(pol_dict, outfile, indent=2)

# Labels chart
layout = go.Layout(
	title='Fan-Athlete Sentiment Scores',
	xaxis=dict(
		title='Datetime'),
	yaxis=dict(title='Sentiment Compound Score (Between -1 & 1)'),
	showlegend=True
)

# Makes chart
fig = go.Figure(data=trace_list, layout=layout)
fig.show()

