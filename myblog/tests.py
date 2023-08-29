from django.test import TestCase
from django.urls import reverse
from .models import Post, CustomCommentForm


class BlogTests(TestCase):
    def setUp(self):
        self.published_post = Post.objects.create(
            post_title="Test Post",
            post_author="Test Author",
            post_slug="test-post",
            post_body="This is a test post body.",
            post_publish_date="2023-08-29 12:00:00",
            post_create_date="2023-08-29 12:00:00",
            post_update_date="2023-08-29 12:00:00",
            post_status="Published"
        )


    def test_one_post_view(self):
        response = self.client.get(reverse('one_post', args=[self.published_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            post_title="Test Post",
            post_author="Test Author",
            post_slug="test-post",
            post_body="This is a test post body.",
            post_publish_date="2023-08-29 12:00:00",
            post_create_date="2023-08-29 12:00:00",
            post_update_date="2023-08-29 12:00:00",
            post_status="Published"
        )

    def test_post_creation(self):
        self.assertEqual(str(self.post), "Test Post")
        self.assertEqual(self.post.post_status, "Published")
class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@gmail.com',
            'body': 'This is a test comment.'
        }
        form = CustomCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {
            'name': '',
            'email': 'test@gmail.com',
            'body': 'This is a test comment.'
        }
        form = CustomCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
class UrlsAndViewsTest(TestCase):
    def test_post_list_url(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myblog/post_list.html')


    def test_nonexistent_post_url(self):
        # Test accessing a non-existent post
        response = self.client.get(reverse('one_post', args=[999]))
        self.assertEqual(response.status_code, 404)