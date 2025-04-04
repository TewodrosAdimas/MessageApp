#!/bin/bash

# Check if Minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "Minikube not found! Please install Minikube first."
    exit 1
fi

# Step 1: Start Minikube Kubernetes Cluster
echo "Starting Kubernetes cluster..."
minikube start

# Step 2: Verify the cluster is running using kubectl
echo "Verifying Kubernetes cluster status..."
kubectl cluster-info

# Step 3: Retrieve available pods
echo "Retrieving available pods..."
kubectl get pods --all-namespaces

# Optional: Show the cluster nodes
echo "Listing nodes in the cluster..."
kubectl get nodes
