FROM python:3.10

WORKDIR /app

COPY installs.txt installs.txt
RUN pip install -r installs.txt

COPY . .

CMD ["python", "application.py"]  # or whatever your main file is
