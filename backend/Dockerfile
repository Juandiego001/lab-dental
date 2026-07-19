FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .

# To install weasyprint
RUN apk add --no-cache \
    pango \
    fontconfig \
    ttf-dejavu \
    ttf-freefont \
    ttf-liberation \
    font-terminus
COPY ./fonts /usr/share/fonts/custom-calibri/
RUN fc-cache -f -v

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]