FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --progress-bar  off -r requirements.txt

# Mounts the application code to the image
COPY ./src /app
WORKDIR /app

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
