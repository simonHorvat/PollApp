# PollApp

PollApp is a web application consisting of two elements: API and PollSite.
```
PollApp
├───API
└───PollSite
```
The site lets people view polls, vote in them, and subsequently view the results/statistics of poll

## API
The API component of PollApp is developed using FastAPI. It provides endpoints to retrieve information about polls and their attendees, as well as choice statistics.

### Endpoints

- GET /polls/{id}/attendees: Retrieves the total number of attendees for a specific poll.
- GET /polls/{id}/choice_statistics: Retrieves the choice statistics for a specific poll.

You can access the API documentation and test the endpoints using the following URL: [http://localhost:5000/docs](http://localhost:5000/docs)

### Code Overview

The API part has the following structure:
```
API
│   config.ini
│   Dockerfile
│   requirements.txt
│   run.py
│
├───app
│   │   main.py
│   │
│   └───routes
│           polls.py
│           __init__.py
│
├───database
│       database.py
│       models.py
│       __init__.py
│
└───schemas
        PollAttendeesResponse.py
        PollChoiceStatisticsResponse.py
        __init__.py
```
The main code for the API component can be found in the `app` directory. Here are the key files and directories:

- `main.py`: The entry point of the API application.
- `routes/polls.py`: Contains the API routes for retrieving attendees and choice statistics.
- `database`: Contains the database-related files such as `database.py` and `models.py`.
- `schemas`: Contains the schema definitions for the API responses.

## PollSite

The PollSite component of PollApp is a Django-based web application that allows users to view and interact with polls.

### Project Structure

The PollSite project follows the typical structure of a Django project. Here are the main files and directories:

- `IndexView`: Renders the index page, displaying the latest published polls.
- `QuestionListView`: Renders the question list page for a specific poll.
- `ResultsView`: Renders the results page for a specific poll, including total attendees and choice statistics.
- `vote`: Handles the vote submission for a poll.

### URLs

The following URLs are available for the PollSite component:

- `/`: The index page, displaying the latest published polls.
- `/polls/{poll_id}/questions/`: The question list page for a specific poll.
- `/polls/{poll_id}/vote/`: Handles the submission of votes for a specific poll.
- `/polls/{poll_id}/results/`: The results page for a specific poll, including total attendees, choice statistics and appropriate charts ([plotly.js](https://plotly.com/javascript/)).

### Running the Applications

To run the PollApp applications, you need to follow these steps:

1. Create a Docker network:

   ```shell
   docker network create mynetwork
   ```

2. Build and run the API container (from ```/API```):
   ```shell
   docker build -t api-image .
   ```
   ```shell
   docker run -d -p 5000:5000 -v path/to/db.sqlite3:/app/database/db.sqlite3 --name api-container --network mynetwork api-image
   ```
   Make sure to replace path/to/db.sqlite3 with the actual path (don't use relative path) to your SQLite database file.

3. Build and run the PollSite container (from ```/PollSite```):
   ```shell
   docker build -t pollsite-image .
   ```
   ```shell
   docker run -d -p 8000:8000 -v path/to/db.sqlite3:/app/db.sqlite3 --name pollsite-container --network mynetwork pollsite-image
   ```
   Make sure to replace path/to/db.sqlite3 with the actual path (don't use relative path) to your SQLite database file.

That's it! You now have the PollApp up and running, with both the API and PollSite components accessible.

## There's room for improvement!
This application has several areas that can be enhanced to make it better. Here are the main points to consider:

1. Front-end Enhancement: The application can benefit from additional pages, a consistent style using a shared base template (base.html), improved navigation elements, and separate html and js code within the Django project (template/static ...).

2. Server Architecture: Consider transitioning from a template provider to a data provider approach. This involves separating the server-side logic from the front-end and leveraging more advanced front-end frameworks like Angular, React, or Vue.js to enhance the user experience.

3. Database Upgrade: Consider using a more robust and scalable database solution like PostgreSQL or exploring other options that better suit the application's needs.

4. Improved Caching: Instead of relying on an in-memory cache, consider utilizing a dedicated database for caching purposes, such as Redis. This can provide better performance and more reliable caching capabilities.

5. Docker Compose Orchestration: Utilize Docker Compose to define and manage the containers within your application. This will simplify the deployment process and enable easier container orchestration.

6. Set the logging service: Use a logs manager like Kibana or Grafana.
   
8. Expand the database model (ORM): Collect more user data (such as age, sex, education, demographic...) to make statistics more powerful.
   
Many things are not finished, mainly due to time constraints or because I didn't feel it was part of the project.
