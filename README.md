# Django REST Framework Blog with Docker

A Django REST Framework application featuring a blog with authentication, posts, and pages. Built with Celery, RabbitMQ, and PostgreSQL, all containerized with Docker.

## Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - REST API toolkit
- **PostgreSQL 15** - Database
- **Celery 5.3.4** - Asynchronous task queue
- **RabbitMQ 3** - Message broker
- **Docker & Docker Compose** - Containerization
- **django-filter 23.5** - Advanced filtering

## Features

- Token-based authentication system
- Blog posts with full CRUD operations
- Static pages management (About, Contact, etc.)
- Celery for background tasks (e.g., welcome emails)
- RabbitMQ as message broker
- PostgreSQL database
- Docker Compose for easy setup
- API documentation with drf-spectacular (Swagger UI)
- CORS support
- Advanced filtering and search
- Permission-based access control

## Project Structure

```
django-interview/
├── config/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py           # Celery configuration
├── app/                     # Main application package
│   ├── authentication/      # User authentication module
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── tasks.py        # Auth-related Celery tasks
│   │   └── tests.py
│   ├── posts/              # Blog posts module
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   └── tests.py
│   └── pages/              # Static pages module
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       ├── permissions.py
│       ├── admin.py
│       └── tests.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── manage.py
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone or navigate to the project directory:
```bash
cd django-interview
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/docs/
- RabbitMQ Management: http://localhost:15672/ (username: admin, password: admin)

### Create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

## Services

The `docker-compose.yml` defines the following services:

- **db**: PostgreSQL database
- **rabbitmq**: RabbitMQ message broker with management plugin
- **web**: Django application server
- **celery_worker**: Celery worker for processing tasks
- **celery_beat**: Celery beat for scheduled tasks

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - Register a new user account
- `POST /api/auth/login/` - Login and get authentication token
- `POST /api/auth/logout/` - Logout (delete token)
- `GET /api/auth/profile/` - Get current user profile
- `PUT/PATCH /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Blog Posts (`/api/posts/`)
- `GET /api/posts/` - List all blog posts (with filtering/search)
- `POST /api/posts/` - Create a new post (authenticated)
- `GET /api/posts/{id}/` - Get a specific post
- `PUT/PATCH /api/posts/{id}/` - Update a post (author only)
- `DELETE /api/posts/{id}/` - Delete a post (author only)
- `GET /api/posts/my-posts/` - List current user's posts

### Pages (`/api/pages/`)
- `GET /api/pages/` - List all pages (with filtering/search)
- `POST /api/pages/` - Create a new page (authenticated)
- `GET /api/pages/navigation/` - Get navigation menu pages
- `GET /api/pages/my-pages/` - List current user's pages
- `GET /api/pages/{slug}/` - Get a specific page by slug
- `PUT/PATCH /api/pages/{slug}/` - Update a page (author only)
- `DELETE /api/pages/{slug}/` - Delete a page (author only)

### Documentation
- `GET /api/docs/` - Swagger UI documentation
- `GET /api/schema/` - OpenAPI schema

## Authentication

The API uses token-based authentication. To authenticate requests:

1. Register or login to get a token
2. Include the token in request headers:
```
Authorization: Token <your-token-here>
```

Example with curl:
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"securepass123","password2":"securepass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"securepass123"}'

# Use token in authenticated requests
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{"title":"My First Post","content":"Post content here","published":true}'
```

## Models

### Post Model
- `title` - Post title (max 200 chars)
- `slug` - Auto-generated URL-friendly slug
- `content` - Post content (TextField)
- `author` - Foreign key to User
- `published` - Boolean for publish status
- `created_at` - Auto timestamp
- `updated_at` - Auto timestamp

### Page Model
- `title` - Page title (max 200 chars)
- `slug` - Auto-generated URL-friendly slug
- `content` - Page content (TextField)
- `meta_description` - SEO meta description (max 160 chars)
- `author` - Foreign key to User
- `published` - Boolean for publish status
- `order` - Integer for navigation ordering
- `show_in_navigation` - Boolean for navigation visibility
- `created_at` - Auto timestamp
- `updated_at` - Auto timestamp

## Filtering and Search

Both posts and pages support:
- **Filtering**: Filter by published status, author, etc.
- **Search**: Search in title and content
- **Ordering**: Sort by various fields

Example:
```bash
# Search posts
GET /api/posts/?search=django

# Filter published posts
GET /api/posts/?published=true

# Order by creation date
GET /api/posts/?ordering=-created_at

# Combine filters
GET /api/posts/?published=true&search=django&ordering=-created_at
```

## Celery Tasks

Example tasks in `app/authentication/tasks.py`:

- `send_welcome_email(user_email, username)` - Sends welcome email to new users
- `cleanup_expired_tokens()` - Clean up expired authentication tokens

### Testing Celery

```bash
docker-compose exec web python manage.py shell
```

```python
from app.authentication.tasks import send_welcome_email

# Run task asynchronously
result = send_welcome_email.delay('user@example.com', 'john')
```

## Development

### Running migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Collecting static files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Running tests

```bash
docker-compose exec web python manage.py test
```

### Accessing Django shell

```bash
docker-compose exec web python manage.py shell
```

### Viewing logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
```

### Stopping the application

```bash
docker-compose down
```

### Stopping and removing volumes

```bash
docker-compose down -v
```

## Environment Variables

Key environment variables (see `.env.example`):

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `RABBITMQ_USER` - RabbitMQ username
- `RABBITMQ_PASSWORD` - RabbitMQ password
- `CELERY_BROKER_URL` - Celery broker URL
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins

## Admin Interface

Django admin is available at http://localhost:8000/admin/

Features:
- User management
- Post management with search, filters, and inline editing
- Page management with navigation ordering
- Token management

## Permissions

- **Public**: Can view published posts and pages
- **Authenticated**: Can create posts and pages, view own drafts
- **Authors**: Can edit/delete only their own posts and pages
- **Admin**: Full access via Django admin

## Production Considerations

Before deploying to production:

1. Change `SECRET_KEY` to a secure random value
2. Set `DEBUG=False`
3. Update `ALLOWED_HOSTS` with your domain
4. Use strong passwords for database and RabbitMQ
5. Configure proper CORS settings
6. Set up proper static file serving (e.g., with Nginx)
7. Use environment-specific settings
8. Enable HTTPS
9. Set up proper logging
10. Configure database backups
11. Set up email backend for Celery tasks
12. Consider using Redis for Celery results backend in production
13. Enable database connection pooling

## License

This project is provided as-is for interview purposes.
