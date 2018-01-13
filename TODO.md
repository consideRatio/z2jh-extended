# Big day TODO
- WAITING...: Allow scaling up to 25 nodes
- Activity backend
  - (essential) User submission of progress responded by progress made
  - (fancy) Dashboard
- Create notebooks
  - BASIC: Python programming certificate
  - MATH: Gradient descent lab
  - PHYSICS: Electric fields

# Big day pre-launch
- Scale up to 25 nodes
- Make sure the nodes have the images prepulled










#TODO
- DONE: Git update / Rebase this repo
- DONE: enabled nbgitpuller serverextension without installing overhead things
- DONE: Load balancer auto ok
- DONE: streamline initial cluster setup
- DONE: Test that hub.extra-config.py is working
- DONE: Git update / rebase this repo again
- DONE: Incorperate this PR
        https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/314
- DONE: Learn how to read logs from my config files
  - DONE: Reformulated: learn why and when, and if one can avoid clearing logs.
  - DONE: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/357
- DONE: Get nbgitpuller up and running...
        https://jupyter.se/hub/user-redirect/git-pull?repo=https://github.com/consideratio/jupyter-math&subPath=source/gradient-descent/gradient-descent.ipynb
- DONE: ENV variables for Learnet.se login
- DONE: Read about controllers (deployments etc)
- DONE: Read about storage
  - DONE: Decide on NFS, GlusterFS or ROOK etc.
  - DONE: Demo a standalone NFS server.
  - DONE: Demo a NFS service on k8s. 
    - YuviPanda is cautious about using a NFS service on k8s for several reasons, you can't RAID disks easily and autoscaling that moves the NFS-server pod can cause downtime for example.
      - Ignore RAID issue
      - Handle the autoscaling issue with priority
        - https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/
- DONE: Learn about inter-cluster DNS
- DONE: add hide_code https://github.com/kirbs-/hide_code
- DONE: Update secrets
- DONE: Remove exposed secret (zro..)


# NFS makes me angry...
- DONE: spawner.start, spawner.lifecyclehook, spawner.cmd, authentication pre_spawn_start
- DONE: FS_ID READ UP ABOUT the kubespawner fsid thing
- DONE: Handlings permissions with docker:
        https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
- DONE: Entrypoint vs CMD:
        https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/
- DONE: https://github.com/kubernetes/kubernetes/issues/2630

# Permissions makes me angry...
- learn about setfacl
- learn about UID, GID
- learn about chmod, chgrp, chown

# Big learning
- DONE: docker
- DONE: kubernetes
- DONE: jupyterhub
  - DONE: kubespawner
  - DONE: nbgrader, nbgitpuller
- DONE: bash scripts
  - DONE: http://guide.bash.academy/inception/
  - DONE: http://guide.bash.academy/commands/
  - DONE: http://guide.bash.academy/expansions/
  - DONE: http://guide.bash.academy/conditionals

# Small learning
- DONE: git-crypt
- DONE: tini - https://github.com/krallin/tini

# Build.py
- Add option to build.py to delete active user pods on deploy
- Make it look nice with click like yuvipandas berkely-dsep-infra repos
- Enable it to easily scale up and down
- Enable it to tear down and set up

- Project refactoring etc.
  - DONE: Secure secrets like this
          https://github.com/berkeley-dsep-infra/datahub/blob/staging/.gitattributes
  - DONE: Consider utilizing gitsubmodules
          https://github.com/yuvipanda/paws
  - DONE: Consider utilizing a subchart
    - Example of a "helm subchart"
      https://github.com/berkeley-dsep-infra/datahub/
  - DONE: Learn more about Helm
    - DONE: requirements.yaml function
    - DONE: Building Helm Charts From the Ground Up: An Introduction to Kubernetes:
            https://www.youtube.com/watch?v=vQX5nokoqrQ
    - DONE: Read documentation somewhat thoroughly
  - DONE: Learn more from KubeCon playlist...
    - DONE: Watched 20 videos..
  - DONE: Setup the build
    - DONE: Get the values.yaml functional
    - DONE: Get the nfs.yaml functional
    - DONE: Get the images functional
    - DONE: Get the build.py functional

- DONE: Use values in the template for nfs when it comes to storage etc...

- DONE: Fix the issue of not being able to read using get_config() within the extra-config.
  - REPORTED: Initially i got: TypeError: get_config() takes 0 positional arguments but 1 was given, issue reported
  - SOLVED: When I added a get_config function in the extra config, i got None values...

- Fix permissions on the exchange directory...
- DONE: Setup a custom NFS Dockerfile: 
        https://github.com/kubernetes/kubernetes/tree/master/test/images/volumes-tester/nfs
  - Stuff i want to have it do...
    - setup anonuid / anongid
    - 

- get prepuller job under control on z2jh-extended (be able to invoke it)
- DONE: get a git-repo volume setup
- DONE: get a startup script hook setup

# Introduction for teachers
- Allow guest login
- Make a 5 min video

# Usage docs
- pip install --user <packagename>
- conda install -p ~/.local <packagename>

# autoscaling
- cluster autoscaler + affinity
- 

- Get rid of the "groups: cannot find name for group ID 1000" warning
- Set the username to be specific for nbgraders sake
- DONE: Setup a "getting started" persistent readonly directory that can link to nbgitpuller links.
  - DONE: use a k8s git-volume mount and its done, it will have require root to change.
-

- DONE: Update node resource requests to limit on memory instead of CPU?

- Mount the NFS volume by settings in the kubespawner instead of the same setup using extraVolumeMounts...
- Prepopulate stuff into the NFS dir..

- DONE: Learn and document how to view the resource usage on my nodes.
  - DONE: kubectl describe nodes

- DONE: Try scaling usage for 32 students
- DONE: Try scaling usage for 200 students
  - DONE: Request higher CPU and "in-use-address" quotas on googles cloud console.

- Setup NBGrader
  - Setup NbGrader based on ... one single directory with ReadWriteMany
    - Fix permissions by using separate images for students and instructors
  - Setup NbGrader based on ... refined directory permissions
    - Consider changing the nbgrader directory structure
    - Learn where the nbgrader config files need to be located if so

- Volumes and mounts
  - DONE: Setup a NFS Service

    - DONE: Decide on a strategy about permissions and mounts for students / instructors
      - 1: NOT USED: Init containers
        - ? Permissions - can the init container adjust permissions on the mount in another container?
        - ? Mounts - can they mount containers? No...
        - TO CONFIRM: You can use environment variables to decide on permissions
      - 2: USED: Separate images
        - TO CONFIRM: Images (can be) chosen by kubespawner in the pre_spawn_start function of the authenticator class.
        - UNUSED: Images (can be) chosen by pod presets based on pod labels
      - 3: Pod-presets
        - ? Label the student pods?

  - Learn more about Linux user and group permissions
    - DONE: Learn about changing user within docker

- Use google cloud repository for docker images
  - https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
  
  - DONE: Labels: Student / Instructor labelling of singleuser pods
  - Annotations: School annotations of singleuser pods
  - PodPresets: https://kubernetes.io/docs/concepts/workloads/pods/podpreset/
  - School volumes
    - teachers-to-teachers directory
    - teachers-to-students directory
    - nbgraders exchange directory

- Scaling
  - DONE: Manual scaling
  - Autoscaling (cordon?, drain?, eh...)

- Cluster teardown instructions

- Helm
  - Implement helm chart best practices:
    - https://gist.github.com/so0k/f927a4b60003cedd101a0911757c605a
- Run a script to update jupyter.se to point to the cloud ip?


# Advanced refinements
- secure-access-to-helm
  https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/security.html#secure-access-to-helm
- audit-cloud-metadata-server-security
  https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/security.html#audit-cloud-metadata-server-security
- delete-the-kubernetes-dashboard
  https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/security.html#delete-the-kubernetes-dashboard

- Update the extraConfig values to be a dict
  https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/398
- Utilize get_config in extraConfig without duplicating code
  https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/397