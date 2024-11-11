# ICLR Scores from OpenReview

A simple script to extract scores of publicly available ICLR submissions from OpenReview.

Run `pip install -r requirements.txt` for installing basic requirements.

Run `python3 main.py` to get a spreadsheet including paper titles and scores, in CSV format. The result is saved in `output.csv`, sorted according to average score.

Note:
- Withdrawn papers are excluded from the output.
- If there is any issue with pip-installing `openreview-py`, you can install it manually following Step 1 in https://docs.openreview.net/getting-started/using-the-api/installing-and-instantiating-the-python-client


**Recommendation:** Let's not overload the OpenReview server, so don't run this too often :)

