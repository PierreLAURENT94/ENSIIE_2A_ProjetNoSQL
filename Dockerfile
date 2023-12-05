FROM python:3.10
 
ENV HOST=0.0.0.0
 
ENV LISTEN_PORT 8080
 
EXPOSE 8080
 
RUN apt-get update && apt-get install -y libpq-dev python3-dev

RUN pip install --no-cache-dir --upgrade streamlit pymongo psycopg2
 
COPY ./app /app/
 
CMD ["streamlit", "run", "/app/app.py", "--server.port", "8080"]