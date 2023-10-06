from flask import Flask, request, jsonify, json
from flask_cors import CORS
import logging
import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.DEBUG)

CORS(app, origins=[
      "https://test.easyfoods.com",
      "https://www.easyfoods.com",
      "https://easyfoods.com"
    ])

def verify_captcha(token, recaptcha_secret_key):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': recaptcha_secret_key,
        'response': token,
        'remoteip': request.remote_addr,
    }
    response = requests.post(url, data=payload)
    result = response.json()
    logging.info(result)
    return result.get('success', False)


@app.route('/contact', methods=['POST'])
def contact():
    json_data = request.get_json()
    try:
        reason = int(json_data['reason'])
    except Exception as e:
        logging.warning(e)
        reason = 0
    name = json_data['name']
    email = json_data['email']
    message = json_data['message']
    subject = json_data['subject']
    gctoken = json_data['g-recaptcha-response']
              
    # Load config
    with open('smtp_config.txt', 'r') as f:
        smtp_config = f.read().splitlines()
    sender_email = smtp_config[0]
    sender_host = smtp_config[1]
    sender_port = smtp_config[2]
    sender_name = smtp_config[3]
    try:
        receiver_email_list = smtp_config[4].split('|')
    except Exception as e:
        logging.warning(e)
        receiver_email_list[0] = smtp_config[4]
    receiver_email = receiver_email_list[reason]
    recaptcha_key = smtp_config[5]

    logging.warning(f'To: {receiver_email}')

    # first, check recaptcha
    captcha_valid = verify_captcha(gctoken, recaptcha_key)
    if not captcha_valid:
        return jsonify({'status': 'error', 'message': 'Captcha failed'}), 500

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'{sender_name} - New Contact from Website'

    text_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
    html_body = f'''\
        <hr>
        <p
            style="margin: 0; font-size: 14px; text-align: left;">
            <strong>Name:</strong> {name}</p>
        <p
            style="margin: 0; font-size: 14px; text-align: left;">
            <strong>Subject:</strong> {subject}</p>
        <p
            style="margin: 0; font-size: 14px; text-align: left;">
            <strong>Email:</strong> {email}</p>
            <hr>
        <p
            style="margin: 0; font-size: 14px; text-align: left;">
            <strong>Message:</strong><br><br>{message}</p>
    '''
      
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP(sender_host, int(sender_port))
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return jsonify({'status': 'sent', 'message': 'Success'}), 200
    except Exception as e:
        logging.warning(e)
        return jsonify({'status': 'error', 'message': f'Error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
