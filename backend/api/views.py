from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_http_methods
from .models import Todo
import json 


def cors_response(response):
    response["Access-Control-Allow-Origin"]="*"
    response["Access-Control-Allow-Methods"]="GET,POST,PUT,DELETE,PATCH,OP"
    response["Access-Control-Allow-Header"] = "Content-Type"
    return response


@csrf_exempt
@require_http_methods("GET","OPTIONS")
def get_todos(request):
    if request.method == "OPTIONS":
        return cors_response(JsonResponse({}))
    todos = Todo.objects.all().order_by('_created_at')
    data = []
    for todo in todos:
        data.append({
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo._created_at.isoformat("%Y-%m-%dT%H:%M:%S"),
        })
    return cors_response(JsonResponse({'todos': data}, safe=False))
# Post create a new todo

@csrf_exempt
@require_http_methods("POST","OPTIONS")
def create_todo(request):
    if request.method == "OPTIONS":
        return cors_response(JsonResponse({}))
    try:
        data = json.loads(request.body)
        todo = Todo.objects.create(
            title = data["title"],
            completed = False
            )
        return cors_response(JsonResponse({
            "success":True,
            "id":todo id,
    
        }))
    except Exception as e:
        return cors_response(JsonResponse({f"error":str(e)},status=400))
    

        
