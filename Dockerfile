FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY docker_resources/local_settings.py torpeekerback

RUN apt update

# Install Chrome 
RUN apt install --yes chromium

# Install ChromeDriver
RUN apt install --yes unzip
RUN wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin
RUN rm chromedriver_linux64.zip

ENTRYPOINT [ "gunicorn", "-b", ":8080", "torpeekerback.wsgi" ]
