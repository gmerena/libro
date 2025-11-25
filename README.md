# Libro

Könyvtár kezelő REST API az SZTE Felhő és DevOps alkalmazásai kurzushoz.

## Stack

- **Backend:** Python 3.13, FastAPI, asyncpg
- **Függőségkezelés:** uv
- **Adatbázis:** PostgreSQL

## DevOps eszközök

- Minikube
- Terraform
- Jenkins
- Prometheus
- Grafana

## Futtatás

```bash
minikube start

cd infrastructure/terraform
terraform init
terraform apply

# Port-forwardok (opcionális)
./portforwards.sh
```