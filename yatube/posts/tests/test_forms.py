from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем запись в базе данных для проверки сушествующего slug
        cls.author = User.objects.create_user(
            username='avtor',
            first_name='valerka',
            last_name='ivanich',
        )
        cls.group = Group.objects.create(
            title='asd',
            slug='1',
            description='dsa',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text='haha',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_postform(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'testtext',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile', kwargs={'username': self.author}
            )
        )
        post_created = Post.objects.order_by('-pub_date').first()
        self.assertEqual(posts_count + 1, Post.objects.count())
        self.assertEqual(post_created.text, 'testtext')
        self.assertEqual(post_created.id, self.post.id + 1)

    def test_edit_post(self):
        post_for_edit = Post.objects.create(
            author=self.author,
            text='textforedit',
        )
        form_data = {
            'text': 'editedtext',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_for_edit.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': post_for_edit.id}
            )
        )
        edited_post = Post.objects.get(id=post_for_edit.id)
        self.assertEqual(edited_post.text, 'editedtext')

    def test_create_post_for_unlog_user(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'testcreate',
            'group': self.group.id
        }
        response = Client().post(
            reverse('posts:post_create'),
            data=form_data,
        )
        self.assertRedirects(
            response, '/auth/login/?next=/create/')
        self.assertEqual(posts_count, Post.objects.count())
