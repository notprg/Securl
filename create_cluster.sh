kind create cluster --config=cluster/cluster_config.yaml
kubectl create --filename app/MUD_K8S.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-v1-crd-gen.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-rbac.yaml
kubectl create --filename cluster/metric_server.yaml
kubectl create --filename cluster/vpa.yaml
./KEDA.sh
kubectl create --filename cluster/hpa.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
kubectl apply -f dashboard-adminuser.yaml
kubectl apply -f cluster_rolebinding.yaml
kubectl -n kubernetes-dashboard create token admin-user > token.txt
echo "Starting Kubernetes Dashboard, to log in use token in token.txt"
kubectl proxy
