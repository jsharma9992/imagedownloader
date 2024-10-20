import streamlit as st
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from icrawler.builtin import GoogleImageCrawler


def download_images(query, num_images):
    crawler = GoogleImageCrawler(storage={"root_dir": "downloads"})
    
   
    try:
        crawler.crawl(keyword=query, max_num=num_images)
        st.success(f"Downloaded {num_images} images of '{query}'!")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def create_zip(directory):
    zip_filename = "downloads.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_file.write(file_path, os.path.relpath(file_path, directory))
    return zip_filename


def send_email(recipient_email, filename):
    sender_email = "spajjoint@gmail.com"  
    sender_password = "jmkuonvikubvjdtx"   

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Downloaded Images"

    with open(filename, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            st.success(f"Email sent to {recipient_email} with the images attached.")
    except Exception as err:
        st.error(f"Failed to send email: {err}")

# Main Streamlit app
def run_app():
    st.title("Image Downloader and Email Sender")

    search_query = st.text_input("Enter the name or topic of the images you want:")
    num_images = st.number_input("Enter the number of images to download:", min_value=1, value=5)
    recipient_email = st.text_input("Enter your email address:")

    if st.button("Download and Send Images"):
        if search_query and recipient_email:
            download_images(search_query, num_images)
            zip_filename = create_zip("downloads")
            send_email(recipient_email, zip_filename)
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    run_app()
