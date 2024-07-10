import requests

def fetch_student_graduation_status(student_id):
    url = f"http://localhost:8081/accounts/student/{student_id}"
    
    try:
        response = requests.get(url)
        print(response.json())
        if response.status_code == 200:
            account_info = response.json()
            return {
                'account_exists': True,
                'has_outstanding_balance': account_info.get('hasOutstandingBalance', False),
                'graduation_eligibility': account_info.get('eligibleForGraduation', False),
                'error': False
            }
        elif response.status_code == 404:
            return {'account_exists': False, 'error': True}
        else:
            return {'error': "Something Went Wrong!"}
    except requests.RequestException as e:
        return {'error': "Unable to Send Request. Please ensure Finance Module is Running"}
