# rest-api-flask
pip install -r requirements.txt
docker run -d -p 5000:5000 rest-apis-flask-python
or
docker run -dp 5005:5000 rest-apis-flask-python
or 
B1: Build
docker build -t rest-apis-flask-python .
B2: Run
<!-- docker run -dp 5000:5000 flask-smorest-api -->
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python
<!-- deploy -->
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python sh -c "flask run --host 0.0.0.0"