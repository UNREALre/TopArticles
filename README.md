#Middle Python developer test task @ CASHOFF

## Installation info
Upload project files to your server.

Create virtual environment for the project.

Run within your newly created venv command:
>pip install -r requirements.txt

Create PostgreSQL database and corresponding user. Configure /top_news/settings.py DATABASES section with appropriate information. 

Ensure that folder /logs have required rights (write) for system logging.

All available APIs described within Postman collection, you can find the link below. Also, you can open collection using your desktop client and use basic auto tests for every API request to figure out if everything works fine.
https://documenter.getpostman.com/view/2849238/TVKEVGMV

####CRON
To run parsing process in schedule use crontab on your server. You will need the command below for your cron task:
>python manager.py run

## TODO
This is a list of functions that have to be implemented into project in near future. Have no time ATM for their implementation.

1. Find out how to use multithreading with Selenium Driver (saving session data)

2. Use Celery instead of CRON task command. 

3. Add functionality to parser, that removes missing articles from feed. If there is no article in the source feed, we need to exclude user link (foreign key) to this article in our DB, to prevent sending it to him.
