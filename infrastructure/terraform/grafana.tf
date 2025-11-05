# Grafana ConfigMap for Datasource
resource "kubernetes_config_map" "grafana_datasource" {
  metadata {
    name = "grafana-datasource"
  }

  data = {
    "datasource.yml" = <<-EOT
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          access: proxy
          url: http://prometheus-service:9090
          isDefault: true
          editable: true
    EOT
  }
}

# Grafana Deployment
resource "kubernetes_deployment" "grafana" {
  metadata {
    name = "grafana"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "grafana"
      }
    }

    template {
      metadata {
        labels = {
          app = "grafana"
        }
      }

      spec {
        container {
          name  = "grafana"
          image = "grafana/grafana:latest"

          port {
            container_port = 3000
          }

          env {
            name  = "GF_SECURITY_ADMIN_USER"
            value = "admin"
          }

          env {
            name  = "GF_SECURITY_ADMIN_PASSWORD"
            value = "admin"
          }

          env {
            name  = "GF_INSTALL_PLUGINS"
            value = ""
          }

          volume_mount {
            name       = "grafana-datasource"
            mount_path = "/etc/grafana/provisioning/datasources"
          }

          volume_mount {
            name       = "grafana-storage"
            mount_path = "/var/lib/grafana"
          }
        }

        volume {
          name = "grafana-datasource"
          config_map {
            name = kubernetes_config_map.grafana_datasource.metadata[0].name
          }
        }

        volume {
          name = "grafana-storage"
          empty_dir {}
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.prometheus
  ]
}

# Grafana Service
resource "kubernetes_service" "grafana" {
  metadata {
    name = "grafana-service"
  }

  spec {
    type = "NodePort"

    selector = {
      app = "grafana"
    }

    port {
      port        = 3000
      target_port = 3000
      node_port   = 30030
    }
  }
}