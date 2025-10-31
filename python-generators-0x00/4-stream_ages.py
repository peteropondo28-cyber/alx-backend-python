def stream_user_ages(user_data):
    for user in user_data:
        yield user['age']


def calculate_average_age(user_data):
    total_age = 0
    count = 0
    for age in stream_user_ages(user_data):
        total_age += age
        count += 1
    return total_age / count if count else 0


if __name__ == "__main__":
    user_data = [
        {'age': 30}, {'age': 25}, {'age': 40}, {'age': 22}, {'age': 35},
        {'age': 28}, {'age': 45}, {'age': 32}, {'age': 27}, {'age': 38},
        {'age': 31}, {'age': 29}, {'age': 42}, {'age': 24}, {'age': 36},
        {'age': 33}, {'age': 26}, {'age': 41}, {'age': 23}, {'age': 37}
    ] * 500

    average_age = calculate_average_age(user_data)
    print(f"Average age of users: {average_age}")
