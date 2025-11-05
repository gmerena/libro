#!/bin/bash
mkdir -p logs

echo "🔄 Port forwarding indítása..."

# Grafana
echo "➡️  Grafana (3000:30030)"
kubectl port-forward service/grafana-service 3000:3000 > logs/grafana.log 2>&1 &

# Jenkins
echo "➡️  Jenkins (8080:8080)"
kubectl port-forward service/jenkins-service 8080:8080 > logs/jenkins.log 2>&1 &

# Libro
echo "➡️  Libro (8000:8000)"
kubectl port-forward service/libro-service 8000:8000 > logs/libro.log 2>&1 &

# Postgres
echo "➡️  Postgres (5432:5432)"
kubectl port-forward service/postgres-service 5432:5432 > logs/postgres.log 2>&1 &

echo ""
echo "✅ Minden port-forward elindítva!"
echo "   Grafana  → http://localhost:3000"
echo "   Jenkins  → http://localhost:8080"
echo "   Libro    → http://localhost:8000"
echo "   Postgres → localhost:5432"
echo ""
echo "📜 Logok: $(pwd)/logs/"
echo ""
echo "Megállításhoz: pkill -f 'kubectl port-forward'"
