resource "kubernetes_secret" "postgres" {
  metadata {
    name = "postgres-secret"
  }

  data = {
    postgres-password = var.postgres_password
  }

  type = "Opaque"
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    name = "postgres-deployment"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "postgres"
      }
    }

    template {
      metadata {
        labels = {
          app = "postgres"
        }
      }

      spec {
        container {
          name  = "postgres"
          image = "postgres:18-alpine"

          port {
            container_port = 5432
          }

          env {
            name  = "POSTGRES_PASSWORD"
            value = var.postgres_password
          }

          env {
            name  = "POSTGRES_DB"
            value = var.postgres_db
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "postgres" {
  metadata {
    name = "postgres-service"
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "postgres"
    }

    port {
      protocol    = "TCP"
      port        = 5432
      target_port = 5432
    }
  }
}