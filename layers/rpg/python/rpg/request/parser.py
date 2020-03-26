parse_headers = lambda h: dict(map(
    lambda k, v: [k.lower(), v],
    h.keys(), h.values()
))