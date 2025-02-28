from utils import pubsub_pb2   # 생성된 Protocol Buffer 모듈
import base64
import json
from google.protobuf.json_format import MessageToJson

# WebSocket으로부터 받은 바이너리 데이터
raw_data = b'\n\x88\n\n\x85\n\n\x82\n\n#\n\x17process_executable_size\x12\x0812744800\n)\n\x17subtrace_linux_cpu_load\x12\x0e0.14 0.09 0.10\n\x14\n\nprocess_id\x12\x06153520\n\x1f\n\x14process_command_line\x12\x07./token\n\x1d\n\x18subtrace_linux_cpu_count\x12\x014\n\x1a\n\x08hostname\x12\x0eip-10-10-1-250\n&\n\x18subtrace_linux_mem_total\x12\n7921892 kB\n0\n\x08event_id\x12$d32e89bd-eb86-4078-87be-a9b116c9fc9f\n\x14\n\x0cprocess_user\x12\x04root\n*\n\x1csubtrace_linux_mem_available\x12\n6899072 kB\n&\n\x04time\x12\x1e2025-02-28T00:07:14.953105052Z\n \n\x17process_executable_name\x12\x05token\x12\xd3\x06{"_id":"d32e89bd-eb86-4078-87be-a9b116c9fc9f","startedDateTime":"2025-02-28T00:07:14.953119642Z","time":0,"request":{"method":"GET","url":"/","httpVersion":"HTTP/1.1","cookies":[],"headers":[{"name":"User-Agent","value":"curl/8.5.0"},{"name":"Accept","value":"*/*"},{"name":"Host","value":"localhost:8080"}],"queryString":[],"postData":{"mimeType":"","params":null,"text":""},"headersSize":-1,"bodySize":0},"response":{"status":404,"statusText":"Not Found","httpVersion":"HTTP/1.1","cookies":[],"headers":[{"name":"Content-Type","value":"text/plain"},{"name":"Date","value":"Fri, 28 Feb 2025 00:07:14 GMT"},{"name":"Content-Length","value":"18"}],"content":{"size":18,"mimeType":"text/plain","text":"NDA0IHBhZ2Ugbm90IGZvdW5k","encoding":"base64"},"redirectURL":"","headersSize":-1,"bodySize":18},"cache":null,"timings":{"send":0,"wait":0,"receive":0}}\x1a\x02\x10\x01'

def parse_byte_string_to_json(proto_binary):
    # Protocol Buffer 메시지 파싱
    message = pubsub_pb2.Message()
    message.ParseFromString(raw_data)

    # 메시지를 JSON으로 변환
    json_data = json.loads(MessageToJson(message))["concreteV1"]["event"]["concreteV1"]
    json_data["harEntryJson"] = json.loads(base64.b64decode(json_data["harEntryJson"]))
    
    return json_data