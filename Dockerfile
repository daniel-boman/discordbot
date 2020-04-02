FROM python:3

ADD *.py /
ADD modules/*.py /modules

CMD ["python", "./__init__.py"]