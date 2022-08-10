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
            id=1
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    # Создаем автора,который делает пост и группу
    def test_create_postform(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'testtext',
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
        self.assertEqual(posts_count + 1, Post.objects.count())
        self.assertTrue(
            Post.objects.filter(
                text='testtext',
            ).exists()
        )

    def test_edit_post(self):
        form_data = {
            'text': 'editedtext',
        }
        response2 = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response2, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            )
        )
        self.assertTrue(
            Post.objects.filter(
                id=self.post.id,
                text='editedtext',
            ).exists()
        )
