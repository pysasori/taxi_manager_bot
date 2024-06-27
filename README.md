# Taxi Manager Bot

This project is a Telegram bot designed to manage data about cars, drivers, and shifts. The bot utilizes Django as the
web framework, PostgreSQL for the database, and Celery for asynchronous tasks. The project is configured to run in
Docker containers.

## Installation

To run the project, you need Docker and Docker Compose installed.

1) Clone the repository
2) Set up the .env file:

- DEBUG=True
- ALLOWED_HOSTS=*
- DB_NAME=mydatabase
- DB_USER=myuser
- DB_PASSWORD=mypassword
- DB_HOST=db
- DB_PORT=5432
- TELEGRAM_BOT_TOKEN=your_telegram_bot_token

3) docker-compose up --build

## Usage
The bot provides the following functionalities:

- Manage cars and drivers: Add, delete, and edit information about cars and drivers.
- Track driver shifts: Monitor starting and ending mileage, start and end times of shifts
- Record fuel bills: Add data about the price and volume of refueling.

## Technologies Used

- Django
- PostgreSQL
- Celery
- Docker

## Prerequisites

- Docker installed on your system
