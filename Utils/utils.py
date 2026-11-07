def pretty_time_diff(timestamp_from: float, timestamp_to: float) -> str:
    delta = int(timestamp_to - timestamp_from)
    sec = int(delta % 60)
    delta -= sec
    min = delta // 60
    delta -= min * 60
    hour = delta // 3600
    delta -= hour * 3600
    day = delta // 86400
    res = f"{day}d" if day > 0 else ""
    res += f"{hour}d" if hour > 0 else ""
    res += f"{min}m" if min > 0 else ""
    res += f"{sec}s" if sec > 0 else ""
    return res
