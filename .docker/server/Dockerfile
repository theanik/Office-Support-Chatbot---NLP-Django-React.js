
# pull official base image
FROM python:3.11.1

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore
# DOCKER_BUILDKIT=1


# set work directory
WORKDIR /app


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# install dependencies
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
COPY ./requirements.txt .
# RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip cache list
# RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt
# RUN --mount=type=cache,target=/root/.cache \
#     pip3 install -r requirements.txt

RUN pip3 install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('stopwords')" ]
RUN [ "python", "-c", "import nltk; nltk.download('wordnet')" ]
RUN [ "python", "-c", "import nltk; nltk.download('omw-1.4')" ]
RUN [ "python", "-c", "import nltk; nltk.download('punkt')" ]
RUN [ "python", "-c", "import nltk; nltk.download('averaged_perceptron_tagger')" ]


# copy entrypoint.sh
COPY ./entrypoint.sh /
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ENV VIRTUAL_ENV=/opt/venv
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]