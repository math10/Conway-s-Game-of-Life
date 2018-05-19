from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conway_game_of_life.models import Grid
from conway_game_of_life.serializers import GridSerializer
from rest_framework.decorators import api_view
# Create your views here.
@csrf_exempt
def GridList(request):
    if request.method == 'GET':
        grids = Grid.objects.all()
        serializer = GridSerializer(grids, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GridSerializer(data=data)
        if serializer.is_valid() and data['x']*data['y'] == len(data['data']):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def GridDetail(request, pk):
    try:
        grid = Grid.objects.get(pk=pk)
    except Grid.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GridSerializer(grid)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GridSerializer(grid, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def GridAfter(request, pk):
    if request.method == 'GET':
        try:
            grid = Grid.objects.get(pk=pk)
        except Grid.DoesNotExist:
            return HttpResponse(status=404)
        
        query = request.GET.get('after')
        if query == None:
            return HttpResponse(status=400)
        else:
            query = query.split(',')
            for i in range(len(query)):
                try:
                    query[i] = int(query[i])
                    if query[i] < 0:
                        return HttpResponse(status=400)
                except Exception:
                    return HttpResponse(status=400)
            sorted(query)
            result = []
            last = []
            l = grid.x * grid.y
            i = 0
            while i < l:
                row = grid.data[i:i+grid.y]
                i += grid.y 
                last.append(row)
            age = 0
            point = 0
            length = len(query)
            max_age = query[length-1]
            while age < max_age:
                while point < length and age == query[point]:
                    result.append(''.join(last))
                    point += 1
                nxt = list(last)
                dx = [1,1,0,-1,-1,-1,0,1]
                dy = [0,1,1,1,0,-1,-1,-1]
                for i in range(grid.x):
                    nxt[i] = list(nxt[i])
                    last[i] = list(last[i])
                    for j in range(grid.y):
                        totalPopulation = 0
                        for k in range(8):
                            x = i + dx[k]
                            y = j + dy[k]
                            if x >= 0 and x < grid.x and y >= 0 and y < grid.y and last[x][y] == 'x':
                                totalPopulation += 1
                        if last[i][j] == 'x':
                            if totalPopulation >= 2 and totalPopulation <= 3:
                                nxt[i][j] = 'x'
                            else:
                                nxt[i][j] = 'o'
                        else:
                            if totalPopulation == 3:
                                nxt[i][j] = 'x'
                            else:
                                nxt[i][j] = 'o'
                    nxt[i] = ''.join(nxt[i])
                age += 1
                last = list(nxt)
            while point < length and age == query[point]:
                result.append(''.join(last))
                point += 1
            response = {'id': grid.id, 'x': grid.x, 'y': grid.y, 'data': []}
            ages = []
            for i in range(length):
                age = {'age': query[i], 'grid': result[i]}
                ages.append(age)
            response['data'] = ages
        return JsonResponse(response)