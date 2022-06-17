
failed_list=( 'a' 'b' 'c' )
GITHUB_REF='HEAD'
GITHUB_SERVER_URL='https://github.com/'
GITHUB_REPOSITORY='testrepo'
GITHUB_RUN_ID='100'

GITHUB_LINK=$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID
echo $GITHUB_LINK
failed_list=$(echo ${failed_list[@]} | sed -e 's/ /<br>/g')


text="Jobs *$failed_list* failed on $GITHUB_REF <br> @ <br> <$GITHUB_LINK|$GITHUB_REPOSITORY>"




jq -n \
      --arg fl "$failed_list" \
      --arg txt "$text" \
      --arg gl "$GITHUB_LINK"\
      --arg ref "$GITHUB_REF" \
      '{ "cards": [ {"header": {"title": "JOBS FAILED", "subtitle": $ref}, "sections": [ {"widgets": [{"textParagraph": {"text": $txt,onClick: {"openLink": {"url": $gl}}}}]}]}]}'





#--arg gr "$GITHUB_REPOSITORY" \
