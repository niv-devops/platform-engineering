# Kubernetes Environment Management Platform

This platform allows you to manage Kubernetes environments by creating and deleting namespaces, as well as checking the status of deployments, pods, and services within those namespaces. The platform uses Flask as the web framework and interacts with Kubernetes using the Kubernetes Python client.

## Features

- **Create a New Environment**: Create a new namespace in Kubernetes, along with a deployment and a NodePort service for the `weather-webapp`.
- **Delete an Environment**: Delete a specific namespace and its associated resources (deployment and service).
- **Check Status**: Check the status of pods, deployments, and services within a namespace.
- **Namespace Management**: Provides functionality to select, create, delete, and view Kubernetes namespaces.

## Requirements

- **Python** 3.x
- **Flask**: A lightweight Python web framework
- **Kubernetes Python Client**: Used to interact with the Kubernetes API

### Required Python Packages

Install the necessary dependencies via `requirements.txt`:

```
Flask==2.3.2
kubernetes==25.0.0
```

To install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone this repository to your local machine.

2. Ensure you have **Kubernetes** set up and **kubectl** configured to communicate with your cluster.

3. If you haven't installed `kubectl` yet, you can follow [these instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

4. Run the application:

```bash
python app.py
```

5. The platform will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### `/create` (GET, POST)
This page allows you to create a new Kubernetes environment (namespace, deployment, and service).

- **GET**: Displays the form to create a new environment.
- **POST**: Creates the namespace, deployment, and service when the form is submitted.

### `/delete` (GET, POST)
This page allows you to delete an existing environment (namespace).

- **GET**: Displays a list of existing namespaces.
- **POST**: Deletes the selected namespace and its resources.

### `/status` (GET, POST)
This page allows you to check the status of a specific namespace, including the status of pods, deployments, and services.

- **GET**: Displays a list of existing namespaces.
- **POST**: Displays the status of pods, deployments, and services in the selected namespace.

## Example Usage

1. **Create a new environment**: Navigate to the `/create` page, provide a namespace name, and submit the form. The system will create a namespace, deployment, and NodePort service for the `weather-webapp`.

2. **Delete an environment**: Navigate to the `/delete` page, select a namespace to delete, and submit the form. The namespace and its resources will be deleted.

3. **Check status**: Navigate to the `/status` page, select a namespace, and submit the form to view the status of pods, deployments, and services in that namespace.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
