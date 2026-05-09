# DevOps Quiz 3 - Selenium News Summary API

Registration: `FA23-BAI-013`

Assigned source: `Pakistan Today`

This project builds a Dockerized FastAPI service that uses Selenium with Chrome/ChromeDriver to search Pakistan Today, open the first article result for a keyword, summarize the article locally, and expose the required API on port `7000`.

## API

```http
GET /get?keyword=technology
```

Response shape:

```json
{
  "registration": "FA23-BAI-013",
  "newssource": "Pakistan Today",
  "keyword": "technology",
  "url": "https://www.pakistantoday.com.pk/...",
  "summary": "..."
}
```

The root page also shows the registration number:

```http
GET /
```

## Build

```bash
docker build -t devops-quiz-013:fa23-bai-013 .
```

## Run

```bash
docker run --rm -p 7000:7000 devops-quiz-013:fa23-bai-013
```

## Test API

```bash
curl http://localhost:7000/
curl "http://localhost:7000/get?keyword=technology"
```

## Docker Hub Tagging

Replace `your-dockerhub-username` with your Docker Hub username:

```bash
docker tag devops-quiz-013:fa23-bai-013 your-dockerhub-username/devops-quiz-013:fa23-bai-013
docker push your-dockerhub-username/devops-quiz-013:fa23-bai-013
```

## Local Tests

```bash
python3 -m pytest
```
