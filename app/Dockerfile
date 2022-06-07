FROM python:3.6
#workspace
ADD . /app
WORKDIR /app
#Requeriments
RUN pip install -r requirements.txt
#port
# EXPOSE 5000
CMD ["python3", "-u", "app.py"]