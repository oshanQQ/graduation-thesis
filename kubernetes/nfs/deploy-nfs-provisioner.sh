helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/

helm upgrade --cleanup-on-fail \
    --install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --namespace nfs \
    --create-namespace \
    --set nfs.server=192.168.10.51 \
    --set nfs.path=/nfs \
    --set storageClass.defaultClass=true \
    --set storageClass.name=nfs
