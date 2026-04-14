# The base image
FROM python:3.11-slim

# 
#RUN apt install python3-pip


RUN pip install --upgrade pip

# set the working directory
WORKDIR /usr/src/

# copy server dir to app
COPY server/ ./app

WORKDIR /usr/src/app

# COPY requirements.txt ./

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install torch cpu for huggingface
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

ENV IMAGE_API_URL=${IMAGE_API_URL}
ENV IMAGE_API_KEY={IMAGE_API_KEY}
ENV TRANSFORMER_NER_MODEL=${TRANSFORMER_NER_MODEL}
ENV ULCA_USER_ID=${ULCA_USER_ID}
ENV ULCA_API_KEY=${ULCA_API_KEY}
ENV MEITY_PIPELINE_ID=${MEITY_PIPELINE_ID}

ENV HOST="0.0.0.0"
ENV PORT=8000

EXPOSE 8000

CMD ["python3", "main.py"]

