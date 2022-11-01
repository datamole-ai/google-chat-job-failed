import os
import urllib3
import json

needs_context = json.loads(os.getenv('NEEDS_CONTEXT'))
google_chat_webhook = os.getenv('GOOGLE_CHAT_WEBHOOK')
initiator = os.getenv('INITIATOR')
github_link = os.getenv('GITHUB_LINK')
head = os.getenv('HEAD')
repo_name = os.getenv('REPO_NAME')

print(needs_context)
print(google_chat_webhook)
print(github_link)
print(head)
print(repo_name)

# List to store failed jobs
failed_list = []

# Add failed jobs to list if job's result is failure
print(type(needs_context))
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

TEXT_DICT = ''
init_by = ''
no_initiator = {"cards": [{"header": {"title": "<b>JOBS FAILED</b>", "subtitle": head}, "sections": [{"widgets": [{"textParagraph": {"text": TEXT}}, {"buttons": [{"textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": github_link}}}}]}]}]}]}
is_initiator = {"cards": [{"header": {"title": "<b>JOBS FAILED</b>", "subtitle": head}, "sections": [{"widgets": [{"textParagraph": {"text": init_by}}, {"textParagraph": {"text": TEXT}}, {"buttons": [{"textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": github_link}}}}]}]}]}]}

if initiator != '':
    init_by = 'Initiated by: <b>' + initiator + '<b>'
    TEXT_DICT = is_initiator
else:
    TEXT_DICT = no_initiator

print(json.dumps(TEXT_DICT))

http = urllib3.PoolManager()
r = http.request(
    'POST',
    google_chat_webhook,
    headers={'Content-Type': 'application/json'},
    body=json.dumps(TEXT_DICT)
)
print(r.data)
