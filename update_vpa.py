import os
import yaml

# Load environment variables
min_cpu = os.getenv("MIN_CPU", "300m")
max_cpu = os.getenv("MAX_CPU", "1")
min_memory = os.getenv("MIN_MEMORY", "300Mi")
max_memory = os.getenv("MAX_MEMORY", "1Gi")

# Load the VPA YAML file
vpa_file_path = 'vpa.yml'

with open(vpa_file_path, 'r') as file:
    vpa_data = yaml.load(file, Loader=yaml.FullLoader)

# print(vpa_data)

try:
    container_policy = next(
        policy for policy in vpa_data['spec']['resourcePolicy']['containerPolicies']
        if policy['containerName'] == 'my-container'
    )
    # Update minAllowed values
    container_policy['minAllowed']['memory'] = min_memory
    container_policy['minAllowed']['cpu'] = min_cpu
    
    # Update maxAllowed values
    container_policy['maxAllowed']['memory'] = max_memory
    container_policy['maxAllowed']['cpu'] = max_cpu

except KeyError as e:
    print(f"Error: The YAML structure does not match the expected format. Missing key: {e}")
except StopIteration:
    print("Error: Could not find container policy for 'my-container'.")
else:
    # Save the updated YAML file
    with open(vpa_file_path, 'w') as file:
        yaml.safe_dump(vpa_data, file, default_flow_style=False)

    print(f"Updated {vpa_file_path} with new CPU and memory limits.")