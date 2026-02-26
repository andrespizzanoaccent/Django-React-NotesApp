from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note, Category
from .serializers import NoteSerializer, CategorySerializer
from .utils import updateNote, getNoteDetail, deleteNote, getNotesList, createNote


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
        {
            'Endpoint': '/categories/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of categories'
        },
        {
            'Endpoint': '/categories/create/',
            'method': 'POST',
            'body': {'name': "", 'metadata': {}},
            'description': 'Creates new category with data sent in post request'
        },
        {
            'Endpoint': '/categories/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single category object'
        },
        {
            'Endpoint': '/categories/id/update/',
            'method': 'PUT',
            'body': {'name': "", 'metadata': {}},
            'description': 'Updates an existing category with data sent in post request'
        },
        {
            'Endpoint': '/categories/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an existing category'
        },
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def getNotes(request):
    if request.method == 'GET':
        return getNotesList(request)

    if request.method == 'POST':
        return createNote(request)


@api_view(['GET', 'PUT', 'DELETE'])
def getNote(request, pk):
    if request.method == 'GET':
        return getNoteDetail(request, pk)

    if request.method == 'PUT':
        return updateNote(request, pk)

    if request.method == 'DELETE':
        return deleteNote(request, pk)


@api_view(['GET', 'POST'])
def manageCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def manageCategory(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'})
