import boto3
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ec2', methods=['POST'])
def ec2():
    ec2 = boto3.client('ec2')
    instance_id = request.form.get('i-07ee73a38da3f775a')
    action = request.form.get('action')
    if action == 'start':
        ec2.start_instances(InstanceIds=[instance_id])
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=[instance_id])
    elif action == 'reboot':
        ec2.reboot_instances(InstanceIds=[instance_id])
    return render_template('index.html')
def list_instances():
    # Retrieve a list of all EC2 instances
    instances = ec2.describe_instances()
    
    # Extract and format instance information
    instance_data = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_data.append({'InstanceID': instance_id, 'State': instance_state})
    
    return render_template('list_instances.html', instances=instance_data)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

