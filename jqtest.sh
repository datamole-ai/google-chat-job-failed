
failed_list=( 'a' 'b' 'c' )
GITHUB_REF='/refs/head/branch'
GITHUB_SERVER_URL='https://github.com/'
GITHUB_REPOSITORY='datamole-ai/testrepo'
GITHUB_RUN_ID='100'


echo $GITHUB_LINK
failed_list=$(echo ${failed_list[@]} | sed -e 's/ /<br>/g')

GITHUB_LINK=$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID
HEAD=$(echo ${GITHUB_REF##*/})
REPO_NAME=$(echo ${GITHUB_REPOSITORY#*/})



text="<b>$failed_list</b><br><br>branch: <b>$HEAD</b>"




jq -n \
      --arg fl "$failed_list" \
      --arg txt "$text" \
      --arg repo "repo: $REPO_NAME" \
      --arg gl "$GITHUB_LINK"\
      --arg ref "on branch $HEAD" \
      '{"cards":[{"header":{"title":"<b>JOBS_FAILED</b>","subtitle":$repo},"sections":[{"widgets":[{"buttons":[{"textButton":{"text":"VIEW_RUN","onClick":{"openLink":{"url":$gl}}}}]},{"textParagraph":{"text":$txt}}]}]}]}'



# { "cards": [ { "header": { "title": "<b>JOBS FAILED</b>", "subtitle": $repo }, "sections": [ { "widgets": [ { "textParagraph": { "text": $txt } }, "button": { "textButton": {"text": "VIEW RUN", "onClick": {"openLink": {"url": $gl }}}}]}]}] }
