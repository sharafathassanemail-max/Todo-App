from django.shortcuts import render
# Create your views here.

from django.http import JsonResponse #Json format me reponse bhejta hai
from django.views.decorators.csrf import csrf_exempt #CSRF removes token validation - import for API
from django.views.decorators.http import require_http_methods
from .models import Todo
import json


#helper function  for the purpose Cross Origin Request (CORS)


def cors_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response["Access-Control-Allow-Header"] = "Content-Type"
    return response


#get all todos
@csrf_exempt
@require_http_methods(["GET","OPTIONS"])
def get_todos(request):
    if request.method == "OPTIONS":
        return cors_response(JsonResponse({}))
    todos = Todo.objects.all().order_by('created_at')
    data = []
    for todo in todos:
        data.append({
            'id': todo.id,
            'title':todo.title,
            'completed':todo.completed,
            'created_at':todo.created_at.strftime("%Y-%m-%d %H:%M:%S")})

    return cors_response(JsonResponse({'todos':data}, safe=False))

#POST create new todo

@csrf_exempt
@require_http_methods(["POST","OPTIONS"])
def create_todo(request):
    if request.method=="OPTIONS":
        return cors_response(JsonResponse({}))
    
    try:

        data=json.loads(request.body)
        todo = Todo.objects.create(
            title = data['title'],
            completed=False
        )
        return cors_response(JsonResponse({
            'success':True,
            'id':todo.id,

        }))
    except Exception as e:
        return cors_response(JsonResponse({'error':str(e)},status=400)) 


# PUT Todos

@csrf_exempt
@require_http_methods(["PUT","OPTIONS"])
def update_todo(request, todo_id):
    if request.method == "OPTIONS":
        return cors_response(JsonResponse({}))
    
    try:
        todo=Todo.objects.get(id=todo_id)
        data = json.loads(request.body)
        if 'title' in data:
            todo.title = data['title']
        if 'completed' in data:
            todo.completed = data['completed']

        todo.save()
        return cors_response(JsonResponse({'success':True, 'message':'Updated!'}))
    except Todo.DoesNotExist:
        return cors_response(JsonResponse({'error':'Todo not Found'}, status=404))
    

#Delete Todo
@csrf_exempt
@require_http_methods(["DELETE","OPTIONS"])
def delete_todo(request, todo_id):
    if request.method == "OPTIONS":
        return cors_response(JsonResponse({}))
    
    try:
        todo=Todo.objects.get(id=todo_id)
        todo.delete()
        return cors_response(JsonResponse({'success':True,'message':'Deleted!'}))
    except Todo.DoesNotExist:
        return cors_response(JsonResponse({'error':'Todo not Found'}, status=404))