import json
import plotly.graph_objs as go

file = json.load(open('nfl-tweet-polarities.json'))
x_axis = []
y_axis = []
pol_tup = []
# print(file['@DangeRussWilson'])
for user, values in file.items():
    x_axis.append(user)
    y_axis.append(values['Average Score'])
    pos_int = len(values['Polarity Scores']['Positive'])/150
    neu_int = len(values['Polarity Scores']['Neutral'])/150
    neg_int = len(values['Polarity Scores']['Negative'])/150
    tup = (pos_int, neu_int, neg_int)
    pol_tup.append(tup)

avg_trace = go.Bar(x=x_axis, y=y_axis, text=['% of positive interactions: {}<br>% of neutral interactons: {}<br>'
                                             '% of negative interactions: {}'.format(tup[0], tup[1], tup[2])
                                             for tup in pol_tup])

avg_layout = go.Layout(
	title='Average Sentiment Scores',
	xaxis=dict(
		title='Users'),
	yaxis=dict(title='Average Sentiment Score (Between -1 & 1)'),
	showlegend=True
)

# Makes chart
avg_fig = go.Figure(data=avg_trace, layout=avg_layout)
avg_fig.show()
file.close()
# print(pol_tup)