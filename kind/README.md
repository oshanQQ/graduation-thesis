# kindind (Kubernetes in Docker in Docker)

Dockerコンテナの中にkindクラスタを構築します。

初めてクラスタを構築する時は、Dockerイメージをビルドします。

```
$ docker-compose build
```

イメージをビルドできたら、コンテナを起動します。

```
$ docker-compose up -d
```

`/app`直下に、`gpu-runtime-estimation`ディレクトリを展開しています。  
今回は`/app/kind`ディレクトリまで移動します。

```
$ docker-compose exec -it kind ash

/ # ls
app    certs  etc    lib    mnt    proc   run    srv    tmp    var
bin    dev    home   media  opt    root   sbin   sys    usr

/ # cd app/kind
```

`kind`ディレクトリ直下で、クラスタを作成します。

```
/app/kind # kind create cluster

Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.25.3) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Not sure what to do next? 😅  Check out https://kind.sigs.k8s.io/docs/user/quick-start/
```

クラスタが展開されているのが確認できます。各NodeはDockerコンテナとして動いています。

```
/app/kind # kubectl get all -A

NAMESPACE            NAME                                             READY   STATUS    RESTARTS   AGE
kube-system          pod/coredns-565d847f94-d9jbg                     1/1     Running   0          3m15s
kube-system          pod/coredns-565d847f94-h2ggw                     1/1     Running   0          3m14s
kube-system          pod/etcd-kind-control-plane                      1/1     Running   0          3m27s
kube-system          pod/kindnet-nkzcb                                1/1     Running   0          3m15s
kube-system          pod/kube-apiserver-kind-control-plane            1/1     Running   0          3m27s
kube-system          pod/kube-controller-manager-kind-control-plane   1/1     Running   0          3m27s
kube-system          pod/kube-proxy-88vml                             1/1     Running   0          3m15s
kube-system          pod/kube-scheduler-kind-control-plane            1/1     Running   0          3m27s
local-path-storage   pod/local-path-provisioner-684f458cdd-gf6ld      1/1     Running   0          3m15s

NAMESPACE     NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
default       service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP                  3m29s
kube-system   service/kube-dns     ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   3m28s

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kindnet      1         1         1       1            1           <none>                   3m26s
kube-system   daemonset.apps/kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   3m28s

NAMESPACE            NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
kube-system          deployment.apps/coredns                  2/2     2            2           3m28s
local-path-storage   deployment.apps/local-path-provisioner   1/1     1            1           3m25s

NAMESPACE            NAME                                                DESIRED   CURRENT   READY   AGE
kube-system          replicaset.apps/coredns-565d847f94                  2         2         2       3m15s
local-path-storage   replicaset.apps/local-path-provisioner-684f458cdd   1         1         1       3m15s


/app/kind # docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                       NAMES
53dc503dd135        kindest/node:v1.25.3   "/usr/local/bin/entr…"   4 minutes ago       Up 4 minutes        127.0.0.1:38973->6443/tcp   kind-control-plane
```


