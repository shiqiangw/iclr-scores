import openreview
import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle

client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')

submissions = client.get_all_notes(invitation='ICLR.cc/2024/Conference/-/Submission', details='directReplies')

reviews = []
for submission in submissions:
    reviews = reviews + [reply for reply in submission.details['directReplies'] if reply['invitations'][0].endswith('Official_Review')]

scores_dict = {}
for r in reviews:
    if r['forum'] not in scores_dict:
        scores_dict[r['forum']] = []
    scores_dict[r['forum']].append(int(r['content']['rating']['value'].split(':')[0]))

statistics = []
all_data = []
for s in tqdm(submissions):
    if s.forum not in scores_dict:
        continue

    title = s.content['title']['value']

    if 'primary_area' in s.content:
        area = s.content['primary_area']['value']
    else:
        area = ''

    if 'venue' in s.content:
        decision = s.content['venue']['value']
    else:
        decision = ''
    if 'oral' in decision.lower():
        decision = 'Oral'
    elif 'spotlight' in decision.lower():
        decision = 'Spotlight'
    elif 'poster' in decision.lower():
        decision = 'Poster'
    elif 'submitted' in decision.lower() or 'rejected' in decision.lower():
        decision = 'Rejected'
    elif 'withdrawn' in decision.lower():
        decision = 'Withdrawn'

    scores = scores_dict[s.forum]
    avg_score = np.mean(scores)
    std_score = np.std(scores)
    all_data.append([ title, str(avg_score), str(std_score), ';'.join([str(i) for i in scores]), area, decision])


df = pd.DataFrame(all_data, columns=['Title', 'Average Score', 'Standard Deviation', 'Individual Scores', 'Author-defined Area', 'Decision'])
df = df.sort_values(by=['Average Score'], ascending=False, ignore_index=True)
df.index = np.arange(1, len(df)+1)
df.to_csv('output.csv', index='True')