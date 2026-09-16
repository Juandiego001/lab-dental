FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .

# Instalar dependencias para weasyprint y fuentes
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    fontconfig \
    fonts-dejavu \
    fonts-freefont-ttf \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY ./fonts /usr/share/fonts/custom-calibri/
RUN fc-cache -f -v

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]