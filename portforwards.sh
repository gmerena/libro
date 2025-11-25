#!/bin/bash
mkdir -p logs

kubectl port-forward service/grafana-service 3000:3000 > logs/grafana.log 2>&1 &
kubectl port-forward service/jenkins-service 8080:8080 > logs/jenkins.log 2>&1 &
kubectl port-forward service/libro-service 8000:8000 > logs/libro.log 2>&1 &
kubectl port-forward service/postgres-service 5432:5432 > logs/postgres.log 2>&1 &
kubectl port-forward service/prometheus-service 9090:9090 > logs/prometheus.log 2>&1 &

echo "Grafana - http://localhost:3000"
echo "Jenkins - http://localhost:8080"
echo "Libro - http://localhost:8000"
echo "Postgres - localhost:5432"
echo "Prometheus - http://localhost:9090"
echo ""
echo "Megállításhoz: pkill -f 'kubectl port-forward'"
