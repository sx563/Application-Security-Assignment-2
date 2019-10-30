import unittest
from app import *

class TestCasesFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_path(self):
        post_result = self.app.get("/", follow_redirects=True)
        self.assertEqual(post_result.status_code, 200)
        self.assertIn(b"Register", post_result.data)
    
    def test_register_path(self):
        post_result = self.app.get("/register")
        self.assertEqual(post_result.status_code, 200)
        self.assertIn(b"Register", post_result.data)

    def test_login_path(self):
        post_result = self.app.get("/login")
        self.assertEqual(post_result.status_code, 200)
        self.assertIn(b"Login", post_result.data)
    
    def test_spell_check_path(self):
        post_result = self.app.get("/spell_check", follow_redirects=True)
        self.assertEqual(post_result.status_code, 200)
        self.assertIn(b"Login", post_result.data)

    def test_register(self):
        data = {
            "uname": "john",
            "pword": "testpassword",
            "2fa": "00000000000"
        }
        post_result = self.app.post("/register", data=data)
        self.assertIn(b"Success: Account registered", post_result.data)

        post_result2 = self.app.post("/register", data=data)
        self.assertIn(b"Failure: Username already registered", post_result2.data)


    def register_user(self):
        data = {
            "uname": "jack",
            "pword": "testpassword",
            "2fa": "00000000000"
        }
        post_result = self.app.post("/register", data=data)

    def test_login_valid_credentials(self):
        self.register_user()
        data = {
            "uname": "jack",
            "pword": "testpassword",
            "2fa": "00000000000"
        }

        post_result = self.app.post("/login", data=data, follow_redirects=True)
        self.assertIn(b"Spell Check", post_result.data)
        self.assertIn(b"Success: User logged in", post_result.data)


    def test_login_invalid_credentials(self):
        self.register_user()
        data = {
            "uname": "jack",
            "pword": "testpassword",
            "2fa": "00000000000"
        }

        original_pword = data["pword"]
        data["pword"] = "wrongpassword"

        post_result2 = self.app.post("/login", data=data)
        self.assertIn(b"Failure: Incorrect password", post_result2.data)

        data["pword"] = original_pword
        data["2fa"] = "1-111-111-1111"
        post_result3 = self.app.post("/login", data=data)
        self.assertIn(b"Failure: Incorrect Two-factor", post_result3.data)

        data["uname"] = "notjack"
        post_result3 = self.app.post("/login", data=data)
        self.assertIn(b"Failure: Incorrect username", post_result3.data)

    def test_empty_fields(self):
        data = {
            "uname": "",
            "pword": "",
            "2fa": ""
        }

        post_result = self.app.post("/register", data=data)
        self.assertIn(b"Failure: Empty Field(s)", post_result.data)

        post_result2 = self.app.post("/login", data=data)
        self.assertIn(b"Failure: Empty Field(s)", post_result2.data)

    def logged_in_user(self):
        self.register_user()
        data = {
            "uname": "jack",
            "pword": "testpassword",
            "2fa": "00000000000"
        }
        post_result = self.app.post("/login", data=data, follow_redirects=True)



    def test_spell_check(self):
        self.logged_in_user()
        post_result = self.app.get("/spell_check")
        self.assertIn(b"Spell Check", post_result.data)

        data = {
            "inputtext": "justice just!ice jus!tice"
        }
        post_result2 = self.app.post("/spell_check", data=data, follow_redirects=True)
        self.assertIn(b"justice just!ice jus!tice", post_result2.data)
        self.assertIn(b"just!ice, jus!tice", post_result2.data)


        

if __name__ == '__main__':
    unittest.main()
