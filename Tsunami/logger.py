def log(s, *args, log_type="LOG"):
    log = f"[{log_type}] {s}"
    if args:
        for arg in args:
            log += " " + str(arg)
    print(log)