#!/bin/bash

minikube start --cni=calico --driver=docker --container-runtime=containerd
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || { kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.4.0" | kubectl apply -f -; }
kubectl -n kube-system wait --for=condition=Ready --all=true pod

istioctl install --set profile=minimal -y

helm install db oci://registry-1.docker.io/cloudpirates/mariadb -f helm/mariadb/values.yml
helm install redis oci://registry-1.docker.io/cloudpirates/redis -f helm/redis/values.yml
kubectl wait --for=condition=Ready pod/db-0 pod/redis-0

helm upgrade --install cert-manager oci://quay.io/jetstack/charts/cert-manager --namespace cert-manager --create-namespace -f helm/cert-manager/values.yml
kubectl -n cert-manager wait --for=condition=Ready --all=true pod

helm install flux-operator oci://ghcr.io/controlplaneio-fluxcd/charts/flux-operator --namespace flux-system --create-namespace
kubectl -n flux-system wait --for=condition=Ready --all=true pod
kubectl -n flux-system apply -f flux-system/management.yml

# the secret has to be created somehow!
kubectl -n flux-system wait --for=condition=Ready --all=true pod
kubectl apply -k flux-system/
