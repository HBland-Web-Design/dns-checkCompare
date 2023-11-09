import json

def load_cache(cachePath):
    try:
        with open(cachePath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_response(key):
    responses = load_cache()

    if key in responses:
        return responses[key]
    else:
        new_response = generate_response_for_key(key)
        responses[key] = new_response
        save_cache(responses)
        return new_response

def generate_response_for_key(key):
    return f"Generated response for {key}"

def save_cache(cache, cachePath):
    with open(cachePath, 'w') as file:
        json.dump(cache, file)

def reset_cache():
    save_cache({})  # Clears the cache by saving an empty dictionary
