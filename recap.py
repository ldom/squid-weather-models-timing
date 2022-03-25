def get_times(timing_map):
    unique_times = set()
    for t in timing_map.values():
        unique_times.update(t["avail_times"].keys())
    return sorted(unique_times)

def get_recap_table(timing_map):
    times = get_times(timing_map)
    result = [["model/availability time", *times],]

    for model_name, model_times in timing_map.items():
        model_line = [model_name,]
        for t in times:
            model_line.append(model_times["avail_times"].get(t, ""))
        result.append(model_line)

    return result
