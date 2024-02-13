from locust import HttpUser, TaskSet, task

class User(HttpUser):
    host = "http://localhost:30070"

    @task
    def index(self):
        self.client.get("/")
