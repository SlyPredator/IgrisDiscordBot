FROM python:3.10.9
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt --upgrade
COPY . /bot
CMD python bot.py
