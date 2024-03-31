from http import HTTPStatus

from django.test import TestCase


class RobotsTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        self.assertEqual(response.content, b"User-agent: *\nDisallow: /\n")
