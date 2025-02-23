import os, shutil, time, smtplib, pandas as pd, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

def rename_files(directory, prefix):
    for count, filename in enumerate(os.listdir(directory)):
        os.rename(os.path.join(directory, filename), os.path.join(directory, f"{prefix}_{count + 1}.ext"))

def clean_data(input_csv, output_csv):
    pd.read_csv(input_csv).dropna().to_csv(output_csv, index=False)

def cleanup_old_files(directory, days):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and time.time() - os.path.getatime(file_path) > days * 86400:
            os.remove(file_path)

def send_email(subject, body, recipient, sender, password):
    msg = MIMEMultipart(); msg['From'], msg['To'], msg['Subject'] = sender, recipient, subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

def backup_files(source, backup):
    for filename in os.listdir(source):
        shutil.copy(os.path.join(source, filename), backup)

def scrape_website(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    for headline in soup.find_all('h2', class_='headline'): print(headline.text)

if __name__ == "__main__":
    # Example Usage
    rename_files("path_to_directory", "file_prefix")
    clean_data("input_data.csv", "cleaned_data.csv")
    cleanup_old_files("/path/to/folder", 30)
    send_email("Weekly Report", "Body of report", "recipient@example.com", "your_email@example.com", "password")
    backup_files("/path/to/source", "/path/to/backup")
    scrape_website("https://example.com/news")
