# Contributing

## Setup

```bash
pipenv install -d
pipenv run pre-commit install --config .pre-commit-config.yml
pipenv run inv qa
```

## Running locally

1. Set and load environment variables:
```bash
cp .example.env .env
edit .env
pipenv shell
```

2. Run dev server:
```bash
uvicorn mailer.app:app --host 0.0.0.0 --port 8000
```
or if using VSCode, use the following configuration in `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "mailer:app",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["--host=0.0.0.0", "--port=8000", "mailer:app"],
      "envFile": "",
      "justMyCode": false
    },
    {
      "name": "mailer:tests",
      "type": "python",
      "request": "test",
      "justMyCode": false
    }
  ]
}
```

3. Try it:
```bash
http GET http://localhost:8000/
http POST http://localhost:8000/api/mail \
    Origin:http://localhost:8000 \
    email="john@doe.com" \
    name="John Doe" \
    subject="Test 💫" \
    message="Hello 👋" \
    honeypot=""
```

4. Open the Swagger OpenAPI documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## Examples

Run the examples:

```
cd examples
pipenv run python -m http.server 5000
```
