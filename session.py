import requests
import time
import os
from pathlib import Path
from dotenv import load_dotenv
import base64
from pprint import pprint
import json


class SpeaklishClient:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        load_dotenv(self.base_dir / '.env')
        self.url_base = "https://api.speaklish.uz/school/"
        self.headers = self._get_headers()

    def _get_headers(self):
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        auth_str = f'{username}:{password}'.encode('utf-8')
        auth_b64 = base64.b64encode(auth_str).decode('utf-8')
        return {'Authorization': f'Basic {auth_b64}'}

    def _request(self, method, endpoint, payload=None, files=None):
        url = self.url_base + endpoint
        response = requests.request(method, url, headers=self.headers, data=payload, files=files)
        response.raise_for_status()
        return response.json()

    def create_session(self):
        endpoint = "session-create?is_test=true&user_id=7777" # by your wish
        return self._request("GET", endpoint)

    def send_part_answers(self, endpoint, questions):
        for question in questions:
            qs_id = question.get('id')
            audio_file = self.base_dir / 'media' / 'tests' / f'audio_{endpoint}_{qs_id}.ogg'
            assert audio_file.exists()
            files = {'voice_audio': open(audio_file, 'rb')}
            payload = {'question_id': qs_id, 'session_id': self.session_id}
            response = self._request("POST", endpoint, payload, files)
            print('qs_id', qs_id, response)

    def wait_for_feedback(self):
        url = f"{self.url_base}session-feedback/{self.session_id}"
        response = self._request("GET", url)


        while response.status_code != 200:
            response = self._request("GET", url)
            pprint(response)
            time.sleep(10)
        
        with open(f'result_{self.session_id}.json', 'w') as f:
            
            f.write(
                json.dumps(response, indent=4, ensure_ascii=False)
            )
            f.close()

    def run_test(self):
        test_session = self.create_session()
        self.session_id = test_session['session_id']

        self.send_part_answers("part-1-create/", test_session['part1_questions'])
        self.send_part_answers("part-3-create/", test_session['part3_questions'])

        part2_question = test_session['part2_question']
        qs_id = part2_question['id']
        audio_file = self.base_dir / 'media' / 'tests' / 'part_2_test.ogg'
        assert audio_file.exists()
        files = {'voice_audio': open(audio_file, 'rb')}
        payload = {'question_id': qs_id, 'session_id': self.session_id}
        response = self._request("POST", "part-2-create/", payload, files)
        print('qs_id', qs_id, response)

        print('waiting for feedback for 30 seconds...')
        self.wait_for_feedback(session_id)

if __name__ == "__main__":
    client = SpeaklishClient()
    client.run_test()
