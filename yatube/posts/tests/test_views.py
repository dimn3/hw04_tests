from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()

POSTS_PER_PAGE = settings.POSTS_PER_PAGE


class PagesTests(TestCase):
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
            group=cls.group,
            text='haha',
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            'posts/index.html': self.authorized_client.get(
                reverse('posts:index')
            ),
            'posts/group_list.html': self.authorized_client.get(
                reverse('posts:group_list', kwargs={'slug': self.group.slug})
            ),
            'posts/profile.html': (
                self.authorized_client.get(
                    reverse(
                        'posts:profile',
                        kwargs={
                            'username': self.author.username
                        }
                    )
                )
            ),
            'posts/post_detail.html': self.authorized_client.get(
                reverse('posts:post_detail', kwargs={'post_id': self.post.id})
            ),
            'posts/create_post.html': self.authorized_client.get(
                reverse('posts:post_create')
            ),
        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                self.assertTemplateUsed(reverse_name, template)

    def test_edit_view(self):
        template = 'posts/create_post.html'
        reverse_name = self.author_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        with self.subTest(template=template):
            self.assertTemplateUsed(reverse_name, template)

    def test_post_correct_group_(self):
        self.assertEqual(self.post.group, self.group)

    def test_view_group_list_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            )
        )
        self.assertEqual(response.context['group'], self.group)

    def test_view_profile_context(self):
        counter = Post.objects.filter(author=self.author).count()
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            )
        )
        self.assertEqual(response.context['counter'], counter)
        self.assertEqual(response.context['author'], self.author)

    def test_view_post_detail(self):
        counter = Post.objects.filter(author=self.author).count()
        response_post = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        response_counter = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(response_post.context['post'], self.post)
        self.assertEqual(response_counter.context['counter'], counter)
        self.assertEqual(response_post.context['post'].group, self.group)
        self.assertEqual(
            response_post.context['post'].text, self.post.text
        )
        self.assertEqual(response_post.context['post'].author, self.author)


class PaginatorViewsTest(TestCase):
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
            title='test_title',
            slug='test_slug',
            description='desc'
        )
        cls.post_list = []
        for i in range(1, 14):
            post_save = Post(
                id=i,
                author=cls.user,
                text=f'№ {i}',
                group=cls.group
            )
            cls.post_list.append(post_save)
        Post.objects.bulk_create(cls.post_list)

    def test_first_page_contains_ten_records(self):
        response = self.guest_client.get(reverse('posts:index'))
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context['page_obj']), POSTS_PER_PAGE)

    def test_second_page_contains_three_records(self):
        # Проверка: на второй странице должно быть четыре поста.
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(
            len(response.context['page_obj']),
            len(self.post_list) % POSTS_PER_PAGE
        )
