# Engineericly Feed

A Django application for managing product feeds with a modern admin interface using django-unfold.

## Features

- Django 5.2.7 with modern admin interface (django-unfold)
- Product management with platform-specific visibility (YouTube, TikTok, Instagram)
- File upload support for products
- Pin/unpin functionality for products
- Docker containerization with multi-stage builds
- SQLite database for simplicity
- Designed to work with external Nginx

## Quick Start

1. **Clone the repository and navigate to the project directory**
   ```bash
   cd /path/to/engineericly_feed
   ```

2. **Start the development environment**
   ```bash
   make up
   # or
   docker-compose up -d
   ```

3. **Access the application**
   - Application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Default superuser: `admin` / `admin123`

## Docker Commands

### Using Makefile (Recommended)

```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start development environment
make down          # Stop and remove containers
make restart       # Restart services
make logs          # Show logs
make shell         # Open shell in web container
make migrate       # Run Django migrations
make collectstatic # Collect static files
make clean         # Clean up containers and volumes
```

### Using Docker Compose Directly

```bash
# Start the application
docker-compose up -d
docker-compose logs -f
docker-compose exec web bash
```

## Environment Variables

Copy `env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## Project Structure

```
engineericly_feed/
├── config/                 # Django project settings
├── products/              # Products app
├── assets/                # Static assets
├── templates/             # Django templates
├── vol/                   # Volume mounts (static/media)
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Development environment
├── docker-compose.prod.yml # Production environment
├── nginx.conf            # Nginx configuration
├── start.sh              # Container startup script
├── Makefile              # Development commands
└── requirements.txt      # Python dependencies
```

## Docker Architecture

### Multi-Stage Dockerfile

- **Stage 1 (builder)**: Builds Python dependencies in virtual environment
- **Stage 2 (production)**: Runtime environment with minimal footprint

### Services

- `web`: Django application with SQLite database
- Designed to work with external Nginx for production

## Security Features

- Non-root user in containers
- Environment-based configuration
- Health checks for the service
- Volume isolation for data persistence

## Development

### Local Development (without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Adding New Dependencies

1. Add to `requirements.txt`
2. Rebuild Docker image: `make build`
3. Restart services: `make restart`

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   # Change port in docker-compose.yml
   ```

2. **Permission issues**
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER vol/
   ```

3. **Database connection issues**
   ```bash
   # Check database service
   docker-compose logs db
   # Reset database
   make clean
   make up
   ```

### Logs

```bash
# All services
make logs

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `make dev`
5. Submit a pull request

## License

This project is licensed under the MIT License.
