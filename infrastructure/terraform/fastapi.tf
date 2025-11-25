resource "kubernetes_deployment" "libro" {
  metadata {
    name = "libro"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "libro"
      }
    }

    template {
      metadata {
        labels = {
          app = "libro"
        }
      }

      spec {
        container {
          name  = "libro"
          image = var.app_image
          
          image_pull_policy = "IfNotPresent"

          port {
            container_port = 8000
          }

          env {
            name  = "DB_HOST"
            value = "postgres-service"
          }

          env {
            name  = "DB_PORT"
            value = "5432"
          }

          env {
            name  = "DB_USER"
            value = "postgres"
          }

          env {
            name = "DB_PASSWORD"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.postgres.metadata[0].name
                key  = "postgres-password"
              }
            }
          }

          env {
            name  = "DB_NAME"
            value = var.postgres_db
          }

          env {
            name  = "DB_POOL_MIN_SIZE"
            value = "1"
          }

          env {
            name  = "DB_POOL_MAX_SIZE"
            value = "10"
          }

          env {
            name  = "API_PREFIX"
            value = "/api"
          }

          env {
            name  = "ENABLE_METRICS"
            value = "true"
          }
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.postgres
  ]
}

resource "kubernetes_service" "libro" {
  metadata {
    name = "libro-service"
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "libro"
    }

    port {
      port        = 8000
      target_port = 8000
    }
  }
}