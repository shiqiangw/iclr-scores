import openreview
import numpy as np
import pandas as pd
from tqdm import tqdm

client = openreview.Client(baseurl='https://api.openreview.net')

submissions = client.get_all_notes(invitation="ICLR.cc/2023/Conference/-/Blind_Submission", details='directReplies')

reviews = []
for submission in submissions:
    reviews = reviews + [reply for reply in submission.details["directReplies"] if reply["invitation"].endswith("Official_Review")]

scores_dict = {}
for r in reviews:
    if r['forum'] not in scores_dict:
        scores_dict[r['forum']] = []
    scores_dict[r['forum']].append(int(r['content']['recommendation'].split(':')[0]))

statistics = []
all_data = []
for s in tqdm(submissions):
    if s.forum not in scores_dict:
        continue
    title = s.content['title']
    if 'Please_choose_the_closest_area_that_your_submission_falls_into' in s.content:
        area = s.content['Please_choose_the_closest_area_that_your_submission_falls_into']
    else:
        area = ''
    scores = scores_dict[s.forum]
    avg_score = np.mean(scores)
    std_score = np.std(scores)
    all_data.append([ title, str(avg_score), str(std_score), ';'.join([str(i) for i in scores]), area])


df = pd.DataFrame(all_data, columns=['Title', 'Average Score', 'Standard Deviation', 'Individual Scores', 'Author-defined Area'])
df = df.sort_values(by=['Average Score'], ascending=False, ignore_index=True)
df.index = np.arange(1, len(df)+1)
df.to_csv('output.csv', index='True')