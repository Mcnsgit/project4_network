from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from network.models import Post, Comment
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for the social network'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--posts', type=int, default=50, help='Number of posts to create')
        parser.add_argument('--comments', type=int, default=100, help='Number of comments to create')

    def handle(self, *args, **options):
        num_users = options['users']
        num_posts = options['posts']
        num_comments = options['comments']

        # Create users
        self.stdout.write('Creating users...')
        users = []
        for i in range(num_users):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='testpass123'
            )
            user.bio = fake.text(max_nb_chars=200)
            user.location = fake.city()
            user.birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
            user.save()
            users.append(user)
            self.stdout.write(f'Created user: {username}')

        # Create follow relationships
        self.stdout.write('Creating follow relationships...')
        for user in users:
            # Each user follows 1-5 random users
            num_to_follow = random.randint(1, 5)
            potential_follows = [u for u in users if u != user]
            if potential_follows:
                follows = random.sample(potential_follows, min(num_to_follow, len(potential_follows)))
                for follow in follows:
                    user.following.add(follow)

        # Create posts
        self.stdout.write('Creating posts...')
        posts = []
        for _ in range(num_posts):
            user = random.choice(users)
            post = Post.objects.create(
                user=user,
                title=fake.sentence(),
                content=fake.paragraph(),
                created_at=fake.date_time_between(start_date='-30d', end_date='now'),
            )
            # Add random likes to posts
            num_likes = random.randint(0, len(users))
            likers = random.sample(users, num_likes)
            post.likes.set(likers)
            posts.append(post)

        # Create comments
        self.stdout.write('Creating comments...')
        for _ in range(num_comments):
            post = random.choice(posts)
            user = random.choice(users)
            comment = Comment.objects.create(
                post=post,
                name=user,
                body=fake.text(max_nb_chars=200),
                date_added=fake.date_time_between(
                    start_date=post.created_at,
                    end_date=datetime.now()
                )
            )
            # Add random likes to comments
            num_likes = random.randint(0, len(users) // 2)
            likers = random.sample(users, num_likes)
            comment.likes.set(likers)

        self.stdout.write(self.style.SUCCESS(f'''
Successfully created:
- {num_users} users
- {num_posts} posts
- {num_comments} comments
'''))
