import json
from datetime import datetime
from pydantic import BaseModel
import os
from typing import Optional, Dict, Any

import datetime
import boto3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from utils.utils import parse_byte_string_to_json, har_entry_to_curl

# 상수 정의
LOG_GROUP_NAME = "/subtrace-proxy-logs"

app = FastAPI(root_path="/mylog")


class CredentialsUpdate(BaseModel):
    region_name: str
    aws_access_key_id: str 
    aws_secret_access_key: str



@app.on_event("startup")
async def startup_event() -> None:
    app.state.region_name = "null"
    app.state.aws_access_key_id = "null"
    app.state.aws_secret_access_key = "null"

    app.state.websocket_connections = []


async def create_log_group(client: Any, log_group_name: str) -> None:
    try:
        client.create_log_group(logGroupName=log_group_name)
        print(f"로그 그룹 '{log_group_name}'을(를) 생성했습니다.")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"로그 그룹 '{log_group_name}'이(가) 이미 존재합니다.")


async def create_log_stream(client: Any, log_group_name: str, log_stream_name: str) -> None:
    try:
        client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
        print(f"로그 스트림 '{log_stream_name}'을(를) 생성했습니다.")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"로그 스트림 '{log_stream_name}'이(가) 이미 존재합니다.")


async def send_log_event(
    client: Any, 
    log_group_name: str, 
    log_stream_name: str, 
    log_data: Dict[str, Any], 
    sequence_token: Optional[str] = None
) -> str:
    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    log_message = json.dumps(log_data).replace("\\", "")
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
    
    return response['nextSequenceToken']


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    app.state.websocket_connections.append(websocket)
    print("WebSocket 연결이 수락되었습니다.")
    
    client = boto3.client(
        'logs',
        region_name=app.state.region_name,
        aws_access_key_id=app.state.aws_access_key_id,
        aws_secret_access_key=app.state.aws_secret_access_key
    )
    
    await create_log_group(client, LOG_GROUP_NAME)
    
    try:
        initial_data = await websocket.receive()
        parsed_initial_data = parse_byte_string_to_json(initial_data["bytes"])
        
        log_stream_name = (
            f'{parsed_initial_data["tags"]["process_command_line"]} '
            f'{datetime.datetime.now().strftime("%H.%M.%S")}~'
        )
        
        await create_log_stream(client, LOG_GROUP_NAME, log_stream_name)
        
        sequence_token = await send_log_event(
            client=client, 
            log_group_name=LOG_GROUP_NAME, 
            log_stream_name=log_stream_name, 
            log_data="Starting the proxy"
        )
        
        while True:
            data = await websocket.receive()
            parsed_data = parse_byte_string_to_json(data["bytes"])
            parsed_data["curl_command"] = har_entry_to_curl(parsed_data)
            parsed_data = dict(sorted(parsed_data.items()))

            sequence_token = await send_log_event(
                client,
                LOG_GROUP_NAME,
                log_stream_name,
                parsed_data,
                sequence_token
            )
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("클라이언트 연결이 종료되었습니다.")
    except Exception as e:
        print(e)

@app.post("/credentials")
async def update_credentials(credentials: CredentialsUpdate):

    app.state.region_name = credentials.region_name 
    app.state.aws_access_key_id = credentials.aws_access_key_id
    app.state.aws_secret_access_key = credentials.aws_secret_access_key

    connections = app.state.websocket_connections.copy()
    close_count = 0
    
    for websocket in connections:
        try:
            await websocket.close(code=1000)
            close_count += 1
        except Exception as e:
            print(e)

    return {"message": f"자격 증명이 성공적으로 업데이트되었습니다. 닫힌 연결 수 : {close_count}", "current_region": app.state.region_name}

@app.get("/healthcheck")
def healthcheck():
    response = {"server": "ok", "awscli": "valid"}
    try:
        client = boto3.client(
            'logs',
            region_name=app.state.region_name,
            aws_access_key_id=app.state.aws_access_key_id,
            aws_secret_access_key=app.state.aws_secret_access_key
        )
        client.describe_log_groups(limit=1)
    except Exception as e:
        print(e)
        response["awscli"] = "invalid"
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
