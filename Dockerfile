FROM python:3.8.5-buster as base
RUN pip install poetry
EXPOSE 8000
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false --local && poetry install --no-root --no-dev

FROM base as prod
COPY . /code/
ENTRYPOINT "poetry run gunicorn 'app:create_app()' --bind 0.0.0.0:$PORT"

FROM base as dev
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 8000

FROM base as test
COPY . /code/

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    rm /var/lib/apt/lists/* -vf &&\
    apt-get clean &&\
    apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip

ENTRYPOINT [ "poetry", "run", "pytest" ]