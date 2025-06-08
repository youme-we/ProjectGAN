FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT_NN=3002

EXPOSE 3002

ENV PROJECT_NAME="GAN1"

CMD ["python3", "wrapper.py"]
