# Kubernetes Cluster Setup Guide

This guide will walk you through the steps to create a Kubernetes cluster using `kind`, `kubectl`, and other tools.

## Prerequisites

Ensure that you have the following tools installed on your system:

- Docker
- kind
- kubectl

## Steps

1. **Start Docker:** Before you begin, make sure Docker is running.
   
   **Note**: After the creation of each pod, make sure that all pods are in a Running and Ready state before continuing with the next command. To do this, run the following command:
   
   ```bash
   kubectl get pods -A
   ```

2. **Delete any existing Kubernetes cluster with kind:**
   
   ```bash
   kind delete cluster
   ```

3. **Create a Kubernetes cluster with kind:**
   
   ```bash
   kind create cluster --config=cluster/cluster_config.yaml
   ```

4. **Create resources from the MUD_K8S.yaml file:**
   
   ```bash
   kubectl create --filename app/MUD_K8S.yaml
   ```

5. **Apply the Vertical Pod Autoscaler (VPA) CRDs:**
   
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-v1-crd.yaml
   ```

6. **Apply the VPA RBAC:**
   
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-v1-rbac.yaml
   ```

7. **Create the metric server:**
   
   ```bash
   kubectl create --filename cluster/metric_server.yaml
   ```

8. **Create the VPA:**
   
   ```bash
   kubectl create --filename cluster/vpa.yaml
   ```

9. **Run the KEDA script:**
   
   ```bash
   ./KEDA.sh
   ```

10. **Create the Horizontal Pod Autoscaler (HPA):**
    
    ```bash
    kubectl create --filename cluster/hpa.yaml
    ```

11. **Apply the Kubernetes Dashboard deployment:**
    
    ```bash
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
    ```

12. **Apply the admin user and role binding:**
    
    ```bash
    kubectl apply -f dashboard-adminuser.yaml
    kubectl apply -f cluster_rolebinding.yaml
    ```

13. **Create a token for the admin user and save it to a file:**
    
    ```bash
    kubectl -n kubernetes-dashboard create token admin-user > token.txt
    ```

14. **Start the Kubernetes Dashboard:**
    
    ```bash
    kubectl proxy
    ```

After running these commands, your Kubernetes cluster should be up and running. You can access the Kubernetes Dashboard at `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`. Use the token in `token.txt` to log in.

## Support

If you encounter any issues while setting up the Kubernetes cluster, please open an issue in this repository.