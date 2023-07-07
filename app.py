from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
os.environ['PYTHONUNBUFFERED'] = '1'

@app.route('/contact', methods=['POST'])
def contact():

    name = request.form.get('name') or request.get_data() or request.get_data(as_text=True) or request.json
    email = request.form.get('mail') or request.get_data() or request.get_data(as_text=True) or request.json
    message = request.form.get('message') or request.get_data() or request.get_data(as_text=True) or request.json
    subject = request.form.get('subject') or request.get_data() or request.get_data(as_text=True) or request.json

    with open('smtp_config.txt', 'r') as f:
        smtp_config = f.read().splitlines()
    sender_email = smtp_config[0]
    sender_host = smtp_config[1]
    sender_port = smtp_config[2]
    sender_name = smtp_config[3]
    receiver_email = email

    print(f'Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}')

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
        print(e)
        return jsonify({'status': 'error', 'message': f'Error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
