# Your First CIM App

A lightweight CIM (Computer Integrated Manufacturing) application designed for entry-level Industrial Engineering (IE) engineers to practice, manage, and monitor production-related data.

## Features

- Simulated production data
- MySQL schema design and CRUD operations
- Real-time notifications using Server-Sent Events (SSE)
- Gantt chart visualization via frontend interface
- Dockerized environment with AWS deployment support

## Tech Stack

**Backend:**

- Python (FastAPI)
- MySQL
- Redis (for SSE pub/sub)

**Frontend:**

- HTML, SCSS, JavaScript

**Database:**

- MySQL

**DevOps & Deployment:**

- Docker, Nginx
- AWS EC2, RDS, S3, CloudFront

## Project Instructions

**Structure:**

- Users visit the website and log in to access features.
- The main index page includes a real-time data table for production monitoring.
- Core functions include:
  - **Search**: query production data by date, equipment, or status.
  - **Maintain**: update standard times and equipment status records.
  - **Notifications**: receive real-time alerts via Server-Sent Events (SSE).

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/structure.png)

**ER Diagram:**

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/ER_diagram.png)

**Redis & SSE Flow:**

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/drawio.png)
