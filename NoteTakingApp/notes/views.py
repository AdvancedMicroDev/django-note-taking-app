# from django.shortcuts import render
# from django.core.validators import validate_email
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
from notes.models import Note, NoteUpdate
from notes.serializers import UserSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    authentication_classes = (TokenAuthentication, )


# 1. User Registration: Endpoint: POST /signup
# @csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return JsonResponse({'message': 'User created successfully', 'user': serializer.data})
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. User Login: Endpoint: POST /login
# @csrf_exempt
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)


# 3. Create new note: Endpoint:POST /notes/create
@csrf_exempt # To handle csrf errors
@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Validation: title and content must be provided and must be strings
        if not title or not isinstance(title, str):
            return JsonResponse({'error': 'Invalid title'}, status=status.HTTP_400_BAD_REQUEST)
        if not content or not isinstance(content, str):
            return JsonResponse({'error': 'Invalid content'}, status=status.HTTP_400_BAD_REQUEST)

        # Validation: title must be less than 200 characters -> Just for fun
        if len(title) > 200:
            return JsonResponse({'error': 'Title is too long'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = Note.objects.create(title=title, content=content, owner=request.user)
            return JsonResponse({'message': 'Note created successfully', 'note_id': note.id})
        except Exception as e:
            # Error handling: return a 500 status code and the error message
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 4. Get a note: Endpoint:GET /notes/{id}
@login_required
def get_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Check if the logged-in user is the owner of the note
    if request.user != note.owner:
        return JsonResponse({'error': 'You do not have permission to view this note'}, status=status.HTTP_403_FORBIDDEN)

    return JsonResponse({'title': note.title, 'content': note.content})


# 5. Share a note: Endpoint:POST /notes/share 
@csrf_exempt
@login_required
def share_note(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        usernames = request.POST.get('usernames')
        note = get_object_or_404(Note, id=note_id)

    # Check if logged user is owner of this note
    if request.user != note.owner:
        return JsonResponse({'error': 'You do not permission to share this note'}, status=status.HTTP_403_FORBIDDEN)
    
    for username in usernames:
        user = get_object_or_404(User, username=username)
        note.shared_with.add(user)

    return JsonResponse({'message': 'Note shared successfully!'})


# 6. Update a note: Endpoint:PUT /notes/{id}
@csrf_exempt
@login_required
def update_note(request, note_id):
    if request.method == 'PUT':
        note = get_object_or_404(Note, id=note_id)

        # Check if the logged-in user has access to the note
        if request.user != note.owner and request.user not in note.shared_with.all():
            return JsonResponse({'error': 'You do not have permission to edit this note'}, status=403)

        new_content = request.POST.get('content')

        # Validation: new_content must be provided and must be a string
        if not new_content or not isinstance(new_content, str):
            return JsonResponse({'error': 'Invalid content'}, status=400)

        NoteUpdate.objects.create(note=note, content=new_content)

        return JsonResponse({'message': 'Note updated successfully'})


# 7. Get note version history: Endpoint:GET notes/version-history/{id}
@login_required
def get_note_history(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Check if the logged-in user has access to the note
    if request.user != note.owner and request.user not in note.shared_with.all():
        return JsonResponse({'error': 'You do not have permission to view this note'}, status=403)

    updates = note.updates.order_by('-timestamp').values('content', 'timestamp')
    return JsonResponse(list(updates), safe=False)


# Create your views here.
# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Validate Email
#         try:
#             validate_email(email)
#         except ValidationError:
#             return JsonResponse({'error': 'Invalid Email.'}, status=400)
        
#         # Validate Password
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             return JsonResponse({'error': f'Invalid Password: {e}'}, status=400)

#         # Check that username, email, and password are not None
#         if not username or not email or not password:
#             return JsonResponse({'error': 'Username, email, and password are required'}, status=400)

#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'Username already taken'}, status=400)
        
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({'error': 'Email already exists'}, status=400)
        
#         user = User.objects.create_user(username=username, email=email, password=password)
#         return JsonResponse({'message': 'User Created successfully!', 'user_id': user.id})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

