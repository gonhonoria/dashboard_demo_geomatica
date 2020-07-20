FROM ubuntu:latest

RUN  hash -r pip

RUN apt-get update && apt-get install -y python3-pip python3-dev build-essential

# Set the locale
ENV LANG C.UTF-8 
ENV LANGUAGE C.UTF-8  
ENV LC_ALL C.UTF-8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

Expose 8501

CMD streamlit run app.py
