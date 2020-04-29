FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN python --version

COPY client_secret.json .
COPY . .

CMD [ "python", "./bot.py" ]
