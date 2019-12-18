from google.cloud import translate_v2 as translate
import os,pprint,time,sys
import logging as log
import tweepy

supported_languages={'Afrikaans':'af','Albanian':'sq','Amharic':'am','Arabic':'ar',
    'Armenian':'hy','Azerbaijani':'az','Basque':'eu','Belarusian':'be',
    'Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Catalan':'ca',
    'Cebuano':'ceb (ISO-639-2)','Chinese (Simplified)':'zh-CN or zh (BCP-47)','Chinese (Traditional)':'zh-TW (BCP-47)',
    'Corsican':'co','Croatian':'hr','Czech':'cs','Danish':'da','Dutch':'nl',
    'English':'en','Esperanto':'eo','Estonian':'et','Finnish':'fi','French':'fr',
    'Frisian':'fy','Galician':'gl','Georgian':'ka','German':'de','Greek':'el',
    'Gujarati':'gu','Haitian Creole':'ht','Hausa':'ha','Hawaiian':'haw (ISO-639-2)',
    'Hebrew':'he or iw','Hindi':'hi','Hmong':'hmn (ISO-639-2)','Hungarian':'hu',
    'Icelandic':'is','Igbo':'ig','Indonesian':'id','Irish':'ga','Italian':'it',
    'Japanese':'ja','Javanese':'jv','Kannada':'kn','Kazakh':'kk','Khmer':'km',
    'Korean':'ko','Kurdish':'ku','Kyrgyz':'ky','Lao':'lo','Latin':'la',
    'Latvian':'lv','Lithuanian':'lt','Luxembourgish':'lb','Macedonian':'mk',
    'Malagasy':'mg','Malay':'ms','Malayalam':'ml','Maltese':'mt','Maori':'mi',
    'Marathi':'mr','Mongolian':'mn','Myanmar (Burmese)':'my','Nepali':'ne',
    'Norwegian':'no','Nyanja (Chichewa)':'ny','Pashto':'ps','Persian':'fa',
    'Polish':'pl','Portuguese (Portugal, Brazil)':'pt','Punjabi':'pa',
    'Romanian':'ro','Russian':'ru','Samoan':'sm','Scots Gaelic':'gd',
    'Serbian':'sr','Sesotho':'st','Shona':'sn','Sindhi':'sd',
    'Sinhala (Sinhalese)':'si','Slovak':'sk','Slovenian':'sl','Somali':'so','Spanish':'es',
    'Sundanese':'su','Swahili':'sw','Swedish':'sv','Tagalog (Filipino)':'tl',
    'Tajik':'tg','Tamil':'ta','Telugu':'te','Thai':'th','Turkish':'tr','Ukrainian':'uk',
    'Urdu':'ur','Uzbek':'uz','Vietnamese':'vi','Welsh':'cy','Xhosa':'xh',
    'Yiddish':'yi','Yoruba':'yo','Zulu':'zu'}

def translate_text(text,target_language,source_language=None):
    log.info('Begin translate_text')
    translate_client = translate.Client()
    log.debug(f'Text {text}  : Target Language :{target_language}')
    if source_language == None:
        source_language='en'
    
    # Google Translate Call
    result = translate_client.translate(text, 
                                        source_language=source_language,
                                        target_language=target_language)
    log.debug(result)
    log.info('End translate_text')
    return result


def get_twitter_api():
    log.info('Begin get_twitter_api')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(env['TWITTER_CONS_KEY'], env['TWITTER_CONS_SECRET'])
    auth.set_access_token(env['TWITTER_ACCESS_KEY'], env['TWITTER_ACCESS_TOKEN'])
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    log.info('End get_twitter_api')

    return api

def get_mentions(api,last_status_id):
    log.info('Begin get_mentions')
    mentions=[]
    latest_status_id_wrote=False
    for mention in api.mentions_timeline(last_status_id):
        mentions.append({
            'id':str(mention.id),
            'text':mention.text,
            'quoted_status_text':mention.quoted_status.text,
            'target_user_screen_name':mention.user.screen_name
        })

        # The first tweet is the latest one, so store its status
        # This will be used to query tweeter next time the bot runs
        # Mentions having id greater than the id store will be queried
        if not latest_status_id_wrote:
            with open('./last_status.txt',"w") as last_status_file:
                last_status_file.write(str(mention.id)+'\n')
            latest_status_id_wrote=True

    log.debug(mentions)
    log.info('End get_mentions')

    return mentions

def post_reply(api,mentions):
    log.info('Post Reply')
    source_language='en'

    for i in range(0,len(mentions)):
        target_language='hi'
        mention=mentions[i]
        log.debug(mention)
        text2translate=' '.join(mention['quoted_status_text'].split(' '))
        tokenizedtext=mention['text'].upper().split(' ')
        log.debug(tokenizedtext)
        
        # Find the target language in mention
        for k,v in supported_languages.items():
            if k.upper() in tokenizedtext:
                log.debug(f'{k.upper()} :{v}')
                target_language=v
                break

        #
        
        translated_text=translate_text(text2translate,target_language,source_language)
        #
        translated_text=f"@{mention['target_user_screen_name']} {translated_text['translatedText']}"
        log.debug(translated_text)
        api.update_status(translated_text,in_reply_to_status_id=mention['id'])
        time.sleep(5)

    log.info('End post_reply')


if __name__ == '__main__':
    env=os.environ
    
    # Set Logging on the screen only
    FORMAT = '[%(levelname)s]::%(asctime)-15s::%(module)s.%(funcName)s::%(lineno)d::%(message)s'
    log.basicConfig(stream=sys.stdout,level=log.DEBUG,format=FORMAT)

    #
    last_status_id=''

    # Store and Read the last status id, every time the bot is run
    # it will request mentions with status id greater than the one we store
    with open('./last_status.txt','r') as last_status:
        last_status_id=last_status.read().strip()
    log.info(f'last_status_id {last_status_id}')

    # Authenticate and Authorization from twtitter
    api=get_twitter_api()
    
    # Read mentions to get queries
    mentions=get_mentions(api,last_status_id)
    
    # Post Translated Tweet
    post_reply(api,mentions)
