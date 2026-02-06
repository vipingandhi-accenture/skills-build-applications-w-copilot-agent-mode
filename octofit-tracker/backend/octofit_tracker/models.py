from djongo import models

class Team(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	def __str__(self):
		return self.name

class User(models.Model):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=100)
	team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='members')
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return self.email

class Workout(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	difficulty = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Activity(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
	workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='activities')
	date = models.DateTimeField(auto_now_add=True)
	duration_minutes = models.PositiveIntegerField()
	calories_burned = models.PositiveIntegerField()
	def __str__(self):
		return f"{self.user.email} - {self.workout.name} on {self.date}"

class Leaderboard(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
	team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboard_entries')
	score = models.IntegerField(default=0)
	rank = models.PositiveIntegerField(default=0)
	def __str__(self):
		return f"{self.user.email} - {self.score}"
