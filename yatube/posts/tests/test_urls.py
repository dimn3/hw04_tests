from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.author = User.objects.create_user(
            username='avtor',
            first_name='valerka',
            last_name='ivanich',
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='asd',
            slug='1',
            description='dsa',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='haha',
            id=1
        )
        cls.url_edit = reverse(
            'posts:post_edit',
            kwargs={
                'post_id': cls.post.id,
            }
        )

    # Проверяем общедоступные страницы
    def test_urls_for_unauth_users(self):
        """Страницы, доступные любому пользователю."""

        addresses = {
            self.guest_client.get('/'),
            self.guest_client.get('/group/1/'),
            self.guest_client.get('/profile/HasNoName/'),
            self.guest_client.get('/posts/1/'),
        }
        for address in addresses:
            with self.subTest(address=address):
                status_code = address.status_code
                self.assertEqual(status_code, 200)

    # Проверяем,что вернется ошибка 404
    def test_unreal_url(self):
        """Ошибка 404"""
        status_code = self.guest_client.get('/hahahehehoho/').status_code
        self.assertEqual(status_code, 404)

    # Проверяем,что страница create доступна авторизованному
    def test_create_page(self):
        """Create для авторизованного"""
        response = self.authorized_client.get('/create/')
        status = response.status_code
        self.assertEqual(status, 200)

    # Проверяем,что страница edit доступна автору
    def test_edit_page(self):
        """edit для автора"""
        response = self.author_client.get(self.url_edit)
        self.assertEqual(response.status_code, 200)

    def test_templates_for_urls(self):
        """Шаблоны"""
        url_template = {
            self.guest_client.get('/'): 'posts/index.html',
            self.guest_client.get('/group/1/'): 'posts/group_list.html',
            self.guest_client.get('/profile/HasNoName/'): 'posts/profile.html',
            self.guest_client.get('/posts/1/'): 'posts/post_detail.html',
            self.author_client.get(self.url_edit): 'posts/create_post.html',
            self.authorized_client.get('/create/'): 'posts/create_post.html',
        }
        for url, template in url_template.items():
            with self.subTest(template=template):
                self.assertTemplateUsed(url, template)
