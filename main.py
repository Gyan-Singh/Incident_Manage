
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


import requests
from requests.auth import HTTPBasicAuth

# Set up your ServiceNow credentials and base URL
BASE_URL = 'https://instance.service-now.com/api/now/table/incident'
USERNAME = 'admin'
PASSWORD = 'pass'






@app.route('/')
def customer():
    return render_template('index.html')

@app.route('/success', methods=['POST', 'GET'])

def print_data():
    if request.method == 'POST':
        result1 = {}
        result = request.form
        short_description = result['sd']
        urgency=result['priority']
    # urgency = urgency_var.get()
    
    # Create a dictionary to hold the ticket data
        data = {
        "short_description": short_description,
        "urgency": urgency
        }
    
    # Make the API request to create the ticket
        response = requests.post(
        BASE_URL,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"}
        )
        print(response)
    # Check the response
        if response.status_code == 201:
            result = response.json()
            ticket_id = result['result']['sys_id']
            inc_number=result['result']['number']
            print(ticket_id)
            result1['Ticket_ID'] = ticket_id
            result1['Inc_Number'] = inc_number
            return render_template("result_data.html", result=result1)
            
        else:
            return render_template('fail.html')
        
@app.route('/status', methods=['POST', 'GET'])

def check_ticket_status():
        if request.method == 'POST':
            result1 = {}
            result = request.form
    # Get ticket ID from the entry field
            ticket_id = result['ticketid']
    
    # Make the API request to check ticket status
            response = requests.get(
        f"{BASE_URL}/{ticket_id}",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"}
    )
    
    # Check the response
            if response.status_code == 200:
                result = response.json()
                print(result)
                status = result['result']['state']
                result1['Ticket_ID'] = ticket_id
                result1['Incident_State'] = status
                result1['close_code'] = result['result']['close_code']
                result1['close_note'] = result['result']['close_notes']

                return render_template("result_data.html", result=result1)
        
            else:
                return render_template('fail.html')

            
        


if __name__ == '__main__':
    app.run(debug=True)
