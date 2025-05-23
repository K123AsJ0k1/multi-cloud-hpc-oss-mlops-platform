#!/bin/bash

set -eoa pipefail

#######################################################################################
# Create and configure a cluster with Kind
#
# Usage: $ export HOST_IP=127.0.0.1; export CLUSTER_NAME="mlops-platform"; ./create_cluster.sh
#######################################################################################


if [ "$INSTALL_LOCAL_REGISTRY" = "true" ]; then
# create a cluster with the local registry enabled in containerd
cat <<EOF | kind create cluster --name $CLUSTER_NAME --image=kindest/node:v1.24.0 --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: dual
  apiServerAddress: ${HOST_IP}
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  - containerPort: 30950
    hostPort: 5000
    protocol: TCP
  - containerPort: 31000
    hostPort: 6000 
    protocol: TCP
  - containerPort: 31001
    hostPort: 6001
    protocol: TCP
  - containerPort: 31002
    hostPort: 6002
    protocol: TCP
  - containerPort: 31003
    hostPort: 6003
    protocol: TCP
  - containerPort: 31004
    hostPort: 6004
    protocol: TCP
  - containerPort: 31005
    hostPort: 6005
    protocol: TCP
  extraMounts:
    - hostPath: /dev/null
      containerPath: /var/run/nvidia-container-devices/all
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."${HOST_IP}:5001"]
    endpoint = ["http://kind-registry:5000"]
EOF

else
# create a cluster
cat <<EOF | kind create cluster --name $CLUSTER_NAME --image=kindest/node:v1.24.0 --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: dual
  apiServerAddress: ${HOST_IP}
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  extraMounts:
    - hostPath: /dev/null
      containerPath: /var/run/nvidia-container-devices/all
EOF

fi


# see https://github.com/kubernetes-sigs/kind/issues/2586
CONTAINER_ID=$(docker ps -aqf "name=$CLUSTER_NAME-control-plane")
docker exec -t ${CONTAINER_ID} bash -c "echo 'fs.inotify.max_user_watches=1048576' >> /etc/sysctl.conf"
docker exec -t ${CONTAINER_ID} bash -c "echo 'fs.inotify.max_user_instances=512' >> /etc/sysctl.conf"
docker exec -i ${CONTAINER_ID} bash -c "sysctl -p /etc/sysctl.conf"

#docker exec -ti ${CONTAINER_ID} ln -s /sbin/ldconfig /sbin/ldconfig.real

exit 0