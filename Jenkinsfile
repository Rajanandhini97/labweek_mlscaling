pipeline {
    agent any

    stages {
        stage('Generate Metrics and Environment Variables') {
            steps {
                script {
                    def pythonScript = '''
import pandas as pd

# Read the CSV file
data = pd.read_csv('k8s_resource_usage.csv')

# Calculate values needed for environment variables
max_cpu_usage = data['cpu_usage'].max()
max_memory_usage = data['memory_usage'].max()

# Write values to a .env file
with open('metrics.env', 'w') as env_file:
    env_file.write(f"MAX_CPU_USAGE={max_cpu_usage}\\n")
    env_file.write(f"MAX_MEMORY_USAGE={max_memory_usage}\\n")

print("Environment variables have been written to metrics.env")
                    '''
                    writeFile file: 'generate_metrics.py', text: pythonScript
                    sh 'python3 generate_metrics.py'
                }
            }

        }

        // stage('Inject Environment Variables') {
        //     steps {
        //         // Use EnvInject to load variables from the .env file
        //         injectEnvVars(filePath: 'metrics.env')
        //     }
        // }

        stage('Inject Environment Variables') {
            steps {
                // Source the .env file and make variables available for this and future stages
                sh '''
                set -a
                source metrics.env
                set +a
                '''
            }
        }

        stage('Use Injected Environment Variables') {
            steps {
                script {
                    // Access the injected environment variables
                    echo "Max CPU Usage: ${env.MAX_CPU_USAGE}"
                    echo "Max Memory Usage: ${env.MAX_MEMORY_USAGE}"
                }
            }
        }
    }
}
