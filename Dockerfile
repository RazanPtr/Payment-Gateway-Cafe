FROM python:3.9
ADD lasti.py .
COPY . /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Install any necessary dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Command to run the FastAPI server when the container starts
CMD ["uvicorn", "lasti:app", "--host", "0.0.0.0", "--port", "80"]