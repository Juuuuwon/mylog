from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils.utils import parse_byte_string_to_json
app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 연결이 수립되었습니다")

    try:
        while True:
            data = await websocket.receive()
            parsed_data = parse_byte_string_to_json(data["bytes"])
    except WebSocketDisconnect:
        print("클라이언트 연결이 종료되었습니다")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
