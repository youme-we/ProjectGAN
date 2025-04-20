FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=3002

EXPOSE 3002

CMD ["python3", "wrapper.py"]
