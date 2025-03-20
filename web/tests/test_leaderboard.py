from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from web.models import Points, Challenge, ChallengeSubmission

class LeaderboardTestCase(TestCase):
    def setUp(self):
        # This runs before each test
        self.client = Client()
        
        # Create test users within the test database
        self.test_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="testpass123"
        )
        
        # Create a second user for testing
        self.test_user2 = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="testpass123"
        )
        
        # Create test challenges
        self.challenge = Challenge.objects.create(
            title="Test Challenge",
            description="Test Description",
            week_number=1,
            start_date="2025-03-01",
            end_date="2025-03-07"
        )
        
        # Create a submission and points
        self.submission = ChallengeSubmission.objects.create(
            user=self.test_user,
            challenge=self.challenge,
            submission_text="Test submission",
            points_awarded=10
        )
        
        # Add some extra points
        Points.objects.create(
            user=self.test_user,
            amount=15,
            reason="Test points",
            point_type="regular"
        )
        
    def test_with_force_login(self):
        # Use the user we created in setUp
        self.client.force_login(self.test_user)
        
        # Using reverse() to get the URL by name is better
        # If you don't know the name, you can find it by running:
        # python manage.py show_urls
        try:
            profile_url = reverse('user_profile')  # Try common URL names
        except:
            profile_url = '/accounts/profile/'  # Fallback to a common path
        
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        
    def test_leaderboard_access(self):
        self.client.force_login(self.test_user)
        
        # Try common URL names for leaderboard
        try:
            leaderboard_url = reverse('leaderboard_main')  # Try common URL names
        except:
            leaderboard_url = '/en/leaderboards/'  # Note: plural form
        
        response = self.client.get(leaderboard_url)
        self.assertEqual(response.status_code, 200)
        
        # Check for leaderboard content
        self.assertContains(response, self.test_user.username)