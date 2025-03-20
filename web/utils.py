import requests
from django.conf import settings
from django.db import models
from datetime import (
    timedelta,
    timezone
    )

from web.models import (
    Cart,
    Points,
    User,
    ChallengeSubmission,
    )


def send_slack_message(message):
    """Send message to Slack webhook"""
    webhook_url = settings.SLACK_WEBHOOK_URL
    if not webhook_url:
        return False

    try:
        response = requests.post(webhook_url, json={"text": message})
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:.2f}"


def get_or_create_cart(request):
    """Helper function to get or create a cart for both logged in and guest users."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def calculate_user_total_points(user):
    """Calculate total points for a user"""
    return Points.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or 0

def calculate_user_weekly_points(user):
    """Calculate weekly points for a user"""
    one_week_ago = timezone.now() - timedelta(days=7)
    return Points.objects.filter(
        user=user, awarded_at__gte=one_week_ago
    ).aggregate(total=models.Sum('amount'))['total'] or 0

def calculate_user_monthly_points(user):
    """Calculate monthly points for a user"""
    one_month_ago = timezone.now() - timedelta(days=30)
    return Points.objects.filter(
        user=user, awarded_at__gte=one_month_ago
    ).aggregate(total=models.Sum('amount'))['total'] or 0

def get_leaderboard(period=None, limit=10):
    """
    Get leaderboard data based on period (None for all-time, 'weekly', or 'monthly')
    Returns a list of users with their points sorted by total points
    """
    if period == 'weekly':
        time_threshold = timezone.now() - timedelta(days=7)
    elif period == 'monthly':
        time_threshold = timezone.now() - timedelta(days=30)
    else:
        time_threshold = None
    
    users = User.objects.all()
    leaderboard_data = []
    
    for user in users:
        if time_threshold:
            points = Points.objects.filter(
                user=user, awarded_at__gte=time_threshold
            ).aggregate(total=models.Sum('amount'))['total'] or 0
        else:
            points = Points.objects.filter(user=user).aggregate(
                total=models.Sum('amount'))['total'] or 0
        
        if points > 0:  # Only include users with points
            leaderboard_data.append({
                'user': user,
                'points': points,
                'challenge_count': ChallengeSubmission.objects.filter(user=user).count()
            })
    
    # Sort by points (descending)
    leaderboard_data.sort(key=lambda x: x['points'], reverse=True)
    
    return leaderboard_data[:limit]