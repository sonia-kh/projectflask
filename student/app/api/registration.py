import http.client
import json
import requests



def REGISTER_in_LIBRARY(student_id):
    try:
        api_url = "http://localhost/api/register"
        data_payload = {
            "studentId": student_id
        }
        headers_info = {
            'Content-Type': 'application/json'
        }

        response = requests.post(api_url, json=data_payload, headers=headers_info)

        if response.status_code == 200:
            return True
        else:
            print(f"Library account registration failed. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as error:
        print(f"An error occurred during library account registration: {error}")
        return False


import http.client
import json

def REGISTER_in_FINANCIAL(student_id):
    try:
        
        conn = http.client.HTTPConnection("localhost", 8081)
        payload_data = json.dumps({
            "studentId": student_id
        })
        headers_info = {
            'Content-Type': 'application/json'
        }
        
        # Make the request
        conn.request("POST", "/accounts/", payload_data, headers_info)
        response = conn.getresponse()

        # Check the response status
        if response.status == 201:
            return True
        else:
            print(f"Finance account registration failed. Status code: {response.status}")
            return False
    except Exception as e:
        print(f"An error occurred during financial profile registration: {e}")
        return False
