FROM python:3.10.5

RUN pip install --upgrade pip

WORKDIR /var/www/app 

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
   

EXPOSE 80