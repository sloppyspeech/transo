from google.cloud import translate_v2 as translate
import os,pprint,time
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
    print('----------Begin translate_text-----------')
    translate_client = translate.Client()
    print(f'Text {text}  : Target Language :{target_language}')
    if source_language == None:
        source_language='en'
    result = translate_client.translate(text, 
                                        source_language=source_language,
                                        target_language=target_language)
    print(result)
    print('----------End translate_text-----------')
    return result


def get_twitter_api():
    print('----------Begin get_twitter_api-----------')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(env['TWITTER_CONS_KEY'], env['TWITTER_CONS_SECRET'])
    auth.set_access_token(env['TWITTER_ACCESS_KEY'], env['TWITTER_ACCESS_TOKEN'])
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    print('----------End get_twitter_api-----------')

    return api

def get_mentions(api,last_status_id):
    print('----------Begin get_mentions-----------')
    mentions=[]
    latest_status_id_wrote=False
    for mention in api.mentions_timeline(last_status_id):
        mentions.append({
            'id':str(mention.id),
            'text':mention.text,
            'quoted_status_text':mention.quoted_status.text,
            'target_user_screen_name':mention.user.screen_name
        })

        if not latest_status_id_wrote:
            with open('./last_status.txt',"w") as last_status_file:
                last_status_file.write(str(mention.id)+'\n')
            latest_status_id_wrote=True

    pprint.pprint(mentions)
    print('----------End get_mentions-----------')

    return mentions

def post_reply(api,mentions):
    print('-----------Post Reply----------')
    source_language='en'
    for i in range(0,len(mentions)):
        target_language='hi'
        mention=mentions[i]
        print(mention)
        text2translate=' '.join(mention['quoted_status_text'].split(' '))
        tokenizedtext=mention['text'].upper().split(' ')
        print(tokenizedtext)
        for k,v in supported_languages.items():
            if k.upper() in tokenizedtext:
                print(f'{k.upper()} :{v}')
                target_language=v
                break

        translated_text=translate_text(text2translate,target_language,source_language)
        translated_text=f"@{mention['target_user_screen_name']} *=Done*=>| {translated_text['translatedText']}"
        print(translated_text)
        api.update_status(translated_text,in_reply_to_status_id=mention['id'])
        time.sleep(5)
    print('----------End post_reply-----------')



if __name__ == '__main__':
    env=os.environ
    last_status_id=''

    with open('./last_status.txt','r') as last_status:
        last_status_id=last_status.read().strip()
    print(f'last_status_id {last_status_id}')

    api=get_twitter_api()
    mentions=get_mentions(api,last_status_id)
    post_reply(api,mentions)
