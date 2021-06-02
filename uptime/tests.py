from rest_framework.test import APITestCase


class TestReadOnly(APITestCase):
    fixtures = ["initial.json"]

    def test_api_home(self):
        response = self.client.get("/uptime/")
        assert response.status_code == 200
        assert "domains" in response.data
        assert "checks" in response.data

    def test_get_domains(self):
        response = self.client.get("/uptime/domains/")
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_get_checks(self):
        response = self.client.get("/uptime/checks/")
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_filter_checks(self):
        no_filter = self.client.get("/uptime/checks/")
        filtered = self.client.get("/uptime/checks/?domain=2")
        assert len(no_filter.data) > len(filtered.data)


class TestFromAlice(APITestCase):
    fixtures = ["initial.json"]

    def setUp(self):
        self.client.login(username="alice", password="alice")

    def test_creates_and_delete_domain(self):
        before = self.client.get("/uptime/domains/").data
        new_one = self.client.post("/uptime/domains/", {"domain": "archive.org"})
        after = self.client.get("/uptime/domains/").data
        assert len(before) + 1 == len(after)
        self.client.delete(new_one.headers["Location"])
        after_delete = self.client.get("/uptime/domains/").data
        assert len(before) == len(after_delete)

    def test_rename_domain(self):
        new_one = self.client.post("/uptime/domains/", {"domain": "arcive.org"})
        self.client.put(new_one.headers["Location"], {"domain": "archive.org"})
        fixed = self.client.get(new_one.headers["Location"])
        assert fixed.data["domain"] == "archive.org"


class TestPermissions(APITestCase):
    fixtures = ["initial.json"]

    def test_cannot_modify_not_owned_domain(self):
        self.client.login(username="alice", password="alice")
        alice_domain = self.client.post("/uptime/domains/", {"domain": "alice.org"})
        self.client.login(username="bob", password="bob")
        should_fail = self.client.put(
            alice_domain.headers["Location"], {"domain": "stolen"}
        )
        assert should_fail.status_code == 403

    def test_cannot_deleted_not_owned_domain(self):
        self.client.login(username="alice", password="alice")
        alice_domain = self.client.post("/uptime/domains/", {"domain": "keepit.org"})
        self.client.login(username="bob", password="bob")
        should_fail = self.client.delete(alice_domain.headers["Location"])
        assert should_fail.status_code == 403
