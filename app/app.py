from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from kubernetes import client, config

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#config.load_kube_config()
config.load_incluster_config()

@app.route('/')
def home():
    """Home page with navigation."""
    return render_template('base.html')

@app.route('/create', methods=['GET', 'POST'])
def create_environment():
    """Create a new environment"""
    if request.method == 'POST':
        namespace = request.form.get('namespace')
        if not namespace:
            flash('Namespace is required!', 'error')
            return redirect(url_for('create_environment'))
        
        k8s_core = client.CoreV1Api()
        k8s_apps = client.AppsV1Api()
        k8s_svc = client.CoreV1Api()
        namespace_body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
        try:
            k8s_core.create_namespace(body=namespace_body)
            flash(f'Environment "{namespace}" created successfully!', 'success')
        except client.ApiException as e:
            flash(f'Error creating namespace: {e}', 'error')
            return redirect(url_for('create_environment'))
        k8s_apps = client.AppsV1Api()
        deployment_body = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "weather-webapp",
                "namespace": namespace
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "weather-webapp"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "weather-webapp"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "weather-webapp",
                                "image": "devopsgoofy/weather-webapp:latest",
                                "ports": [{"containerPort": 5000}]
                            }
                        ]
                    }
                }
            }
        }
        try:
            k8s_apps.create_namespaced_deployment(
                body=deployment_body,
                namespace=namespace
            )
            flash(f'Deployment for "{namespace}" created successfully!', 'success')
        except client.ApiException as e:
            flash(f'Error creating deployment: {e}', 'error')
            return redirect(url_for('create_environment'))
        
        service_body = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "weather-webapp-service",
                "namespace": namespace
            },
            "spec": {
                "selector": {
                    "app": "weather-webapp"
                },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 5000
                    }
                ],
                "type": "NodePort"
            }
        }
        try:
            k8s_svc.create_namespaced_service(
                body=service_body,
                namespace=namespace
            )
            flash(f'Service for "{namespace}" created successfully!', 'success')
        except client.ApiException as e:
            flash(f'Error creating service: {e}', 'error')
            return redirect(url_for('create_environment'))
        
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_environment():
    """Delete an environment."""
    if request.method == 'POST':
        namespace = request.form.get('namespace')
        if not namespace:
            flash('Namespace is required!', 'error')
            return redirect(url_for('delete_environment'))
        k8s_core = client.CoreV1Api()
        try:
            k8s_core.delete_namespace(name=namespace)
            flash(f'Environment "{namespace}" deleted successfully!', 'success')
        except client.ApiException as e:
            flash(f'Error deleting namespace: {e}', 'error')
        return redirect(url_for('home'))
    k8s_core = client.CoreV1Api()
    namespaces = [ns.metadata.name for ns in k8s_core.list_namespace().items]
    return render_template('delete.html', namespaces=namespaces)

@app.route('/status', methods=['GET', 'POST'])
def check_status():
    """Check the status of a specific namespace."""
    k8s_core = client.CoreV1Api()
    k8s_apps = client.AppsV1Api()
    v1 = client.CoreV1Api()
    namespaces = [ns.metadata.name for ns in v1.list_namespace().items]

    if request.method == 'POST':
        namespace = request.form.get('namespace')
        if not namespace:
            flash('Namespace is required!', 'error')
            return redirect(url_for('check_status'))
        try:
            pods = k8s_core.list_namespaced_pod(namespace=namespace).items
            services = k8s_core.list_namespaced_service(namespace=namespace).items
            deployments = k8s_apps.list_namespaced_deployment(namespace=namespace).items
            pod_status = [{
                'name': pod.metadata.name,
                'status': pod.status.phase,
                'images': [container.image for container in pod.spec.containers]
            } for pod in pods]

            deployment_status = [{
                'name': deployment.metadata.name,
                'replicas': deployment.status.replicas,
                'ready_replicas': deployment.status.ready_replicas
            } for deployment in deployments]

            service_status = [{
                'name': service.metadata.name,
                'type': service.spec.type,
                'ports': service.spec.ports
            } for service in services]

            return render_template(
                'status.html',
                namespace=namespace,
                pods=pod_status,
                deployments=deployment_status,
                services=service_status,
                namespaces=namespaces
            )
        except client.ApiException as e:
            flash(f'Error fetching status: {e}', 'error')
            return redirect(url_for('check_status'))

    return render_template('status.html', namespaces=namespaces)

if __name__ == '__main__':
    app.run(debug=True)
