##tradeBot����

###�K�v�ȃ��C�u�����[�̃C���X

from coinex.coinex import CoinEx
import requests
import json
import pandas as pd
import numpy as np
import time
import datetime



##�����̌��J���Ɣ閧�����Z�b�g

public=''
SecretKey=''

coinex = CoinEx(public, SecretKey)

##���i���擾����֐�


##CET�̉��i���擾����֐�

def get_cet_price():
    
    ##URL�ɃA�N�Z�X
    
    tick=requests.get('https://api.coinex.com/v1/market/ticker?market=CETBCH')
    
    ##json�̌����悤�ɂ���
    cet_tick=json.loads(tick.text)
    data=cet_tick['data']
    ticker=data['ticker']
    cet_price=ticker['open']
        
    return cet_price




##��̊֐��ō�������X�g���f�[�^�t���[���ɂ���


cetprice_list=[]
sma5_list=[]
sma25_list=[]
signal=True
cet_amount=1



##���C�u�����[�̓Ǎ���TwitterAPI���̐ݒ�

from requests_oauthlib import OAuth1Session
import json

CK = ''                             # Consumer Key
CS = ''     # Consumer Secret
AT = '' # Access Token
AS = ''         # Accesss Token Secert


# �c�C�[�g���e�p��URL
url = "https://api.twitter.com/1.1/statuses/update.json"

# OAuth�F�؂� POST method �œ��e
twitter = OAuth1Session(CK, CS, AT, AS)





##BOT�{��

for i in range(1440):
    
    
    ##CET�̉��i���擾����
    a=get_cet_price()
    cetprice_list.append(a)
    Cet_PriceData=pd.Series(cetprice_list)
    
    
    ##5���E25���̓�̈ړ����ς��v�Z����
    sma25=Cet_PriceData.rolling(5).mean()
    sma75=Cet_PriceData.rolling(25).mean()
    
    
    
    ##�ŐV�̈ړ����ς𒊏o����
    new=len(sma25)
    new2=len(sma75)
    
    
    ##�����̏�Ԃ��m�F
    order=coinex.order_pending('CETBCH')
    
    
    
    ##���������邩�ǂ������m�F
    if order['has_next']:
        print("�������c���Ă��܂�")
    
    
    else:
        if signal:
            if sma25[new-1]<sma75[new2-1]:
                buy=coinex.order_market('CETBCH', 'buy', 0.05) ##���������̔���
                cet_amount=buy['deal_amount']
                signal=False
                d = datetime.datetime.today()
                balance=coinex.balance()
                bch=balance['BCH']
                tweet='@tos'+'\r\n'+str(d.strftime("%Y-%m-%d %H:%M:%S"))+'CET�𔃂��܂���'+str(bch['available'])
                params = {"status":tweet}
                req = twitter.post(url, params = params)
                print(d.strftime("%Y-%m-%d %H:%M:%S"),'CET�𔃂��܂���',bch['available'])
        else:
            if sma25[new-1]>sma75[new2-1]:
                coinex.order_market('CETBCH', 'sell',cet_amount)
                signal=True
                d = datetime.datetime.today()
                balance=coinex.balance()
                bch=balance['BCH']
                tweet='@tos'+'\r\n'+str(d.strftime("%Y-%m-%d %H:%M:%S"))+'CET�𔄂�܂���'+str(bch['available'])
                params = {"status":tweet}
                req = twitter.post(url, params = params)
                print(d.strftime("%Y-%m-%d %H:%M:%S"),'CET�𔄂�܂���',bch['available'])
                
        time.sleep(60)

            
            