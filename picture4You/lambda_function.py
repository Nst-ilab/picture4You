import http.client, urllib.parse
import json
import logging
import random
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Lineから「元気の出る画像をください」と入力されたら画像を返す。それ以外はNoneを返す。
    lineMessage = event["lineMessage"]["events"][0]["message"]["text"]
    logger.info("linemessage : " + lineMessage)
    
    res = "https://s3-ap-northeast-1.amazonaws.com/nstilab.image.storage/image/Right-kun.jpg"
#    res = "Right-kun.jpg"

    if lineMessage == "元気の出る画像をください":
        headers, result = BingImageSearch()
        
        resDict = json.loads(result)

        #取得結果からランダムに取得
        i = random.randint(0,10)

        logger.info("i : " + str(i))

#        logger.info("response from API(json) : " + json.dumps(resDict, ensure_ascii=False, indent=4) )
        
#本当はオリジナル画像を表示したかったが、ファイルサイズの制約のためか表示できないのでサムネイルを設定
        originalContentURL=resDict["value"][i]["thumbnailUrl"] + "&w=200&h=200"
#        originalContentURL=resDict["value"][i]["contentUrl"]
#        originalContentURL="https://s3-ap-northeast-1.amazonaws.com/nstilab.image.strage/image/notfound.png"
        previewImageURL=resDict["value"][i]["thumbnailUrl"] + "&w=200&h=200"
#        previewImageURL="https://s3-ap-northeast-1.amazonaws.com/nstilab.image.strage/image/notfound.png"
        

        logger.info("Original Content URL : " + originalContentURL)
        logger.info("Preview Image URL : " + previewImageURL)
    
    
        return {"originalContentURL":originalContentURL,"previewImageURL":previewImageURL}
        
    else:
        return None
        
    
# Bing image searchから画像を取得（Referenceを引用）
def BingImageSearch():

    subscriptionKey = os.environ.get('BingImageAPISubscriptionKey')

    host = os.environ.get('BingImageAPIHost')
    path = os.environ.get('BingImageAPIURL')

    termList = ["子猫","リゾート","松岡修造","犬","スイーツ","リゲイン","小熊","NRIシステムテクノ","NRI System Techno","橋本環奈","セキセイインコ","有村架純"]

    term = random.choice(termList)
    
    logger.info("term : " + term)

    "Performs a Bing image search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(term)
#クエリ条件がよくわからないのであとで直したい
    query = query + "&ImageFilters=%27Size%3ASmall%27maxFileSize%3A520192%27"
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]


    logger.info("query :" + query)
    return headers, response.read().decode("utf8")

