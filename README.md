## Filebeat logging, Elasticsearch and Kibana Setup

### Setup using docker-compose

```bash
$ git clone https://github.com/Divya063/ELK_filebeat_deployment.git
$ cd ELK_filebeat_deployment
$ docker-compose up 

```
To check the kibana dashboard head over to [localhost:5601](http://localhost:5601) and apply filter `{ container.name : python_app }`, logs from python application will be visible there. Elasticsearch will be available at the url [localhost:9200](http://localhost:9200).

<b> Kibana Dashboard </b>

![Alt text](https://github.com/Divya063/ELK_filebeat_deployment/blob/master/screenshots/kibana_docker.png)

###  Migrate a Docker Compose Workflow to Kubernetes

kompose is a tool which takes a Docker Compose file and translates it into Kubernetes resources.

#### Installation (MacOS)

```bash

$ brew install Kompose

```
Installation instructions for other platforms are provided [here.](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/#install-kompose)

#### Using Kompose

To convert the docker-compose.yml file to files that we can use with kubectl, run `kompose convert` and then `kubectl apply -f <output file>`.

#### Example

```bash
$ kompose convert --volumes hostPath                      
WARN Ignoring user directive. User to be specified as a UID (numeric). 
INFO Kubernetes file "elasticsearch-service.yaml" created 
INFO Kubernetes file "kibana-service.yaml" created 
INFO Kubernetes file "app-deployment.yaml" created 
INFO Kubernetes file "elasticsearch-deployment.yaml" created 
INFO Kubernetes file "filebeat-deployment.yaml" created 
INFO Kubernetes file "kibana-deployment.yaml" created 

```
Then use kubectl apply -f <output file for the service you want to deploy>

```bash
$ kubectl apply -f filebeat-deployment.yaml               
deployment.apps/filebeat configured
```
After deploying the service head over to [Kubernetes dashboard](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/overview?namespace=default) to check for the status.

<b> Kubernetes dashboard </b>

![Alt text](https://github.com/Divya063/ELK_filebeat_deployment/blob/master/screenshots/dashboard.png)

To access the kibana and elasticsearch instance, do port forwarding. 

#### Example

```bash
$ kubectl get pods --namespace=default                    ─╯
NAME                             READY   STATUS    RESTARTS   AGE
app-79fb66779-l8gmv              1/1     Running   1          7h36m
elasticsearch-587cf4b694-mxbbk   1/1     Running   0          6h42m
filebeat-58d44cc6b7-8j2fd        1/1     Running   0          55m
kibana-cb8ffcf65-fshfp           1/1     Running   0          6h40m

# For elasticsearch
$ kubectl port-forward elasticsearch-587cf4b694-mxbbk  9200:9200 --namespace=default
Forwarding from 127.0.0.1:9200 -> 9200
Forwarding from [::1]:9200 -> 9200

# For Kibana
$ kubectl port-forward kibana-cb8ffcf65-fshfp  5601:5601 --namespace=default
Forwarding from 127.0.0.1:5601 -> 5601
Forwarding from [::1]:5601 -> 5601
Handling connection for 5601
```
Head over to [localhost:5601](http://localhost:5601) and apply filter `{container.labels.io_kubernetes_container_name:python-app}`, logs from python application will be visible there. Elasticsearch will be available at the url [localhost:9200](http://localhost:9200).

<b> Kibana Dashboard </b>
![Alt text](https://github.com/Divya063/ELK_filebeat_deployment/blob/master/screenshots/kube_kibana.png)




