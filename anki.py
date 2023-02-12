import json
import urllib.request
import crawler.english_cambridge as cambridge
import platform
import datetime
from openAI import keyToImage

if platform.system() == 'Windows':
    DOWNLOAD_DIR = 'C:/Users/tang/AppData/Roaming/Anki2/使用者 1/collection.media/'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def addCards(word, deckName='英文單字'):
    today = str(datetime.date.today())
    deckName = f"{deckName}::{today}"
    invoke('createDeck', deck=deckName) #新增牌組
    try:# 使用 try，測試內容是否正確
        result, sentencesList = cambridge.LookUp(word, DOWNLOAD_DIR)
        print("sentencesList :" + sentencesList[0])
        en_note_template = {
            "deckName": deckName,
            "modelName": "myCard",
            'fields': result,
            "picture": [{
                "url": keyToImage(sentencesList[0]),
                "filename": f"{word}.png",
                "fields": [
                    "圖片"
                ]
            }]
        }
        result = invoke('addNote',**{ "note": en_note_template })
        print('got list of decks: {}'.format(result))

        return True
    except:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        return False

    
    
if __name__ == '__main__':
    print(addCards('apple', deckName='英文單字'))
    
