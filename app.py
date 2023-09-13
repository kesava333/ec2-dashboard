import boto3
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ec2', methods=['POST'])
def ec2():
    ec2 = boto3.client('ec2')
    instance_id = request.form.get('instance_id')
    action = request.form.get('action')
    if action == 'start':
        ec2.start_instances(InstanceIds=[instance_id])
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=[instance_id])
    elif action == 'reboot':
        ec2.reboot_instances(InstanceIds=[instance_id])
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

