# importing required packages
import pandas as pd
from google_play_scraper import app  # https://github.com/JoMingyu/google-play-scraper
from bs4 import BeautifulSoup
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

# import ID's of Google play store banking apps we want to monitor
IDs = pd.read_excel('Input/BankingApps.xlsx')

# download Google play store data and store as pandas dataframe
df = pd.DataFrame(IDs.apply(lambda x: app(x['Google play ID'], lang='en', country='be'), axis=1).tolist())[['title',
    'version', 'updated', 'recentChanges', 'score', 'ratings']]

# extract updated date info using raw web scraping (this info is not correctly collected) and assign to df
def updated_date_scraper(id):
    """This function uses webscraping to directly collect the 'updated date' of each banking app in the
    google play store, by using its google play store id"""
    url = "https://play.google.com/store/apps/details?id=" + id
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return str(soup.find_all("div", {"class": "xg1aie"}))[21:33]

df['updated'] = IDs.apply(lambda x: updated_date_scraper(x['Google play ID']), axis=1)

# todo see link Dorian https://www.freecodecamp.org/news/if-name-main-python-example/#:~:text=We%20can%20use%20an%20if,name%20if%20it%20is%20imported

# save final results as excel file
file = '/Users/khalid/Desktop/BKG87/Monitoring_BankingApps/Output/GooglePlayStore_bankingapps.xlsx'
df.to_excel(file, index=False)

# automated mailing regarding latest version and its patch notes
def send_mail(send_from: str, subject: str, text: str,
              send_to: list, files=None):
    """This function generalizes the automatic mailing process"""
    send_to = send_to

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

# put in login details from gmail app password + recipients and send out the update
Mail_details = pd.read_excel('Input/Mail_login.xlsx')
username = Mail_details.iloc[0][0]
password = Mail_details.iloc[0][1]
send_to = Mail_details['Send to'].tolist()

# mail subject and body
subject = "test mail: Latest banking app updates (automated mail)"
text = "Hi subscriber, please find attached an excel file with an overview of the latest versions and updates of the Belgian banking apps."

# send out mails
send_mail(send_from= username,
          subject=subject,
          text= text,
          send_to= send_to,
          files=[file])
