import time

def paginate_users(page_size, offset):
    time.sleep(0.1)
    start_index = offset
    end_index = offset + page_size
    users = [f"user_{i}" for i in range(start_index, end_index)]
    return users

def lazy_paginate(page_size):
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        yield users
        offset += page_size

if __name__ == '__main__':
    page_size = 10
    for page in lazy_paginate(page_size):
        print(f"Fetched page with users: {page}")
        if len(page) < page_size:
            break
