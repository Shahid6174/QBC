def weighted_moving_average(data, window_size):
   
    if not data or window_size <= 0 or window_size > len(data):
        return []
    
    wma = []
    weights = list(range(1, window_size + 1))
    weight_sum = sum(weights)
    
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        weighted_sum = sum(w * x for w, x in zip(weights, window))
        wma.append(weighted_sum / weight_sum)
    return wma
