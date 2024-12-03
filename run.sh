

docker compose up -d fastapi-server --build
docker compose up test-runner --build ; docker compose up -d allure-reports --build
echo "go to -> http://localhost:5001"
