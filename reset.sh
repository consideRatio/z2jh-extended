kubectl delete pod $(kubectl -n hub get pod | grep -Eo "hub[^ ]+") $(kubectl -n hub get pod | grep -Eo "proxy[^ ]+") $(kubectl -n hub get pod | grep -Eo "jupyter-[^ ]+")
