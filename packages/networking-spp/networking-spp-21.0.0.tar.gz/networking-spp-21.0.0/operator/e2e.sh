#! /bin/bash
kubectl apply -f deploy/crds/spp.spp_crd.yaml
kubectl apply -f deploy/service_account.yaml
kubectl apply -f deploy/role.yaml
kubectl apply -f deploy/role_binding.yaml 
kubectl apply -f deploy/operator.yaml 
operator-sdk test local ./test/e2e --namespace default --no-setup
kubectl delete deployment spp-operator
