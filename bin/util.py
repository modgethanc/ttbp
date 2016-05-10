#!/usr/bin/python

import inflect
import time

p = inflect.engine()

def pretty_time(time):
    m, s = divmod(time, 60)
    if m > 0:
        h, m = divmod(m, 60)
        if h > 0:
            d, h = divmod(h, 24)
            if d > 0:
                w, d = divmod(d, 7)
                if w > 0:
                    mo, w = divmod(w, 4)
                    if mo > 0:
                        return p.no("month", mo)
                    else:
                        return p.no("week", w)
                else:
                    return p.no("day", d)
            else:
                return p.no("hour", h)
        else:
            return p.no("minute", m)
    else:
        return p.no("second", s)
