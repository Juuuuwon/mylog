from utils import pubsub_pb2   # 생성된 Protocol Buffer 모듈
import base64
import json
import shlex
from google.protobuf.json_format import MessageToJson


def parse_byte_string_to_json(proto_binary):
    # Protocol Buffer 메시지 파싱
    message = pubsub_pb2.Message()
    message.ParseFromString(proto_binary)

    # 메시지를 JSON으로 변환
    json_data = json.loads(MessageToJson(message))["concreteV1"]["event"]["concreteV1"]
    json_data["harEntryJson"] = json.loads(base64.b64decode(json_data["harEntryJson"]))
    
    return json_data


def har_entry_to_curl(har_data):
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
        if header["name"].lower() not in ["content-length", "host", "accept"] and not (
            header["name"].lower() == "user-agent" and "curl" in header["value"].lower()
        ) and header["name"].startswith("x-") == False:
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
    return (" ".join(shlex.quote(arg) if ' ' in arg else arg for arg in curl_cmd))
