# Initial setup
## https://zero-to-jupyterhub.readthedocs.io/en/latest/create-k8s-cluster.html

## Pre-req 1
Get a google account and create a project: https://console.cloud.google.com/

## Pre-req 2
export GCLOUD_ACCOUNT=erik.i.sundell@gmail.com
export GCLOUD_PROJECT=jupyter-se
export GCLOUD_COMPUTE_REGION=europe-west3
export GCLOUD_COMPUTE_ZONE=europe-west3-c
export CLUSTER_NAME=jupyter-se
export K8S_NAMESPACE=prod
export HELM_RELEASE=prod

## Pre-req 3
gcloud components update

gcloud config set account $GCLOUD_ACCOUNT
gcloud config set project $GCLOUD_PROJECT
gcloud config set compute/region $GCLOUD_COMPUTE_REGION
gcloud config set compute/zone $GCLOUD_COMPUTE_ZONE

## Create cluster, setup kubernetes + helm, update kubectl config
gcloud container clusters create $CLUSTER_NAME \
    --num-nodes=1 \
    --machine-type=n1-standard-4 \
    --zone=europe-west3-c \
    --cluster-version=1.8.4-gke.1

kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$GCLOUD_ACCOUNT

kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller \
    --clusterrole=cluster-admin \
    --serviceaccount=kube-system:tiller
helm init --service-account tiller

kubectl --namespace=kube-system patch deployment tiller-deploy \
    --type=json \
    --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'





# Adjustments
## Scale down
gcloud container clusters resize $CLUSTER_NAME --size 0

## Scale up
#### NOTE: Helm upgrade > runs pre-puller > ensures new nodes gets images
#### gcloud container clusters list
gcloud container clusters resize $CLUSTER_NAME --size 1 --quiet
helm upgrade $HELM_RELEASE \
    --wait \
    --install \
    --namespace=$K8S_NAMESPACE \
    --values z2jh-extended/secret-values.yaml \
    z2jh-extended/






# Tear down
Visit console.cloud...

# Re-Setup
kubectl config use-context $CLUSTER_NAME
kubectl config set-context $(kubectl config current-context) --namespace=$K8S_NAMESPACE





# Update old
./build.py build --push
./build.py deploy 

helm upgrade --wait --install --namespace=hub hub jupyterhub/ -f gcloud-config.yaml
kubectl delete pod $(kubectl -n hub get pod | grep -Eo "hub[^ ]+") $(kubectl -n hub get pod | grep -Eo "proxy[^ ]+") $(kubectl -n hub get pod | grep -Eo "jupyter-[^ ]+")
kubectl get pod

# Update new
- Make a git commit
./build.py --push 







# Logs
kubectl logs $(kubectl get pod | grep -v Terminating | awk '/^hub/ {print $1}')
kubectl logs $(kubectl get pod | grep -v Terminating | awk '/^proxy/ {print $1}') nginx
kubectl logs $(kubectl get pod | grep -v Terminating | awk '/^proxy/ {print $1}') chp
kubectl logs $(kubectl get pod | grep -v Terminating | awk '/^proxy/ {print $1}') kube-lego

# Basic
kubetl get pod
kubetl get svc








# Private docker repo?
$ kubectl create secret docker-registry myregistrykey --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
spec:
  containers:
    - name: foo
      image: janedoe/awesomeapp:v1
  imagePullSecrets:
    - name: myregistrykey # <----------



# PodPresets to mount for students / instructors / schools?




# HELM
install --debug --dry-run ./z2jh-extended


# GIT
## Update the zero-to-jupyterhub-k8s project
git submodule foreach git pull origin master


# DNS

kubectl --namespace=kube-system get svc
# Funkar
## Test av kube-dns
kubectl exec -c nginx $(kubectl get pod | awk '/^proxy/ {print $1}') ping proxy-api.hub.svc.cluster.local


conda install -c conda-forge nbgrader

## To disable the Assignment List extension:
jupyter nbextension disable --sys-prefix assignment_list/main --section=tree
jupyter serverextension disable --sys-prefix nbgrader.server_extensions.assignment_list

## To disable the Create Assignment extension:
jupyter nbextension disable --sys-prefix create_assignment/main

## To disable the Formgrader extension:
jupyter nbextension disable --sys-prefix formgrader/main --section=tree
jupyter serverextension disable --sys-prefix nbgrader.server_extensions.formgrader







# Inspect node utilization
kubectl describe nodes
















# ABOUT AUTH STUFF...

## SETUP
microsoft = oauth.remote_app(
	'microsoft',
	consumer_key='98cb4414-51b6-4665-8cfa-3e884e95ed74',
	consumer_secret='bjuABQF110:-[azpmDHR00]',
	request_token_params={'scope': 'offline_access User.Read'},
	base_url='https://graph.microsoft.com/v1.0/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
	authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)

## RESPONSE
{  
    '@odata.context':'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
    'id':'44400c56-b95f-4adb-b014-d9d2221d33c1',
    'businessPhones':[],
    'displayName':'Erik Sundell',
    'givenName':'Erik',
    'jobTitle':'Lärare',
    'mail':'erik.sundell@it-gymnasiet.se',
    'mobilePhone':None,
    'officeLocation':'IT-Gymnasiet Uppsala',
    'preferredLanguage':None,
    'surname':'Sundell',
    'userPrincipalName':'erik.sundell@learnet.se'
 }

## NOW AVAILABLE IN THE NOTEBOOKS
import os
print('AUTH_USERNAME:', os.environ['AUTH_USERNAME'])
print('AUTH_USER_PRINCIPAL_NAME:', os.environ['AUTH_USER_PRINCIPAL_NAME'])
print('AUTH_DISPLAY_NAME:', os.environ['AUTH_DISPLAY_NAME'])
print('AUTH_GIVEN_NAME:', os.environ['AUTH_GIVEN_NAME'])
print('AUTH_SURNAME:', os.environ['AUTH_SURNAME'])
print('AUTH_MAIL:', os.environ['AUTH_MAIL'])
print('AUTH_JOB_TITLE:', os.environ['AUTH_JOB_TITLE'])
print('AUTH_OFFICE_LOCATION:', os.environ['AUTH_OFFICE_LOCATION'])


# -----------
# confused things in the end of initial setup...
# ... visit /home/username/.kube/config and clear it up there instead...
export TMP_CONTEXT=$(kubectl config get-contexts | grep '*' | awk '{print $2}')
export TMP_CLUSTER=$(kubectl config get-contexts | grep '*' | awk '{print $3}')
export TMP_AUTHINFO=$(kubectl config get-contexts | grep '*' | awk '{print $4}')

kubectl config set-context $CLUSTER_NAME \
    --cluster=$TMP_CLUSTER \
    --user=$TMP_AUTHINFO \
    --namespace=$K8S_NAMESPACE

kubectl config use-context $CLUSTER_NAME
kubectl config delete-context $TMP_CONTEXT
# -----------