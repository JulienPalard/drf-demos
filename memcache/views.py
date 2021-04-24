from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def root(request, memory={}):
    return Response(
        "This is the mem cache entry point, there's nothing here, provide a key in the URL."
    )


@api_view(["GET", "PUT", "DELETE"])
def cache(request, key, memory={}):
    if request.method == "GET":
        return Response(memory.get(key))
    if request.method == "PUT":
        memory[key] = request.data
        return Response(request.data)
    if request.method == "DELETE":
        if key in memory:
            del memory[key]
        return Response()
