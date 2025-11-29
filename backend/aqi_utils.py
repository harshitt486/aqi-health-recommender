# CPCB Breakpoints for PM2.5
pm25_breakpoints = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 500, 401, 500)
]

# CPCB Breakpoints for PM10
pm10_breakpoints = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 600, 401, 500)
]

def calculate_subindex(C, breakpoints):
    for (BPlo, BPhi, Ilo, Ihi) in breakpoints:
        if BPlo <= C <= BPhi:
            return ((Ihi - Ilo) / (BPhi - BPlo)) * (C - BPlo) + Ilo
    return None

def compute_aqi_from_pm(pm25, pm10):
    subindices = []

    if pm25:
        si25 = calculate_subindex(pm25, pm25_breakpoints)
        if si25:
            subindices.append(si25)

    if pm10:
        si10 = calculate_subindex(pm10, pm10_breakpoints)
        if si10:
            subindices.append(si10)

    if not subindices:
        return None

    return max(subindices)

def aqi_category(aqi):
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Severe"
