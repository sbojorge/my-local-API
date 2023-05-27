from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='sara', password='pass')

    def test_can_list_posts(self):
        sara = User.objects.get(username='sara')
        Post.objects.create(owner=sara, title = 'a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='sara', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        sara = User.objects.create_user(username='sara', password='pass')
        gati = User.objects.create_user(username='gati', password='tamm')
        Post.objects.create(
            owner=sara, title='a title', content='some content'
        )
        Post.objects.create(
            owner=gati, title='another title', content='some other content'
        )

    def test_can_retrieve_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cannot_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_can_update_own_post(self):
        self.client.login(username='sara', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cannot_update_others_post(self):
        self.client.login(username='sara', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a pretty title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
