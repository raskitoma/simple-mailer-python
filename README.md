# RSKpyMailer: Simple-Py-Mailer

This app enables you to send email from a form.

This project assumes you have a SMTP relay server with no authentication required, so that means your relay must accept this app ip address(host) to be added as a valid sender.

This also assumes you have a valid captcha v2 key from google, paired with the sender.

Access to this app via POST request with json object as body, with the following variables:

- name
- email
- message
- subject
- g-recaptcha-response

## Usage

1. Clone this repository.
2. Modify the `smtp_config.txt` file with your SMTP configuration and details.
3. Build and run the Docker container using the following command: ```docker-compose up --build```
4. The contact API will be available at `http://localhost:3001/contact`.  This is accesible via POST request, check variables that must be send as urlencoded-form-data.
