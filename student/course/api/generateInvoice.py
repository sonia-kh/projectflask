import requests
import json
from datetime import datetime

def CREATE_BILL(amount, student_id):
    invoice_details = {
        "amount": float(amount),  # Ensure amount is a float
        "dueDate": datetime.now().strftime('%Y-%m-%d'),
        "type": "TUITION_FEES",
        "account": {
            "studentId": student_id
        }
    }
    print("Submitting data to billing API:", invoice_details)
    endpoint = "http://localhost:8081/invoices/"
    request_headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(endpoint, json=invoice_details, headers=request_headers)
        if response.status_code == 201:
            invoice_data = response.json()
            return {
                "created_successfully": True,
                "invoice_reference": invoice_data.get('reference', None)
            }
        elif response.status_code == 422:
            return {
                "created_successfully": False,
                "student_invalid": True
            }
        else:
            return {
                "created_successfully": False,
            }
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {
            "created_successfully": False,
        }
