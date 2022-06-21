# google-chat-job-failed
This sends messages to google chat when a workflow job fails.

## Usage
Place this as a job at the end of your workflow. 

Pass the jobs that you need to track to `needs:`.

The action takes 2 mandatory variables: `gchatURL` and `json`.  
Leave the json variable as is in the example. This is still a WIP.  
Add your Google Chat webhook URL to the repo's secrets and send it to the gchatURL variable.   

You can add more conditions to the `if:` after `always()`. `always()` is necessary for the job to run even if the workflow fails. 

```YAML
post-to-google-chat:
    needs: [ job1, job2, job3 ]
    if: always() 
    runs-on: ubuntu-latest
    steps:
      - name: google-chat-job-failed
        uses: datamole-ai/google-chat-job-failed@main
        with:
          gchatURL: ${{ secrets.GOOGLE_CHAT_WEBHOOK }}
          json: ${{ toJSON(needs) }}
```
