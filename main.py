from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os

AMAZON_URL = 'https://www.amazon.it/bimar-B301-Prontoforno-Elettronico-preimpostati/dp/B09JZQ4D38/?th=1'
TARGET_PRICE = 250.00
email_host = os.environ.get('email_host')
email_port = int(os.environ.get('email_port'))
email_sender = os.environ.get('email_sender')
password_sender = os.environ.get('email_password')
email_recipient = os.environ.get('email_recipient')


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9'
}
response = requests.get(AMAZON_URL, headers=headers)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'lxml')

price_tag = soup.select_one("span.a-offscreen")
price_decimal = float(price_tag.getText().split('€')[0].replace(',', '.'))
if price_decimal < TARGET_PRICE:
    with smtplib.SMTP(email_host, port=email_port) as connection:
        connection.starttls()
        connection.login(user=email_sender, password=password_sender)
        connection.sendmail(from_addr=email_sender, to_addrs=email_recipient, msg=f"Subject: The price is now under target \n\nThe price is now just {price_decimal} euro for the item {AMAZON_URL}")













