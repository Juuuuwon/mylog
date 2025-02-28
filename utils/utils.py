from utils import pubsub_pb2   # 생성된 Protocol Buffer 모듈
import base64
import json
import shlex
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


def har_entry_to_curl(har_data):
    """
    HAR 데이터(딕셔너리)를 curl 명령어로 변환합니다.
    
    Args:
        har_data (dict): HAR 데이터가 포함된 딕셔너리
        
    Returns:
        str: 변환된 curl 명령어
    """
    # 입력이 딕셔너리가 아니면 오류 반환
    if not isinstance(har_data, dict):
        return "오류: 입력은 딕셔너리 형태여야 합니다."
    
    # harEntryJson 키 처리
    if "harEntryJson" in har_data:
        har_entry = har_data["harEntryJson"]
    else:
        har_entry = har_data
    
    # 기본 요소 확인
    if not all(key in har_entry for key in ["request", "response"]):
        return "오류: 필수 요소(request 또는 response)가 JSON에 없습니다."
    
    request = har_entry["request"]
    
    # 기본 curl 명령어 구성
    method = request.get("method", "GET")
    url = request.get("url", "")
    
    # URL에 호스트가 포함되어 있지 않으면 Host 헤더에서 가져옴
    if not url.startswith(("http://", "https://")):
        host_header = next((h["value"] for h in request.get("headers", []) if h["name"].lower() == "host"), None)
        
        if host_header:
            scheme = "https" if method == "CONNECT" else "http"
            url = f"{scheme}://{host_header}{url}"
    
    curl_cmd = ["curl"]
    
    # 메서드 추가
    if method != "GET":
        curl_cmd.extend(["-X", method])
    
    # 헤더 추가
    for header in request.get("headers", []):
        # User-Agent는 curl에서 기본적으로 설정하므로 중복 방지
        if header["name"].lower() not in ["content-length", "host"] and not (
            header["name"].lower() == "user-agent" and "curl" in header["value"].lower()
        ):
            curl_cmd.extend(["-H", f"{header['name']}: {header['value']}"])
    
    # POST 데이터 추가
    if "postData" in request and request["postData"].get("text"):
        # Content-Type 헤더 확인
        content_type = request["postData"].get("mimeType", "")
        post_data = request["postData"]["text"]
        
        if content_type.startswith("application/json"):
            curl_cmd.extend(["-d", post_data])
        else:
            curl_cmd.extend(["--data-raw", post_data])
    
    # 쿼리 문자열 처리 (이미 URL에 포함되어 있으므로 별도 처리 불필요)
    
    # URL 추가 (마지막에 추가)
    curl_cmd.append(url)
    
    # 기타 옵션들 (필요에 따라 추가)
    # curl_cmd.append("-v")  # 상세 출력
    
    # 문자열로 변환 (쉘 이스케이핑 적용)
    return " ".join(shlex.quote(arg) if ' ' in arg else arg for arg in curl_cmd)