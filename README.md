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
- The main index page includes a data table for daily production monitoring.
- Core functions include:
  - **Search**: query production data by date, equipment, or status.
  - **Maintain**: update standard times and equipment status records.
  - **Notifications**: receive real-time alerts via Server-Sent Events (SSE).

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/structure.png)

**ER Diagram:**

The database schema includes the following key tables:

- `eqp_status`: tracks the status of each equipment.
- `standard_times`: stores standard operation time for each product.
- `prod_info`: basic product information.
- `temp_oee`: temporarily stores raw data for calculating OEE (Overall Equipment Effectiveness).
- `final_oee`: stores finalized and aggregated OEE results for display and analysis.
- `users`: stores user credentials and roles.

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/ER_diagram.png)

**Redis & SSE Flow:**

![image](https://github.com/cmchiu-grover/your-first-cim/blob/main/img/drawio.jpg)
