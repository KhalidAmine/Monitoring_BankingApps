import pandas as pd
from google_play_scraper import app  # https://github.com/JoMingyu/google-play-scraper

## define ID's of Google play store BE banking apps we want to monitor
KBC_id = 'com.kbc.mobile.android.phone.kbc'
Belfius_id = 'be.belfius.directmobile.android'
ING_id = 'com.ing.banking'
BNPPF_id = 'com.bnpp.easybanking'

# todo make excel file  so that it can be loaded in as pandas

## download KBC Google play store data
# #todo make function that standardizes all of the below and merge in first dataframe
# KBC
KBC = pd.DataFrame([app(
    KBC_id,
    lang='en',  # defaults to 'en'
    country='be'  # defaults to 'us'
)])
# Belfius
Belfius = pd.DataFrame([app(
    Belfius_id,
    lang='en',  # defaults to 'en'
    country='be'  # defaults to 'us'
)])
# ING
ING = pd.DataFrame([app(
    ING_id,
    lang='en',  # defaults to 'en'
    country='be'  # defaults to 'us'
)])
# BNPPF
BNPPF = pd.DataFrame([app(
    BNPPF_id,
    lang='en',  # defaults to 'en'
    country='be'  # defaults to 'us'
)])

# row bind dataframes
pdList = [KBC, Belfius, ING, BNPPF]  # List of your dataframes
df = pd.concat(pdList)

# transform to dataframe #todo put it in your function from previous section
df = df[['title', 'version', 'updated', 'recentChanges', 'score',
         'ratings']]  # updated' not in right format... using web scraping to correct it

## extract updated date info using raw web scraping
from bs4 import BeautifulSoup
from urllib.request import urlopen

# todo make function of the below + see link Dorian
updated = []
# KBC
url = "https://play.google.com/store/apps/details?id=" + KBC_id
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
updated.append(str(soup.find_all("div", {"class": "xg1aie"}))[21:33])
# Belfius
url = "https://play.google.com/store/apps/details?id=" + Belfius_id
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
updated.append(str(soup.find_all("div", {"class": "xg1aie"}))[21:33])
# ING
url = "https://play.google.com/store/apps/details?id=" + ING_id
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
updated.append(str(soup.find_all("div", {"class": "xg1aie"}))[21:32])
# BNPPF
url = "https://play.google.com/store/apps/details?id=" + BNPPF_id
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
updated.append(str(soup.find_all("div", {"class": "xg1aie"}))[21:32])

# update df with the new updated app version data
df['updated'] = updated

# save final results as excel file
file = 'Output/GooglePlayStore_bankingapps.xlsx'
df.to_excel(file, index=False)

## automatic mailing regarding latest version and its patch notes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename


def send_mail(send_from: str, subject: str, text: str,
              send_to: list, files=None):
    send_to = default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype=ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(f))
        msg.attach(attachedfile)

    smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


# put in login details from app password and send out the update
username = "khalid.amine@sia-partners.com"
password = "dnfmrmbqmkmegcbl"
default_address = ["khalid.amine@sia-partners.com"]

# todo make function so that it is more generalized + make fixed parameter of send_to and files
send_mail(send_from=username,
          subject="test mail: Latest banking app updates (automated mail)",
          text="Hi subscriber, please find attached an excel file with an overview of the latest versions and updates "
               "of the Belgian banking apps.",
          send_to=["khalid.amine@sia-partners.com", "ruben.borghs@sia-partners.com"],
          files=['/Users/khalid/Desktop/BKG87/Monitoring_BankingApps/Output/GooglePlayStore_bankingapps.xlsx'])
