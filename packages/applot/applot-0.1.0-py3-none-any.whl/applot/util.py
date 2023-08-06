
def make_scale(dmin,dmax,rmin,rmax):
    dextent = dmax - dmin
    rextent = rmax - rmin
    sfactor = rextent / dextent
    def scale(n):
        return (n - dmin) * sfactor + rmin
    return scale

def extent(iterable):
    lo = hi = None
    for v in iterable:
        if lo is None and hi is None:
            lo = hi = v
        elif v < lo:
            lo = v
        elif v > hi:
            hi = v
    return lo, hi

def arange(start,stop=None,step=1,clean=True):
    if step == 0: 
        raise ValueError("Can't have step of 0")
    if stop is None:
        start, stop = 0, start
    up = start < stop
    if up and step < 0:
        raise ValueError("Can't have negative step and start < stop.")
    if up and step < 0:
        raise ValueError("Can't have positive step and start > stop.")
    arr = []
    n = start
    while (n < stop and up) or (n > stop and not up):
        if clean: n = round(n,12)
        arr.append(n)
        n += step
    return arr 
    

def linspace(start,stop=None,n=10):
    step = (stop - start) / (n - 1)
    return [start+step*i for i in range(n)]
