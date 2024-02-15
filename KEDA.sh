#!/bin/bash
# Installing KEDA
echo "Installing KEDA..."
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace keda
kubectl get deploy,crd -n keda

# Installing HTTP-Add-on
echo "Installing HTTP-Add-On..."
helm install http-add-on kedacore/keda-add-ons-http --namespace keda

# Installing CRD
echo "Installing CRDs..."
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.0.0-beta/keda-2.0.0-beta.yaml
kubectl apply -f https://github.com/kedacore/keda/blob/main/config/samples/keda_v1alpha1_scaledjob.yaml
kubectl apply -f https://github.com/kedacore/keda/blob/main/config/samples/kustomization.yaml
kubectl apply -f https://github.com/kedacore/keda/blob/main/config/samples/http_v1alpha1_httpscaler.yaml
