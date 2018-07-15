FROM python:3

ENV DEPLOY_WORKDIR /usr/src/app
ENV DEPLOY_RESOURCES_DIR deploy_resources

WORKDIR $DEPLOY_WORKDIR

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY $DEPLOY_RESOURCES_DIR/local_settings.py torpeekerback

# Install Chrome repo stuff
RUN \
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

RUN apt-get update

# Install Chrome itself
RUN apt-get install --yes google-chrome-stable

# Install ChromeDriver
RUN apt-get install --yes unzip
RUN wget https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin
RUN rm chromedriver_linux64.zip

# Clean apt package list
RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "gunicorn", "-b", ":8000", \
                  "--workers", "4", \
                  "torpeekerback.wsgi" ]
