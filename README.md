# transo
A Simple twitter bot to translate tweet from English to any language supported by Google Translate.

## Usage
Just retweet a tweet with @appwithtech translate to language e.g. @appwithtech translate to French

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
