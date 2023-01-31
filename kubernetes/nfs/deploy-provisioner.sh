helm upgrade --cleanup-on-fail \
    nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=192.168.10.51 \
    --set nfs.path=/nfs \
    --set nfs.mountOptions=v4 \
    --set storageClass.defaultClass=true \
    --set storageClass.name=nfs
