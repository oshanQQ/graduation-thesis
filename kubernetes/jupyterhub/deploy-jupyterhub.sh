helm upgrade --cleanup-on-fail \
  --install jhub jupyterhub/jupyterhub \
  --namespace jhub \
  --create-namespace \
  --version=2.0.0 \
  --debug \
  --timeout 10m0s \
  --values config.yaml
