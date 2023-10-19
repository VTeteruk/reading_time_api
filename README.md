# Time Reading API

Reading Tracker is a Django-based web application that allows users to track their reading sessions and keep records of the books they've read.
___
## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
___
## Getting Started

To get started with Reading Tracker, follow the instructions below:

### Prerequisites

- [Python](https://www.python.org/) (>=3.6)
- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VTeteruk/reading_time_api.git
   ```
2. Navigate to the project directory:
    ```bash
    cd reading-tracker/
    ```
3. Create and activate venv file:
    ```bash
    python -m venv venv
    venv\Scripts\activate.bat
    ```
4. Fill `.env_sample` file and rename it to `.env`
5. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```
6. Create user to get access for everything (web url):
   ```bash
   http://localhost:8000/api/users/register
   http://localhost:8000/api/users/token
   ```
___
# API Endpoints
Use this url to access the documentation:
   ```bash
   http://localhost:8000/api/schema/swagger/
   ```

___
# Running Tests
To run the tests for Reading Tracker, use the following command:
   ```bash
   pytest
   ```
