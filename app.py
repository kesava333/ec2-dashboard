import boto3
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = 'Kcchow333#'
# Initialize the Boto3 EC2 client
ec2 = boto3.client('ec2', region_name='us-east-2')

@app.route('/')
def list_ec2_instances():
    # Retrieve a list of EC2 instances
    instances = ec2.describe_instances()
    running_count = 0  # Initialize running instance count
    stopped_count = 0  # Initialize stopped instance count

    # Extract instance details, including the instance name
    instance_list = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_name = ""
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break

            instance_details = {
                'InstanceID': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'InstanceName': instance_name,  # Add instance name
            }
            instance_list.append(instance_details)
            # Count instances based on state
            if instance_details['State'] == 'running':
                running_count += 1
            elif instance_details['State'] == 'stopped':
                stopped_count += 1
    # Calculate the instance count
    instance_count = len(instance_list)
    return render_template('ec2_instances.html', instances=instance_list, instance_count=instance_count, running_count=running_count, stopped_count=stopped_count)
    
@app.route('/start_instance', methods=['POST'])
def start_instance():
    instance_id = request.form.get('instance_id')
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        flash(f"Starting EC2 instance {instance_id}", 'success')
    except Exception as e:
        flash(f"Failed to start EC2 instance {instance_id}: {str(e)}", 'error')
    return redirect('/')

@app.route('/stop_instance', methods=['POST'])
def stop_instance():
    instance_id = request.form.get('instance_id')
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        flash(f"Stopping EC2 instance {instance_id}", 'success')
    except Exception as e:
        flash(f"Failed to stop EC2 instance {instance_id}: {str(e)}", 'error')
    return redirect('/')

@app.route('/terminate_instance', methods=['POST'])
def terminate_instance():
    instance_id = request.form.get('instance_id')
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        flash(f"Terminating EC2 instance {instance_id}", 'success')
    except Exception as e:
        flash(f"Failed to terminate EC2 instance {instance_id}: {str(e)}", 'error')
    return redirect('/')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
