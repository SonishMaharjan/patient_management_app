FROM python:3.10
EXPOSE 5000
WORKDIR /app
# THIS IS SEPERATE COPY BECUASE WHEN copy below changes, this copy with will cached and RUN pip install -R is not run
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# docker build -t rest-apis-flask-python .

# docker run -p 5005:5000 rest-apis-flask-python

# run as daemon ( background)
# docker run -d -p 5005:5000 rest-apis-flask-python

# runing docker with volume ( while developing) so that you dont have to rebuild image every time you changes
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python
