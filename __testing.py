# Convert string to float
def to_float(value, fallback=None):
    try: return float(value)
    except: pass
    return fallback

a = "10.5416"
b = to_float(value=a, fallback=None)

print(b)


