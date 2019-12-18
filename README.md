# transo
A Simple twitter bot to translate tweet from English to any language supported by Google Translate.

## Setup
1. Pull the Repo
2. pip install requirements.txt
3. Create a developer account on deverloper.twitter.com and your application 
   (https://docs.inboundnow.com/guide/create-twitter-application/)
4. Set the following environment variables 
   ```
   export TWITTER_CONS_KEY='Your Twitter App Consumer Key'
   export TWITTER_CONS_SECRET='Your Twitter App Consumer Secret'
   export TWITTER_ACCESS_KEY='Your Twitter App Access Key'
   export TWITTER_ACCESS_TOKEN='Your Twitter App Consumer Secret'
   ```

5. Create a GCP account and provide access to google translate
6. Download your private key and set an environment variable to point to it.
    ```
    export GOOGLE_APPLICATION_CREDENTIALS='~/.myKeys/Transo.json'
    ```

## Execution & Usage
1. Run the app in a perpetual while loop or cron or any scheduler of your choice
   ``` python transo_engine.py```

2. Go to your twitter account select a tweet, retweet it by prefixing 
   ``` 
      @appwithtech translate to <your target language>
      e.g. @appwith tech translate to French
   ```
3. If the app is running correctly, you would recieve the translated tweet as a reply.
