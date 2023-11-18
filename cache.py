import json

def load_cache(cachePath):
    try:
        with open(cachePath, 'r') as file:
            cached_data = json.load(file)
            return cached_data
    except FileNotFoundError:
        return f"FileNotFound"
    except Exception as e:
        print(str(e))
        return e

def get_response(key):
    try:
        responses = load_cache()  # Assuming load_cache() loads the cache data
        
        if responses and key in responses:
            return responses[key]
        else:
            new_response = generate_response_for_key(key)  # Assuming this function generates a response
            if responses is None:  # If cache is empty or not loaded
                responses = {}  # Initialize an empty dictionary
            responses[key] = new_response
            save_cache(responses)  # Assuming this function saves the updated cache
            return new_response
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        return None  # Return None in case of an error

def generate_response_for_key(key):
    print ("Generated response for {key}")
    return f"Generated response for {key}"

def save_cache(cache, cachePath):
    try:
        with open(cachePath, 'w') as file:
            for response in cache:
                serialized_response = json.dumps(response, separators=(',', ':'))
                file.write(serialized_response + '\n')
        print(f"JSON data saved to {cachePath} successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def reset_cache(cache, cachePath):
    try:
        with open(cachePath, 'w+') as file:  # Using 'w+' mode to enable file truncation
            file.truncate(0)  # Truncate the file content to reset it to blank
            file.write('[\n')
            # for response in cache:
            for index, response in enumerate(cache):
                serialized_response = json.dumps(response, separators=(',', ':'))
                file.write(serialized_response)
                if index < len(cache) - 1:
                    file.write(',')
                file.write('\n')
            file.write(']')
        print(f"JSON data saved to {cachePath} successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def cache_compare(current_check, cacheLoaded):
    try:
        cache_data = cacheLoaded
        current_data = current_check
        Results = []
        for current_record in current_data:
            # print(f"{current_record['record']},{current_record['recordType']}")
            # print("----------------------")
            for cache_record in cache_data:
                # print(cache_record)
                # print("++++++++++++++++++++++")
                if current_record["record"] == cache_record["record"] and current_record["recordType"] == cache_record["recordType"]:
                    Result = {}
                    Result['domain'] = current_record["domain"]
                    Result['record'] = current_record["record"]
                    Result['recordType'] = current_record["recordType"]
                    if current_record["recordValue"] == cache_record["recordValue"]:
                        # print(f"Record {current_record['record']},{current_record['recordType']} for Domain {current_record['domain']} matches Cache")
                        Result['status'] = "Pass"
                        # print("Pass")
                        # print(f"----")
                    else:
                        Result['status'] = "Fail"
                        Result['msg'] = {}
                        Result['msg']['ExpectedValue'] = cache_record['recordValue']
                        Result['msg']['CurrentValue'] = current_record['recordValue']
                        # print(f"Record {current_record['record']},{current_record['recordType']} for Domain {current_record['domain']} does not match Cache")
                        # print(f"Current Value: {current_record['recordValue']}")
                        # print(f"Expected Value: {cache_record['recordValue']}")
                        # print(f"#######################################")
                        # print("Fail")
                        # print(f"----")

                    Results.append(Result)
                else:
                    continue
        return Results
    except FileNotFoundError:
        print("Cache file not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format in cache or current check.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")