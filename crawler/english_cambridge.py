import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import ssl
import subprocess
import platform
import datetime
import json
import re

def LookUp(word, download_dir):

    # Eliminate the end of line delimiter
    word = word.splitlines()[0]
    wordUrl = urllib.parse.quote(word, safe='')
    wordUrl = wordUrl.replace('%20','-')
    wordUrl = wordUrl.replace('%27','-')
    wordUrl = wordUrl.replace('%28','-')
    wordUrl = wordUrl.replace('%29','-')
    wordUrl = wordUrl.replace('%2F','-')
    wordUrl = wordUrl.replace('--','-')
    if wordUrl[-1] == '-':
        wordUrl = wordUrl[:-1]
    
    url='https://dictionary.cambridge.org/us/dictionary/english-chinese-traditional/{}'.format(wordUrl)

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    ssl._create_default_https_context = ssl._create_unverified_context

    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    result = {}
    #example = word + '<br>'
    vocab = soup.find('span', class_ = 'hw dhw').get_text()
    phonetic = "/" + soup.find('span', class_ = 'us dpron-i').find('span',"ipa dipa lpr-2 lpl-1").get_text() + "/"
    example = ''
    enExplanation = ''
    zhExplanation = ''
    sound = ''
    sentencesList = []
    

    guideWordStyleHead_bp = '<font color = #7700b8><b>' 
    guideWordStyleTail_bp = '</b></font>'
    guideWordStyleHead = '<font color = #0085f5>' #64e82c 
    guideWordStyleTail = '</font>'
    posStyleHead = '<font color = #a4a1a6>' #ffa60d 
    posStyleTail = '</font>'
    
    soundCnt = 1
    cnt = 1

    if word == '':
        return None

    posIdiomBlocks = soup.select('div.entry-body__el')
    if len(posIdiomBlocks) == 0:
        posIdiomBlocks = soup.select('div.pr.idiom-block')

    for posBlock in posIdiomBlocks:                                                 # posBlock means the part of speech block of the word
        for pos in posBlock.select('span.pos.dpos'):
            example += "{}({}){}<br>".format(posStyleHead, pos.get_text(), posStyleTail)
            zhExplanation += "{}({}){}<br>".format(posStyleHead, pos.get_text(), posStyleTail)
            # print(pos.get_text())
        for usAudio in posBlock.select('span.us.dpron-i'):
            for source in usAudio.select('source[type="audio/mpeg"]'):
                if source is not None and bool(download_dir) != False:
                    try:
                        urllib.request.urlretrieve('https://dictionary.cambridge.org{}'.format(source['src']), '{}Py_{}_{}.mp3'.format(download_dir, word, soundCnt))
                        sound ='[sound:Py_{}_{}.mp3]'.format(word, soundCnt)
                        soundCnt = soundCnt + 1
                    except urllib.error.HTTPError as err:
                        print("HTTP Error:", err)
                    # print(source['src'])
        for guideWordBlock in posBlock.select('div.pr.dsense'):                     # There can be more than one guide word in a part of speech
            # for guideword in guideWordBlock.select('span.guideword.dsense_gw'):
            #     zhExplanation += "{}{}{}<br>".format(guideWordStyleHead_bp, guideword.get_text(), guideWordStyleTail_bp)
            #     # print(guideword.get_text())
            for meaningBlock in guideWordBlock.select('div.def-block.ddef_block'):  # A guide word can include many meanings
                for enMeaning in meaningBlock.select('div.def.ddef_d'):
                    enExplanation += "{}) {}<br>".format(cnt, enMeaning.get_text())
                    # print(enMeaning.get_text())
                for zhMeaning in meaningBlock.select('div.def-body.ddef_b > span.trans.dtrans.dtrans-se'):
                    zhExplanation += "{}{}){}{}<br>".format(guideWordStyleHead, cnt, zhMeaning.get_text(), guideWordStyleTail)
                    # print(zhMeaning.get_text())

                example += "{}) ".format(cnt)
                for theEnExample in meaningBlock.select('div.def-body.ddef_b > div.examp.dexamp > span.eg.deg'):
                    example += "{}".format(theEnExample.get_text())
                    sentencesList.append("{}".format(theEnExample.get_text()))
                    # print(theEnExample.get_text())
                    break
                example += "<br>"
                for theZhExample in meaningBlock.select('div.def-body.ddef_b > div.examp.dexamp > span.trans.dtrans.dtrans-se.hdb'):
                    example += "{}<br>".format(theZhExample.get_text())
                    # print(zhExample.get_text())
                    break
                cnt += 1
            # print('-------------------------')
        # print('●●●●●●●●●●●●●●●●●●●●●●●●●●')

    # Some meaning will reveal the 'word' in zhExplanation
    zhExplanation = zhExplanation.replace(word,'___')
    uppercase_word = word[0].upper() + word[1:len(word)]
    zhExplanation = zhExplanation.replace(uppercase_word,'___')

    example = example.replace( vocab , '<u>'+vocab+'</u>') # 粗體:'<b>'+vocab+'</b>'
    print(example)

    result['單字'] = vocab
    result['音標'] = phonetic
    result['發音(US)'] = sound
    result['例句'] = example
    result['eg解釋'] = enExplanation
    result['zh解釋'] = zhExplanation
    
    print(' ')
    print('<< {} >>'.format(word))
    print(' ')
    # print('正面', example)
    # print('背面', zhExplanation)
    return result, sentencesList



if __name__ == '__main__':
    LookUp("respondent", "./")