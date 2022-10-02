import os
import sys
import json
import time
import threading

import smtplib
from email.mime.text import MIMEText

import pyupbit

def check_order(order_list : list):
    count = 0
    while order_list:
        time.sleep(10)
        count += 1

        if count >= 360:
            return False
    return True

if __name__ == "__main__":
    config = json.loads("config.json")

    upbit = pyupbit.Upbit(config["access_key"], config["secret_key"])

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(config["send_mail_address"], config["send_mail_password"])

    signature = "\n\n [코인 매수 봇에서 보낸 메일입니다.]"

    order_amount = 6000 # unit: KRW

    ticker_list = ["KRW-BTC", "KRW-ETH"]

    if upbit.get_balance("KRW") < order_amount * 1.5:
        mail_contents = "코인 매수 봇 알림! \n - 주문에 필요한 원화가 부족합니다. 원화를 입금 해주세요!"
        msg = MIMEText(mail_contents + signature)
        msg['Subject'] =  "[코인 매수 봇] 알림! 원화 입금이 필요합니다!"
        session.sendmail(config["send_mail_address"], config["send_mail_password"], msg.as_string())
    else:
        order_contents = "아래와 같이 주문했습니다! \n\n [주문 내역] \n"
        for ticker in ticker_list:
            order = upbit.buy_market_order(ticker, order_amount)
            order_contents += ticker \
                            + "\n - 주문 가격 (KRW): " + str(order["price"]) \
                            + "\n - 수수료 (KRW): " + str(order["reserved_fee"]) \
                            + "\n - 총 비용 (KRW): " + str(order["locked"]) \
                            + "\n\n"
        
        order_msg = MIMEText(order_contents + signature)
        order_msg['Subject'] =  "[코인 매수 봇] 자동 매수 주문을 완료했습니다!"
        session.sendmail(config["send_mail_address"], config["send_mail_password"], order_msg.as_string())
        
        # 체결 여부 확인
        result_contents = "아래와 같이 체결됐습니다! \n\n [체결 내역] \n"
        failed_list = []
        for ticker in ticker_list:
            if check_order(upbit.get_order(ticker)):
                result = upbit.get_order(ticker, state="done")[0]
                result_contents += ticker \
                            + "\n - 체결 시점 시장가 (KRW): " + str(result["price"]) \
                            + "\n - 체결된 양 (KRW): " + str(result["volume"]) \
                            + "\n - 수수료 (KRW): " + str(result["paid_fee"]) \
                            + "\n\n"
            else:
                failed_list.append(ticker)
                result_contents += ticker \
                            + "\n - 체결에 실패했습니다! 업비트 홈페이지에서 거래 내역을 확인해주세요!" \
                            + "\n\n"

        result_msg = MIMEText(result_contents + signature)

        if failed_list:
            result_msg['Subject'] =  "[코인 매수 봇] 일부 주문만 체결됐습니다!"
        else:
            result_msg['Subject'] =  "[코인 매수 봇] 모든 주문이 체결됐습니다!"

        session.sendmail(config["send_mail_address"], config["send_mail_password"], result_msg.as_string())
    
    session.quit()

