from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import cloudinary.uploader
from .utils import extract_text_from_pdf, analyze_resume_with_ai, match_resume_with_jd
from .models import Resume, Analysis

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'User created successfully',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    
    return Response({'error': 'Invalid credentials'}, 
                   status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resume(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No File Provided'},
            status= status.HTTP_400_BAD_REQUEST
         )
    file = request.FILES['file']

    if not file.name.endswith('.pdf'):
        return Response(
            {'error': 'Only Pdf File Allowed'},
            status= status.HTTP_400_BAD_REQUEST
         )
    

    raw_text = extract_text_from_pdf(file)
    file.seek(0)

    upload_result = cloudinary.uploader.upload(
        file,
        resource_type='raw',
        folder='resumes'
    )

    # saving in database

    resume = Resume.objects.create(
        user= request.user,
        file_name= file.name,
        file_url= upload_result['secure_url'],
        raw_text= raw_text
    )


    # returning response that data is successfully added or not 
    return Response({
        'id': resume.id,
        'file_name': resume.file_name,
        'file_url': resume.file_url,
        'text_extracted': len(raw_text)>0,
        'message': 'Resume Uploaded Successfully'
    }, status=status.HTTP_201_CREATED)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_resume(request, resume_id):
    
    # Resume dhundo — agar nahi mila toh 404
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
    except Resume.DoesNotExist:
        return Response(
            {'error': 'Resume not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Agar text nahi nikla PDF se
    if not resume.raw_text:
        return Response(
            {'error': 'No text found in resume'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # AI se analysis lo
    result = analyze_resume_with_ai(resume.raw_text)
    
    # Database mein save karo
    analysis, created = Analysis.objects.get_or_create(resume=resume)
    analysis.overall_score = result.get('overall_score', 0)
    analysis.ats_score = result.get('ats_score', 0)
    analysis.skills_found = result.get('skills_found', [])
    analysis.skills_missing = result.get('skills_missing', [])
    analysis.experience_check = result.get('experience_check', '')
    analysis.suggestions = result.get('suggestions', [])
    analysis.is_complete = True
    analysis.save()
    
    return Response({
        'resume_id': resume.id,
        'overall_score': analysis.overall_score,
        'ats_score': analysis.ats_score,
        'skills_found': analysis.skills_found,
        'skills_missing': analysis.skills_missing,
        'experience_check': analysis.experience_check,
        'suggestions': analysis.suggestions,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    
    # Sirf is user ki resumes lo — last 10
    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-uploaded_at')[:10]
    
    history = []
    
    for resume in resumes:
        item = {
            'id': resume.id,
            'file_name': resume.file_name,
            'file_url': resume.file_url,
            'uploaded_at': resume.uploaded_at,
            'analysis': None
        }
        
        # Agar analysis ho gayi hai toh woh bhi add karo
        try:
            analysis = resume.analysis
            if analysis.is_complete:
                item['analysis'] = {
                    'overall_score': analysis.overall_score,
                    'ats_score': analysis.ats_score,
                    'skills_found': analysis.skills_found,
                    'skills_missing': analysis.skills_missing,
                    'suggestions': analysis.suggestions,
                }
        except Analysis.DoesNotExist:
            pass
        
        history.append(item)
    
    return Response(history, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def match_with_jd(request, resume_id):
    
    # Job description lo request se
    job_description = request.data.get('job_description')
    
    if not job_description:
        return Response(
            {'error': 'Job description is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Resume dhundo
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
    except Resume.DoesNotExist:
        return Response(
            {'error': 'Resume not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # AI se match karo
    result = match_resume_with_jd(resume.raw_text, job_description)
    
    return Response({
        'resume_id': resume.id,
        'match_percentage': result.get('match_percentage', 0),
        'matching_keywords': result.get('matching_keywords', []),
        'missing_keywords': result.get('missing_keywords', []),
        'strong_points': result.get('strong_points', []),
        'weak_points': result.get('weak_points', []),
        'recommendation': result.get('recommendation', ''),
    }, status=status.HTTP_200_OK)