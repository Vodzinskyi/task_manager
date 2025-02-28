# Task Manager

A simple, effective task management tool designed for personal productivity.

## Overview
Task Manager is a lightweight application that helps you organize projects and tasks efficiently. Built for individuals who are passionate about productivity, it provides essential features to manage your task-flow without unnecessary complexity.

## Features

- **Project Management**: Create, update, and delete projects
- **Task Organization**: Add, update, and delete tasks within projects
- **Task Prioritization**: Reorder tasks to set priorities
- **Deadlines**: Assign due dates 
- **Task Completion**: Mark tasks as 'done'

## Technology Stack

- **Backend**: Django
- **Frontend**: Alpine.js, HTMX, Bootstrap v5
- **Database**: PostgreSQL

## Getting Started
    
You can either use the [deployed version](https://task-manager-5e8t.onrender.com/) of the application or run it locally by following the instructions below

### Prerequisites

Make sure you have [Docker](https://www.docker.com/) installed on your machine

### Installation & Running Locally

1. Clone the repository:
```
git clone https://github.com/Vodzinskyi/task_manager
cd task-manager
```

2. Start the application using Docker Compose:
```
docker-compose up --build
```

3. The application will be available at http://localhost:8000.

### Stopping the Application
To stop the containers, run:
```
docker-compose down
```