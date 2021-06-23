FROM python:3.7-slim

WORKDIR /automation_training

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    build-essential \
    software-properties-common \
    nano \
    ca-certificates \
    libjpeg-dev \
    libpng-dev &&\
    rm -rf /var/lib/apt/lists/*

RUN yes | pip install \
    wheel \
    uwsgi \
    nltk==3.5 \
    Bani==0.7.2 \
    nlpaug==1.1.3 &&\
    pip cache purge

RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

COPY . .

CMD python3 main.py

# In regards to volume -> to save the model files in container's directory:
# docker run -it -v /Users/karenw/desktop/automation_training/generatedModel:/automation_training/generatedModel bani_training
#to remove vol: docker rm -v



