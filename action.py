import os
import urllib3
import json

needs_context = json.loads(os.getenv('NEEDS_CONTEXT'))
google_chat_webhook = os.getenv('GOOGLE_CHAT_WEBHOOK')
github_link = os.getenv('GITHUB_LINK')
head = os.getenv('HEAD')
repo_name = os.getenv('REPO_NAME')

failed_list = []

print(type(needs_context))
for job_name in needs_context:
    job = needs_context.get(job_name)
    if job.get('result') == 'failure':
        failed_list.append(job_name)

if len(failed_list) == 0:
    exit(0)
else:
    text = 'Failed jobs: <br><b>' + '<br>'.join(map(str, failed_list)) + '</b>'
    # title = "<b>JOBS FAILED</b>"

text_dict = {"cards": [{"header": {"title": "<b>JOBS FAILED</b>", "subtitle": head}, "sections": [{"widgets": [{"textParagraph": {"text": text}}, {"buttons": [{"textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": github_link}}}}]}]}]}]}
# message = json.dumps(text_string).encode('utf-8')
print(json.dumps(text_dict).encode('utf-8'))

http = urllib3.PoolManager()
r = http.request(
    'POST',
    google_chat_webhook,
    headers={'Content-Type': 'application/json'},
    body=json.dumps(text_dict).encode('utf-8')
  )

print(r.data)
