from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils.utils import parse_byte_string_to_json
from datetime import datetime
import boto3
import json

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.region_name = "ap-northeast-2"
    app.state.access_key_id = "AKIA36Z6VRBICXVFVT4Q"
    app.state.secret_access_key = "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"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = boto3.client(
            'logs',
            region_name=app.state.region_name,
            aws_access_key_id=app.state.access_key_id,
            aws_secret_access_key=app.state.secret_access_key
    )
    
    log_group_name = "/subtrace-proxy-logs"
    try:
        client.create_log_group(logGroupName=log_group_name)
        print(f"로그 그룹 '{log_group_name}'을(를) 생성했습니다.")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"로그 그룹 '{log_group_name}'이(가) 이미 존재합니다.")

    data = await websocket.receive()
    parsed_data = parse_byte_string_to_json(data["bytes"])
    log_stream_name = f'{parsed_data["tags"]["process_command_line"]} {parsed_data["tags"]["event_id"]}'

    try:
        client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
        print(f"로그 스트림 '{log_stream_name}'을(를) 생성했습니다.")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"로그 스트림 '{log_stream_name}'이(가) 이미 존재합니다.")

    sequence_token = None

    try:
        while True:
            data = await websocket.receive()
            # print(data)
            parsed_data = parse_byte_string_to_json(data["bytes"])
            # print(parsed_data)

            timestamp = int(datetime.now().timestamp() * 1000)
            log_message = json.dumps(parsed_data)
            log_event = {"timestamp": timestamp, "message": log_message}

            if sequence_token:
                response = client.put_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    logEvents=[log_event],
                    sequenceToken=sequence_token
                )
            else:
                response = client.put_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    logEvents=[log_event]
                )
            sequence_token = response['nextSequenceToken']
            print(response)


    except WebSocketDisconnect:
        print("Client disconnected.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
