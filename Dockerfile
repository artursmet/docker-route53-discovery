FROM python:3.6-alpine
RUN pip install boto3 requests

ADD update_route53_records.py /
CMD ["python", "/update_route53_records.py"]
