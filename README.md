Prerequisites:
Python 3.x
MongoDB
RabbitMQ

Installation:
git clone https://github.com/MandalSagar/Rabbitmq_task.git
cd <repository_directory>
python3.x -m venv env
source env/bin/activate
pip install -r requirements.txt

To run the Client Script
To generate rangom status code between 0,6 and send that to rabbitMq queue 
python client.py

To run the Server 
To process the status from rmmbitMq and also api to fetch data from mongodb on the basis of timestamp
python api.py



Sample Curl Request:
curl -X GET "http://127.0.0.1:5010/status?start_time=2024-07-06%2018:35:30&end_time=2024-07-06%2018:36:00"
