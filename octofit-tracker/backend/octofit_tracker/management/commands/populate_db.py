from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear all data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users
        tony = User.objects.create(email='tony@stark.com', username='IronMan', team=marvel)
        steve = User.objects.create(email='steve@rogers.com', username='CaptainAmerica', team=marvel)
        bruce = User.objects.create(email='bruce@wayne.com', username='Batman', team=dc)
        clark = User.objects.create(email='clark@kent.com', username='Superman', team=dc)

        # Create Workouts
        run = Workout.objects.create(name='Running', description='5k run', difficulty='Medium')
        lift = Workout.objects.create(name='Weight Lifting', description='Bench press', difficulty='Hard')

        # Create Activities
        Activity.objects.create(user=tony, workout=run, duration_minutes=30, calories_burned=300)
        Activity.objects.create(user=steve, workout=lift, duration_minutes=45, calories_burned=400)
        Activity.objects.create(user=bruce, workout=run, duration_minutes=25, calories_burned=250)
        Activity.objects.create(user=clark, workout=lift, duration_minutes=50, calories_burned=500)

        # Create Leaderboard
        Leaderboard.objects.create(user=tony, team=marvel, score=700, rank=1)
        Leaderboard.objects.create(user=steve, team=marvel, score=400, rank=2)
        Leaderboard.objects.create(user=bruce, team=dc, score=250, rank=2)
        Leaderboard.objects.create(user=clark, team=dc, score=500, rank=1)

        # Create unique index on email for User collection
        with connection.cursor() as cursor:
            cursor.db_conn[User._meta.db_table].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
