# Sales Research API

AI-powered sales prospect research automation API.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/sales-research-api.git
cd sales-research-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start development environment:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

6. Run migrations:
```bash
alembic upgrade head
```

7. Access the API:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

## Development

- Run tests: `pytest`
- Format code: `black .`
- Check types: `mypy .`
- Lint code: `flake8`

## API Documentation

Detailed API documentation is available at `/docs` when running the server.

## License

MIT