FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
        wget https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz && \
        tar -xzf enron_mail_20150507.tar.gz

COPY main.py .
COPY models.py .

CMD [ "python", "main.py" ]