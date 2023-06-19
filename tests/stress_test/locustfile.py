from locust import HttpUser, task, between
import random

texts_for_normalization_pairs = [
    ("spotkajmy się za pięć trzecia", "spotkajmy się 02:55"),
    ("w pół do drugiej mam ważne spotkanie", "01:30 mam ważne spotkanie"),
    ("kod do domofonu to pięć sześć zero jeden","kod do domofonu to 5 6 0 1"),
    ("debet na koncie wynosi dwanaście złotych", "debet na koncie wynosi 12 złotych"),
    ("siedemset dwadzieścia trzysta czterdzieści osiem pięćset trzydzieści pięć", "720 348 535"),
]

class PlItnUser(HttpUser):
    # wait_time =  between (0.75,1.25)
    wait_time =  between (0.75,1.25)

    @task
    def normalize_endpoint(self):
        normalization_data_pair = random.choice(texts_for_normalization_pairs)
        
        request_data = {
            "text" : normalization_data_pair[0]
        }
        with self.client.post("/normalize/", json=request_data, catch_response=True) as response:
            try:
                if response.json()["normalized_text"] != normalization_data_pair[1]:
                    response.failure("Got wrong normalized text")
            except:
                response.failure("Error parsing response")