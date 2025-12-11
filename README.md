# YourFirstCIM

A Computer Integrated Manufacturing (CIM) system for monitoring and managing manufacturing operations, featuring real-time equipment status tracking, OEE (Overall Equipment Effectiveness) analytics, and production management.

## Overview

YourFirstCIM is a full-stack web application that provides comprehensive manufacturing execution system capabilities including:

- Real-time equipment status monitoring
- OEE (Overall Equipment Effectiveness) calculation and visualization
- Gantt chart views for production scheduling
- Equipment maintenance management
- WIP (Work in Progress) tracking
- Production data queries and analytics
- Real-time notifications via Server-Sent Events (SSE)

## Tech Stack

### Backend
- **Framework**: FastAPI 0.110.0
- **Server**: Uvicorn 0.29.0
- **Database**: MySQL (via SQLAlchemy 2.0.29)
- **Cache**: Redis 7.0
- **Authentication**: JWT (PyJWT 2.8.0, python-jose 3.3.0)
- **File Storage**: AWS S3 (boto3)
- **Scheduling**: APScheduler 3.10.4
- **Data Visualization**: Matplotlib 3.8.4

### Frontend
- **Framework**: React 19.1.0
- **Build Tool**: React Scripts 5.0.1
- **Testing**: React Testing Library
- **Web Server**: Nginx

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Cache/Message Broker**: Redis 7.0

## Project Structure

```
yourfirstcim/
├── backend/
│   ├── app/
│   │   ├── db/              # Database connection and CRUD operations
│   │   ├── models/          # Business logic models
│   │   ├── routers/         # API route handlers
│   │   └── main.py          # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── cimapp/              # React application source
│   ├── static/              # Built static files
│   └── nginx.conf           # Nginx configuration
├── test/                    # Test files
├── docker-compose.yml       # Docker services configuration
└── .env.example             # Environment variables template
```

## Features

### Dashboard Pages
- **Dashboard**: Main overview of manufacturing operations
- **Equipment Gantt Chart**: Visual timeline of equipment usage
- **OEE Analytics**: Overall Equipment Effectiveness metrics
- **Equipment Status Query**: Real-time equipment status lookup
- **WIP Query**: Work in Progress tracking
- **Equipment Maintenance**: Maintenance records and scheduling
- **IE Maintenance**: Industrial Engineering maintenance tasks
- **IE Query**: Industrial Engineering data queries
- **Notifications**: Real-time system alerts

### API Capabilities
- User authentication and authorization
- Real-time data streaming via SSE
- Equipment status monitoring
- Production data queries
- Maintenance record management
- OEE calculation and reporting
- Chart generation and visualization
- Scheduled daily jobs for data processing

## Getting Started

### Prerequisites
- Docker and Docker Compose
- MySQL database
- AWS account (for S3 storage)
- Redis (included in docker-compose)

### Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Configure environment variables in `.env`:
```env
# MySQL Configuration
MYSQL_HOST=your_host
MYSQL_ROOT_USER=your_root_user
MYSQL_ROOT_USER_PASSWORD=your_root_user_password
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database_name
MYSQL_PORT=your_database_port

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=your_aws_region
AWS_BUCKET=your_aws_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain
```

### Installation & Running

#### Using Docker Compose (Recommended)

1. Build and start all services:
```bash
docker-compose up -d
```

2. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Redis: localhost:6379

3. Stop the services:
```bash
docker-compose down
```

#### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend/cimapp
npm install
npm start
```

**Redis:**
```bash
docker run -d -p 6379:6379 redis:7.0-alpine
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Backend Development
The backend uses FastAPI with modular routers:
- [charts.py](backend/app/routers/charts.py) - Chart generation endpoints
- [users.py](backend/app/routers/users.py) - User management
- [queries.py](backend/app/routers/queries.py) - Data query endpoints
- [maintain.py](backend/app/routers/maintain.py) - Maintenance management
- [sse.py](backend/app/routers/sse.py) - Server-sent events
- [notifications.py](backend/app/routers/notifications.py) - Notification system
- [oee.py](backend/app/routers/oee.py) - OEE calculations
- [daily_jobs.py](backend/app/routers/daily_jobs.py) - Scheduled tasks

### Frontend Development
The frontend is built with React and serves static HTML pages through Nginx in production.

## Architecture

### Services
1. **Backend**: FastAPI application handling business logic and API endpoints
2. **Frontend**: React application served by Nginx
3. **Redis**: Caching and pub/sub for real-time features
4. **MySQL**: Primary data store (external)
5. **AWS S3**: File storage (external)

### Key Features
- **APScheduler**: Automated daily jobs for data processing
- **SSE**: Real-time updates without WebSocket complexity
- **Redis Pub/Sub**: Real-time notification broadcasting
- **JWT Authentication**: Secure user authentication
- **SQLAlchemy ORM**: Type-safe database operations

## Testing

Backend tests are located in the [test/](test/) directory.

```bash
cd test
python -m pytest
```

## Deployment

The application is containerized and can be deployed using Docker Compose. For production:

1. Configure SSL certificates in [frontend/certs/](frontend/certs/)
2. Update [frontend/nginx.conf](frontend/nginx.conf) with production settings
3. Set production environment variables
4. Deploy using `docker-compose.yml`

## License

This project is part of the WeHelp Bootcamp training program.

## Contributing

This is a training project. For questions or issues, please contact the project maintainer.
