from .test_setup import TestSetup


class TestAuthViews(TestSetup):

    def test_user_cannot_register_without_post_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_register(self):
        # import ipdb;ipdb.set_trace()
        res = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_incorrect_creds(self):
        res = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(res.status_code, 200)
