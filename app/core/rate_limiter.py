import time 

max_request = 5
window_seconds = 60 

requests = {}

def check_rate_limit(
    client_id: str | int
) -> bool:

    now = time.time()

    if client_id not in requests:
        requests[client_id] = []

    requests[client_id] = [
        timestamp
        for timestamp in requests[client_id]
        if now - timestamp < window_seconds
    ]

    if len(requests[client_id]) >= max_request:
        oldest_request = requests[client_id][0]
        retry_after = int(
            window_seconds - (now - oldest_request)
        ) + 1

        return False, retry_after

    requests[client_id].append(now)

    return True, 0