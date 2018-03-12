FROM python:3.6-alpine
RUN pip install boto3 requests

ADD . /app/
CMD ["python /app/update_route_53_records.py"]
