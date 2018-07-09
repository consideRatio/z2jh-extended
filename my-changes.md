kubespawner singleuser_/user_ prefix fixes #745
kubespawner storage extra labels
helm hook fixup (recommend 2.9)
scheduler stuff
placeholder stuff
user-dummy stuff
pause 3.1
hub/proxy pod affinities replaced with node affinities
labeling update for easier pod affinity
podculler integrated into jupyterhub
podculler maxAge bugfix
bump kubespawner
extraTolerations supported
extra...Affinity supported


VERIFICATION:
create a node pool
    jupyterhub-core-pool
    jupyterhub-user-pool
label a node pool
    jupyterhub-purpose: core
    jupyterhub-purpose: user
taint a node pool
    jupyterhub-dedicated: user
PriorityClass + priorityClassName

# PLACEHOLDER PODS
# Should be USER PODS + 
priorityClassName: jupyterhub-user-placeholder-priority


autoscaler todo:
- DONE: core stuff should have a preferred core affinity
- DONE: user stuff should have a preferred user affinity
- DONE: fix schedulers rbac:  https://kubernetes.slack.com/messages/C09TP78DV/ (AWAIT)
  - https://github.com/kubernetes/kubernetes/blob/master/plugin/pkg/auth/authorizer/rbac/bootstrappolicy/testdata/cluster-roles.yaml
- DONE: fix PriorityClass installation: https://github.com/kubernetes/helm/issues/4277 (AWAIT)
- DONE: decide on required / preferred node affinity for the user pods (preferred / preferred but configurable)
- DONE: change pod-kind to pod-kind?
- DONE: antipodaffinity on node schedulers
- DONE: fix jupyterhub_config.py fully
- DONE: schema for placeholder values
- DONE: schema for user dummy values
- DONE: did not work well... PVC, make the PV remain if PVC is deleted somehow? Deletion policy or similar?
- DONE: try -> merge mins kubespawner
- DONE: Allow setting tolerations and affinities
    - PR: https://github.com/jupyterhub/kubespawner/pull/205
- DONE: allow adding additional tolerations
- DONE: allow adding additional affinities
- DONE: fix schedulers namespace workaround (what did i do?): https://github.com/kubernetes/kubernetes/issues/60469 (AWAIT)
- DONE: update schemas

- WAIT: hub.jupyter.org_dedicated: https://issuetracker.google.com/issues/77240642
- WAIT: await kubernetes 1.11 on GKE: https://cloud.google.com/kubernetes-engine/release-notes
- WAIT: Update kube-scheduler to 1.11 again https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/kube-scheduler-amd64


- segment the code to various PRs or at least commits
- make a demo
    - show pending pods
- draft-update scheduler to utilize KubeSchedulerConfig api

TODO Documentation:
- deprecate packing of pods
- update gcloud guide (adding new pools with labels/taints, removing old, gcloud set zone first)
    - request help for amazon etc
- update placeholder and user-dummy information
- add recommendation on securing the PV by adjusting its reclaimpolicy
- changelog

FUTURE
- consider adding another culler for placeholder pods

# placeholder / user-dummy
kubectl patch deployment placeholder --patch '{"spec": {"replicas": 0}}'
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 0}}'





# kube-dns patch
kubectl patch configmap --namespace kube-system kube-dns-autoscaler --patch '{"data": {"linear": "{\"coresPerReplica\":256,\"nodesPerReplica\":16,\"preventSinglePointFailure\":false}"}}'

# before creating the cluster
gcloud config set container/cluster test-cluster-1
gcloud config set compute/zone europe-west3-c
gcloud config set container/new_scopes_behavior true

# creating the cluster...
gcloud container clusters create test-cluster-1 \
--enable-kubernetes-alpha \
--cluster-version=latest \
--num-nodes=1

    Hmmm...
--enable-autorepair
--no-enable-cloud-logging \
--no-enable-cloud-monitoring

# deleting default pool
gcloud container node-pools delete default-pool

# creating core pool
gcloud container node-pools create \
core-pool \
--machine-type=n1-standard-1 \
--num-nodes=1 \
--node-labels=hub.jupyter.org/node-purpose=core \
--enable-autorepair

# creating user pool
gcloud beta container node-pools create user-pool \
--preemptible \
--machine-type=n1-standard-4 \
--num-nodes=0 \
--enable-autoscaling \
--min-nodes=0 \
--max-nodes=10 \
--node-labels hub.jupyter.org/node-purpose=user \
--node-taints hub.jupyter.org_dedicated=user:NoSchedule \
--enable-autorepair





Demonstration

1. Add 4 placeholders
kubectl patch deployment placeholder --patch '{"spec": {"replicas": 4}}'
2. Add 4 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 4}}'
3. Add to 8 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 8}}'
4. Remove to 0 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 0}}'
5. Add to 4 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 4}}'
6. Add to 8 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 8}}'
7. Add to 28 dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 28}}'
8. Remove all dummy-users
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 0}}'



--- User nodes
watch -t -n 0.5 'echo "# User nodes"; echo; kubectl get nodes --selector hub.jupyter.org/node-purpose=user | cut -c 1-55'

--- Pending pods
watch -t -n 0.5 'tput setaf 3; echo "# Pending pods"; echo; kubectl get pods --field-selector=status.phase=Pending | cut -c 1-53'

--- Scheduled pods
watch -t -n 0.5 'tput setaf 2; echo "# Scheduled pods"; echo; kubectl describe node --selector=hub.jupyter.org/node-purpose=user | grep -E "user-placeholder|user-d
ummy|Namespace" | cut -c 1-56'

watch -t 'printf "# A DEMO OF: kube-scheduler, cluster autoscaler, pod-priority

--- CA
watch -n 0.5 -t 'echo "# Cluster Autoscaler status"; echo; kubectl get cm -n kube-system cluster-autoscaler-status -o yaml | grep gke-test -A 6 | cut -c 6-58'

1. Adding 4 placeholder pods  --- CA scale up
2. Adding 4 dummy-user pods   --- 1 node full (max 8 pods)
3. Adding 4 dummy-user pods   --- Placeholders evicted > CA scale up > Placeholders reschedule
4. Removing 8 dummy-user pods --- 1 node at 4/8 and 1 node at 0/8
5. Adding 4 dummy-user pods   --- Users packed instead of spread
6. Adding 4 dummy-user pods   --- Placeholders evicted > Users packs with Users
7. Adding 20 dummy-user pods  --- CA adds two more nodes
8. Removing all dummy-users   --- CA scale down (~10 min delay)"'

watch -t "tput setaf 7; printf '# A demonstration of:

# Details
1. Placeholders get evicted (Max 4 per node)
2. Pending pods triggers scale up
3. Scheduler packs pods tight

# About
- z2jh.jupyter.org
- github.com/jupyterhub/zero-to-jupyterhub-k8s

# Made by
@consideRatio / Erik Sundell'"






GOOD:
1. Fill up based on # of real user pods rather than placeholder pods
2. Allow the cluster autoscaler to relocate placeholders


THOUGHTS:
- Placeholder pods wasn't preempted when real users had room on another node
- The culler shut down the placeholder pods and the user dummies
    WHY?! They didn't have a singleuser label or similar.