def generate_random_number(length):
    start_range = 10 ** (length - 1)
    end_range = (10 ** length) - 1
    return random.randrange(start_range, end_range)