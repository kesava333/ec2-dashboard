import boto3
from flask import Flask, render_template

app = Flask(__name__)
# Initialize the Boto3 EC2 client
ec2 = boto3.client('ec2', region_name='us-east-2')

@app.route('/')
def list_ec2_instances():
    # Retrieve a list of EC2 instances
    instances = ec2.describe_instances()

    # Extract instance details
    instance_list = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_details = {
                'InstanceID': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PublicDNS': instance.get('PublicDnsName', 'N/A'),
                'PrivateIP': instance['PrivateIpAddress']
            }
            instance_list.append(instance_details)

    return render_template('ec2_instances.html', instances=instance_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
