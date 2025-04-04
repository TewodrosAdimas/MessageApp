#!/bin/bash

# Scale the Django app deployment to 3 replicas
echo "Scaling the Django app to 3 replicas..."
kubectl scale deployment messaging-app-deployment --replicas=3

# Verify that the deployment is scaled and multiple pods are running
echo "Verifying that the app pods are running..."
kubectl get pods

# Perform load testing using wrk tool (ensure wrk is installed)
echo "Starting load testing using wrk..."
wrk -t12 -c400 -d30s http://<your-service-ip>:8000/

# Monitor resource usage for the app and database pods
echo "Monitoring resource usage..."
kubectl top pods
