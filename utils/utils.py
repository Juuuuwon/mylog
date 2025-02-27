import utils.subtrace_pubsub_pb2 as subtrace_pubsub_pb2
import json

def parse_byte_string_to_json(byte_string):
    # 1. 태그와 har_entry_json 파싱
    tags = {}
    json_start = byte_string.find(b'{')
    if json_start == -1:
        raise ValueError("No JSON found in byte_string")
    har_entry_json = byte_string[json_start:]
    
    position = 0
    while position < json_start:
        p = byte_string.find(b'\x12', position)
        if p == -1 or p >= json_start:
            break
        q = byte_string.rfind(b'\n', 0, p)
        key_start = q + 1 if q != -1 else 0
        key = byte_string[key_start:p].decode('utf-8', errors='ignore').strip()
        
        position = p + 1
        if position >= len(byte_string):
            break
        value_length = byte_string[position]
        position += 1
        if position + value_length > len(byte_string):
            break
        value = byte_string[position:position + value_length].decode('utf-8', errors='ignore')
        position += value_length
        
        r = byte_string.find(b'\n', position)
        if r == -1:
            break
        position = r + 1
        
        tags[key] = value
    
    # 2. Protobuf 메시지 생성
    message = subtrace_pubsub_pb2.Message()
    event_v1 = message.concrete_v1.event.concrete_v1
    
    # 태그 설정
    for key, value in tags.items():
        event_v1.tags[key] = value
    
    # har_entry_json 설정
    event_v1.har_entry_json = har_entry_json
    
    # 3. 직렬화
    serialized = message.SerializeToString()
    
    # 4. 역직렬화
    parsed_message = subtrace_pubsub_pb2.Message()
    parsed_message.ParseFromString(serialized)
    
    # 5. JSON 데이터 후처리
    parsed_har_entry_json = parsed_message.concrete_v1.event.concrete_v1.har_entry_json
    json_str = parsed_har_entry_json.decode('utf-8', errors='ignore')
    processed_json_str = json_str.replace("null", "0").rsplit("}", 1)[0] + "}"
    parsed_data = json.loads(processed_json_str)
    
    return parsed_data
