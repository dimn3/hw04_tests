from django.test import Client, TestCase


class StaticPagesURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/author/ и /about/tech/."""
        addresses = {
            '/about/author/',
            '/about/tech/'
        }
        for address in addresses:
            with self.subTest(address=address):
                status_code = self.guest_client.get(address).status_code
                self.assertEqual(status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /about/author/ и /about/tech/."""
        responses_templates = {
            self.guest_client.get('/about/author/'): 'about/author.html',
            self.guest_client.get('/about/tech/'): 'about/tech.html'
        }

        for response, template in responses_templates.items():

            with self.subTest(response=response):
                self.assertTemplateUsed(response, template)
