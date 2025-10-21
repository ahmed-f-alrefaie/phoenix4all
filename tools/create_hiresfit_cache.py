from phoenix4all.sources.hiresfits import list_available_files


from dataclasses import asdict
# Compress the list of available files into


with open("hiresfit_cache.json", "r") as f:
    result = json.load(f)




with open("hiresfit_cache.jsonz", "w") as f:
    json.dump(json_zip(result), f)



