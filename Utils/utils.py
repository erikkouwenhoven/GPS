def pretty_time_diff(timestamp_from: float, timestamp_to: float) -> str:
    delta = int(timestamp_to - timestamp_from)
    day = (delta % 86400)// 86400
    delta -= day * 86400
    hour = (delta // 3600)
    delta -= hour * 3600
    minute = delta // 60
    delta -= minute * 60
    sec = int(delta % 60)
    res = f"{day}d" if day > 0 else ""
    res += f"{hour}h" if hour > 0 else ""
    res += f"{minute}m" if minute > 0 else ""
    res += f"{sec}s" if sec > 0 else ""
    return res


if __name__ == "__main__":
    from datetime import datetime
    ts = datetime.now().timestamp()
    print(pretty_time_diff(ts, ts + 10))
    print(pretty_time_diff(ts, ts + 100))
    print(pretty_time_diff(ts, ts + 1000))
    print(pretty_time_diff(ts, ts + 10000))
