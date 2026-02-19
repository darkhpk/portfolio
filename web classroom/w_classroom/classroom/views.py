from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CodeSession
from .executor import CodeExecutor
import json
import uuid
import logging

# Get logger
logger = logging.getLogger('classroom')


def index(request):
    """Lobby page with list of rooms"""
    # Get active sessions (updated in last 2 hours)
    from django.utils import timezone
    from datetime import timedelta
    cutoff_time = timezone.now() - timedelta(hours=2)
    
    sessions = CodeSession.objects.filter(updated_at__gte=cutoff_time)
    logger.info(f"Lobby accessed - Active rooms: {sessions.count()}")
    
    return render(request, 'classroom/lobby.html', {
        'sessions': sessions
    })


def create_room(request):
    """Create a new room"""
    if request.method == 'POST':
        room_name = request.POST.get('room_name', 'Untitled Room')
        username = request.POST.get('username', 'Anonymous')
        
        # Store username in session
        request.session['username'] = username
        
        # Create new session
        session_id = str(uuid.uuid4())
        CodeSession.objects.create(
            session_id=session_id,
            room_name=room_name,
            creator_username=username,
            code='',
            language='python',
            participant_count=1
        )
        
        logger.info(f"Room created - Name: '{room_name}', Creator: {username}, Session: {session_id}")
        return redirect('classroom', session_id=session_id)
    
    return redirect('index')


def join_room(request, session_id):
    """Join an existing room"""
    if request.method == 'POST':
        username = request.POST.get('username', 'Anonymous')
        request.session['username'] = username
        
        logger.info(f"User {username} joining session {session_id}")
        return redirect('classroom', session_id=session_id)
    
    return redirect('index')


def classroom(request, session_id):
    """Main classroom view with collaborative code editor"""
    username = request.session.get('username', 'Anonymous')
    
    session, created = CodeSession.objects.get_or_create(
        session_id=session_id,
        defaults={'code': '', 'language': 'python', 'room_name': 'Untitled Room', 'creator_username': username}
    )
    
    if created:
        logger.info(f"New session auto-created: {session_id} by {username}")
    else:
        logger.info(f"User {username} accessed existing session {session_id}")
    
    return render(request, 'classroom/classroom.html', {
        'session': session,
        'session_id': session_id,
        'username': username
    })


@csrf_exempt
@require_http_methods(["POST"])
def execute_code(request):
    """Execute code and return output"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        logger.info(f"Code execution requested - Session: {session_id}, Language: {language}, Code length: {len(code)}")
        
        # Update session
        session = get_object_or_404(CodeSession, session_id=session_id)
        session.code = code
        session.language = language
        
        # Execute code
        executor = CodeExecutor()
        output = executor.execute(code, language)
        
        # Save output
        session.output = output
        session.save()
        
        logger.info(f"Code execution completed - Session: {session_id}")
        
        return JsonResponse({
            'success': True,
            'output': output
        })
    except Exception as e:
        logger.error(f"Code execution failed - Session: {session_id}, Error: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'output': f'Error: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def save_code(request):
    """Save code without executing"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        session = get_object_or_404(CodeSession, session_id=session_id)
        session.code = code
        session.language = language
        session.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def get_session_data(request, session_id):
    """Get current session data"""
    try:
        session = get_object_or_404(CodeSession, session_id=session_id)
        return JsonResponse({
            'success': True,
            'code': session.code,
            'output': session.output,
            'language': session.language
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
