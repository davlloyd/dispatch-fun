def handle(ctx, payload):
    name = "Noon"
    place = "Nowhere"
    if payload:
        name = payload.get("name", name)
        place = payload.get("place", place)
    return {"myField": "Hello, %s from %s" % (name, place)}

