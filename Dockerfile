# Dockerfile

ARG         AWS_ACCOUNT=437795906767

FROM        ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/docker-parent-images:python38 AS base

WORKDIR     /var/app

# Update and install common packages
RUN         yum -y update
RUN         yum -y install curl git tar zip

# Create and configure virtualenv and uwsgi
ENV         VIRTUAL_ENV /var/venv
RUN         python3.8 -m venv ${VIRTUAL_ENV}
ENV         PATH "$VIRTUAL_ENV/bin:$PATH"

RUN         pip install --upgrade pip
RUN         pip install uwsgi
RUN         useradd uwsgi -s /bin/false

# Add application and install requirements
ADD         . /var/app
RUN         if [ -f /var/app/requirements.txt ]; then pip install -I -r /var/app/requirements.txt; fi

# Build image for live deployment
FROM        base AS deploy

# Remove tests
RUN         rm -rf /var/app/tests

# Add startup script
ADD         uwsgi-start.sh /
RUN         chmod +x /uwsgi-start.sh
ENTRYPOINT  ["/uwsgi-start.sh"]

EXPOSE      8080

# Build the dev stage
FROM        base AS dev

# httpretty install complains about some unicode error without this
ENV         LC_ALL=en_US.utf-8
ENV         LC_CTYPE=en_US.UTF-8

RUN         pip install -r /var/app/requirements-dev.txt

# Enables prints in python to flush to stdout
ENV         PYTHONUNBUFFERED 1
# Start dev server
ENTRYPOINT  ["/var/venv/bin/python"]
CMD         ["dev.py", "2>&1"]
