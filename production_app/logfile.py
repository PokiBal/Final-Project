with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    entry = last_line.strip().split(":")
    timestamp = entry[0] + ":" + entry[1]
    message = entry[4].strip().replace('"', '\\"')

print(f"{timestamp}, {message}")