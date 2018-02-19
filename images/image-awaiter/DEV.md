# Documentation
About kubectl proxy:
https://kubernetes.io/docs/tasks/access-kubernetes-api/http-proxy-access-api/

Example use of proxy
curl http://localhost:8080/api/v1/pods?labelSelector=component=hub

# Example work
#### Test proxy to cluster
--- cleanup
kubectl delete clusterrole image-awaiter; kubectl delete clusterrolebinding image-awaiter; kubectl delete sa image-awaiter; kubectl delete job image-awaiter; kubectl delete ds hook-image-puller

--- build and run locally through proxy
kubectl proxy --port=8080
docker build --tag consideratio/iptest:v0 .
docker run -it --rm --net=host consideratio/iptest:v0

--- run on cluster
kubectl run iptest --image=docker.io/consideratio/iptest:v1 --port=8080


https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.9/#list-all-namespaces-63

TODO:
- DONE: fix main.go to allow a debug parameter to be passed, if that is passed it should communicate to localhost 8080 instead.
- DONE: ensure basic function through the proxy
- DONE: try it out in a helm upgrade situation