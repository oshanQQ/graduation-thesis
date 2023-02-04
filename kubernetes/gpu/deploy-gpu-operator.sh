helm repo add nvidia https://nvidia.github.io/gpu-operator
helm repo update

helm install --wait --generate-name \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator \
  --set driver.enabled=false
