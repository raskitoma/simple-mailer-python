# RSKpyMailer: Simple-Py-Mailer

This is an endpoint that ables you to send email through this.

## Usage

1. Clone this repository.
2. Modify the `smtp_config.txt` file with your SMTP configuration and details.
3. Build and run the Docker container using the following command: ```docker-compose up --build```
4. The contact API will be available at `http://localhost:3001/contact`.  This is accesible via POST request, check variables that must be send as urlencoded-form-data.
