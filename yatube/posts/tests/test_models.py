from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        text_must_be = PostModelTest.post.text[:15]
        text_str = PostModelTest.post.__str__()
        title_must_be = PostModelTest.group.title
        title_str = PostModelTest.group.__str__()
        self.assertEqual(
            text_must_be, text_str,
            '__str__ у текста поста работает некорректно'
        )
        self.assertEqual(
            title_must_be, title_str, '__str__ у групп работает некорректно'
        )

    def test_models_post_verbose_name(self):
        """Проверяем verbose_name модели Post"""
        post = PostModelTest.post
        verbose_text = post._meta.get_field('text').verbose_name
        verbose_text_must = 'Текст поста'
        verbose_pubdate = post._meta.get_field('pub_date').verbose_name
        verbose_pubdate_must = 'Дата публикации'
        verbose_author = post._meta.get_field('author').verbose_name
        verbose_author_must = 'Автор'
        verbose_group = post._meta.get_field('group').verbose_name
        verbose_group_must = 'Группа'
        self.assertEqual(
            verbose_text, verbose_text_must, 'text verbose error'
        )
        self.assertEqual(
            verbose_pubdate, verbose_pubdate_must, 'pubdate verbose error'
        )
        self.assertEqual(
            verbose_author, verbose_author_must, 'author verbose error'
        )
        self.assertEqual(
            verbose_group, verbose_group_must, 'group verbose error'
        )

    def test_models_post_help_text(self):
        """Проверяем verbose_name модели Post"""
        post = PostModelTest.post
        help_text_post = post._meta.get_field('text').help_text
        help_text_post_must = 'Введите текст поста'
        help_text_group = post._meta.get_field('group').help_text
        help_text_group_must = 'Группа, к которой будет относиться пост'
        self.assertEqual(
            help_text_post, help_text_post_must, 'text verbose error'
        )
        self.assertEqual(
            help_text_group, help_text_group_must, 'group verbose error'
        )
