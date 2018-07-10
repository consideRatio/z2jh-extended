- DONE: Pod Culler is now a jupyterhub service

Since JupyterHub 0.9 the pod culler is integrated as a jupyterhub service instead of being deployed as a pod with associated container image.

- DONE: Values.yaml: cull.maxAge bug fixed

The value cull.maxAge was previously never consumed by the jupyterhub_config.py as it reads from its configmap where the entry cull.max-age was never set. This affected maxAge based cullings on JupyterHub 0.9+.

- DONE: Remove `schedulerStrategy: pack | spread`

This was a half measure solution in order to pack user pods on nodes for better cluster autoscaling. The to be implemented custom scheduler will allow actual packing of user pods while this option that enables a preferred pod affinty made pods schedule on a nodes one or more user pod on it already.

For example, consider having three nodes: one empty node and two nodes with one user pod on them. A custom user scheduler could schedule five additional user pods to the same node by looking how much resoureces were requested, but simply adding a user pod affinity would only ensure that new pods are scheduled on one of the two nodes with one or more user pod on it. This option is overpromising things, let us not mislead the users and direct them towards a custom scheduler instead.

- DONE: Bumping pause image

In order to keep up to date, bumping the pause image container to 3.1.

- DONE: Upgrade various resource APIs (K8s 1.9+)

Keeping up with the kubernetes API development, the new API requires k8s 1.9+.

For more information see: https://v1-8.docs.kubernetes.io/docs/reference/workloads-18-19/

- DONE: Image-puller's made robost (Helm 2.9+)

The hook based puller ensures user images are pulled to the nodes before an upgrade of the hub takes place. This is helpful as if this wouldn't be done, users would potentially be spawned on nodes without the user image available forcing them to wait up to minutes. The users would probably think something was wrong and shut down ahead of time.

To complement this pre-upgrade / pre-install hook based image puller, the continuous puller will pull images to all nodes right when they are created, for example by a cluster autoscaler. The continuous image puller is now enabled by default as it is very useful for the cluster autoscaling used in conjunction with user placehodlers that is creating headroom.

Due to a bug in Helm related to the annotation `helm.sh/hook-delete-policy: hook-failed`, multiple puller instances tended to accumulate. In this commit the deletion policy `before-hook-creation` enters our code base (Helm 2.9+) and allows for a pre-existing k8s resource with the same name to be deleted before helm tries to create it. Without this Helm would raise an "... already exist" error. This also ensures that max one pre-install/upgrade hook puller would remain on install/upgrade failures. It also ensures that this single resource as well is cleaned up on the next successfull helm installation or upgrade.

- DONE: Added `hub.jupyter.org/storage-kind: user | core` labels to PVC's

Thanks to this label, an administrator would be able to select only the user storage for example.

NOTE: this change is safe to make without loosing the PVCs dynamically provisioned volume, but it will not influence already the PVCs already created by kubespawner.

- DONE: Added `hub.jupyter.org/pod-kind: user | core` labels to Pods

Allows for easier affinity rules and pod selection queries.

- DONE: Added the node affinity option `matchNodePurpose`

 With a dedicated node pool for core pods and user pods, we can with this option `prefer` or `require` that the pod's `hub.jupyter.org/pod-kind` value matches the nodes `hub.jupyter.org/node-purpose` value.

 Additional parts in next commit...

- DONE: Added support for configuring `extraTolerations` and `extra...Affinity`

For use with the kubespawner features introduced in https://github.com/jupyterhub/kubespawner/pull/205.

- DONE: Added a template helper for resource requests/limits

Ensures we avoid code duplication in the future when introducing user-placeholder and user-dummy along with real user pods.

- DONE: Added user-scheduler to schedule user pods

By adding a custom user scheduler, we can declare that our user pods should schedule with a different kind of logic. For cluster autoscaling purposes it is great to pack the user pods tight and that is exactly what this custom user pod scheduler will accomplish.

- DONE: Removed outdated pod affinity attempts

Previous attempts to make core pods stick to one node failed. The pod affinity on the hub and proxy pods probably only ended up giving a false sense of making the core pods stick to one node while they in reality end up on various nodes. By using node affinity to the `hub.jupyter.org/node-purpose` node label instead, we will accomplish a much more robust solution.

- DONE: Added PodPriority support (K8s 1.11+)

PodPriority allows pods with lower priority to be evicted by pods with higher priority. This can be utilized in conjunction with user placeholder pods to create a headroom on nodes and allow themselves to be evicted by real user pods if needed.

- DONE: Added user-placeholder deployment (Soft req: PodPriority)

To be used in conjuction with PodPriority and a cluster autoscaler in order to create headroom for real users. The placeholder pods are supposed to be evicted when the node resources are needed by a real user. When they get evicted and end up Pending they will make a cluster autoscaler scale up if possible.

```shell
# In order to scale the user placeholders dynamically...
kubectl patch deployment user-placeholder --patch '{"spec": {"replicas": 4}}'
```

- DONE: Added user-dummy deployment

To be used with the user-scheduler, PodPriority, user-placeholders and a cluster autoscaler in order to test how the system behaves. A user-dummy should simulate a real user, so it is configured to have the same affinities and PodPriority as a real user. The benefit of this deployment is that you can control the amount of user-dummy's very qickly as compared to awaiting users for testing.

```shell
# In order to scale the user dummies dynamically...
kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 4}}'
```

- DONE: Updated tools/lint.py to support K8s <=1.11

`kubeval` requires schemas for the K8s API. These were not available in the default kubeval repo, so while waiting for my PR to be accepted I point towards my repo as a source for the K8s API schemas used by `kubeval` at https://github.com/consideRatio/kubernetes-json-schema

- DONE: Consume singleuser.image with hub-config

Ensured consisted use of configmap instead of using environment variables for the singleuser image. The new configmap entry is named `singleuser.image-spec`.

- DONE: jupyterhub_config.py refreshed for readability

Nothing fancy, just made it easier to read through by grouping related configurations.

- DONE: Complementary - Allow setting of storage labels

- DONE: Complementary - Pod Culler as a JupyterHub Service

- DONE: Complementary - preferScheduleNextToRealUsers

Consider two nodes, one with two user-placeholder pods and one with two actual users. With this preconfigured affinity option set, the pod will schedule next to the real users which is what you would want in order to accomplish efficient cluster autoscaling.

NOTE: This is recommended for clusters with less than 100 nodes, but since pod affinities are computationally expensive and cause the scheduler to leave new pods in Pending state for seconds upwards if the cluster grows large.


IDEA:
SHOULD... the placeholder pods have anti-affinity for singleuser pods if the singleuserpods will 


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
- DONE: make a demo

- WAIT: hub.jupyter.org_dedicated: https://issuetracker.google.com/issues/77240642
- WAIT: await kubernetes 1.11 on GKE: https://cloud.google.com/kubernetes-engine/release-notes
- WAIT: Update kube-scheduler to 1.11 again https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/kube-scheduler-amd64


- segment the code to various PRs or at least commits
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