FROM python:3.12-slim

ENV TZ=Asia/Taipei
RUN apt-get update && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

