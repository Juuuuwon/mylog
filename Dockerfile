FROM python:3.12-slim

WORKDIR /app

RUN pip install fastapi uvicorn[standard] boto3 protobuf

COPY . .

RUN apt update && apt install -y --no-install-recommends curl tzdata && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1001 nonroot && \
    useradd -u 1001 -g nonroot nonroot \
    && chown -R nonroot:nonroot /app

USER nonroot

ENV TZ=Asia/Seoul

ENTRYPOINT ["python"]
CMD ["main.py"]
