# Following the template here, which seems to chime nicely with recent
# Docker getting started tutorials:
# https://fastapi.tiangolo.com/deployment/docker/?h=requirements.txt#dockerfile
FROM python:3.8
WORKDIR /code

# Copying in package dependency definitions (and installing them) is
# good Docker practice to take advantage of caching.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Having done that, we can copy the rest of the code etc. over.
COPY ./app /code/app

# Run the app/server. Note the typical IP/port to run on in a container
# differs from when running locally.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]