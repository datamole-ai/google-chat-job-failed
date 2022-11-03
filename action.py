import os
import urllib3
import json


# Action input variables
needs_context = json.loads(os.getenv('NEEDS_CONTEXT'))
google_chat_webhook = os.getenv('GOOGLE_CHAT_WEBHOOK')
initiator = os.getenv('INITIATOR')
# Other environment variables
github_link = os.getenv('GITHUB_LINK')
head = os.getenv('HEAD')
repo_name = os.getenv('REPO_NAME')

# List to store failed jobs
failed_list = []

# Add failed jobs to list if job's result is failure
for job_name in needs_context:
    job = needs_context.get(job_name)
    if job.get('result') == 'failure':
        failed_list.append(job_name)

# if there's no failed jobs: exit
# otherwise build string for failed jobs
if len(failed_list) == 0:
    exit(0)
else:
    TEXT = 'Failed jobs: <br><b>' + '<br>'.join(map(str, failed_list)) + '</b>'

# Choose JSON dict if initiator has been set or not.
if initiator:
    INIT_BY = 'Initiated by: <b>' + initiator + '<b>'
    TEXT_DICT = {"cards": [{"header": {"title": "<b>JOBS FAILED</b>", "subtitle": repo_name+":"+head}, "sections": [{"widgets": [{"textParagraph": {"text": INIT_BY}}, {"textParagraph": {"text": TEXT}}, {"buttons": [{"textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": github_link}}}}]}]}]}]}
else:
    TEXT_DICT = {"cards": [{"header": {"title": "<b>JOBS FAILED</b>", "subtitle": repo_name+":"+head}, "sections": [{"widgets": [{"textParagraph": {"text": TEXT}}, {"buttons": [{"textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": github_link}}}}]}]}]}]}

# Make POST request to webhook URL
http = urllib3.PoolManager()
r = http.request(
    'POST',
    google_chat_webhook,
    headers={'Content-Type': 'application/json'},
    body=json.dumps(TEXT_DICT)
)
print(r.data)
