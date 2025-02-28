FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt update && apt install -y curl

RUN groupadd -g 1001 nonroot && \
   useradd -u 1001 -g nonroot nonroot \
   && chown -R nonroot:nonroot /app

USER nonroot

ENTRYPOINT ["python"]
CMD ["main.py"]