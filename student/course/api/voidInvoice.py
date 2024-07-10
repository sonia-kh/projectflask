import requests

def VOID_INVOICE(invoice_ref):
    api_url = f"http://localhost:8081/invoices/{invoice_ref}/cancel"
    request_headers = {
        "Content-Type": "application/json"
    }

    try:
        result = requests.delete(api_url, headers=request_headers)
        print("HTTP status code received:", result.status_code)
        print("API response content:", result.content.decode('utf-8'))

        if result.status_code == 200:
            return {
                "cancellation_successful": True,
                "feedback": f"Invoice {invoice_ref} successfully voided."
            }
        elif result.status_code == 404:
            return {
                "cancellation_successful": False,
                "feedback": f"Invoice {invoice_ref} not located."
            }
        elif result.status_code == 422:
            return {
                "cancellation_successful": False,
                "feedback": f"Invoice {invoice_ref} cannot be voided due to invalid state."
            }
        else:
            return {
                "cancellation_successful": False,
                "feedback": f"Unable to void invoice {invoice_ref}. It might already be paid."
            }
    except requests.RequestException as error:
        print(f"Exception encountered: {error}")
        return {
            "cancellation_successful": False,
            "feedback": f"Exception encountered: {error}"
        }
