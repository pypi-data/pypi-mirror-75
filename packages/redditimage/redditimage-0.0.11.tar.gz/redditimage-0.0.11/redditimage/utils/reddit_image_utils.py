# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import time

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def username(username: float) -> str:
    return username if username.startswith('u/') else 'u/' + username

def sub(sub: float) -> str:
    return sub if sub.startswith('r/') else 'r/' + sub

def number_text(number: float) -> str:
    if number < 1000:
        return str(number)
    
    float_num = float(number)
    int_num_k = int(float_num/1000)

    remaining = number - int_num_k*1000
    remaining_h = int(float(remaining/100))

    return str(int_num_k) + '.' + str(remaining_h) + 'k'#('.' + str(remaining_h) if remaining_h > 0 else '') + 'k'

def date_text(timestamp: float) -> str:
    duration = int(time.time() - timestamp)

    dur = 0
    mu = ''

    if duration < 60:           # 1 minute
        dur = duration
        mu = 'seconds'
    elif duration < 120:        # 2 minutes
        dur = 1
        mu = 'minute'
    elif duration < 3600:       # 1 hour
        dur = int(duration/60)
        mu = 'minutes'
    elif duration < 7200:       # 2 hours
        dur = 1
        mu = 'hour'
    elif duration < 86400:      # 1 day
        dur = int(duration/3600)
        mu = 'hours'
    elif duration < 172800:     # 2 days
        dur = 1
        mu = 'day'
    elif duration < 2592000:    # 30 days
        dur = int(duration/86400)
        mu = 'days'
    elif duration < 5184000:    # 60 days
        dur = 1
        mu = 'month'
    elif duration < 31536000:   # 1 year
        dur = int(duration/2592000)
        mu = 'months'
    elif duration < 63072000:   # 2 years
        dur = 1
        mu = 'year'
    elif duration < 3122064000: # 99 years
        dur = int(duration/31536000)
        mu = 'years'

    return str(dur) + ' ' + mu

def saturate_color(rgb: (int, int, int)
) -> (int, int, int):
    h, _, l = hsl_from_rgb(float(rgb[0]), float(rgb[1]), float(rgb[2]))

    if l < 50:
        l=50

    return rgb_from_hsl(h, 100, l)

def hsl_from_rgb(
    r: float,
    g: float,
    b: float,
    h_range: int = 360,
    s_range: int = 100,
    l_range: int = 100
) -> (int, int, int):
    import colorsys

    h, l, s = colorsys.rgb_to_hls(r/255,g/255,b/255)

    return int(h*h_range), int(s*s_range), int(l*l_range)

def rgb_from_hsl(
    h: float,
    s: float,
    l: float,
    h_range: int = 360,
    s_range: int = 100,
    l_range: int = 100
) -> (int, int, int):
    import colorsys

    h /= float(h_range)
    s /= float(s_range)
    l /= float(l_range)

    return tuple(round(i * 255.0) for i in colorsys.hls_to_rgb(h,l,s))


# ---------------------------------------------------------------------------------------------------------------------------------------- #