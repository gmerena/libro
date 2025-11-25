resource "kubernetes_config_map" "prometheus" {
  metadata {
    name = "prometheus-config"
  }

  data = {
    "prometheus.yml" = <<-EOT
      global:
        scrape_interval: 15s

      scrape_configs:
        - job_name: 'libro-api'
          static_configs:
            - targets: ['libro-service:8000']
          metrics_path: '/metrics'
    EOT
  }
}

resource "kubernetes_deployment" "prometheus" {
  metadata {
    name = "prometheus"
  }
  
  spec {
    replicas = 1
    
    selector {
      match_labels = {
        app = "prometheus"
      }
    }
    
    template {
      metadata {
        labels = {
          app = "prometheus"
        }
      }
      
      spec {
        container {
          name  = "prometheus"
          image = "prom/prometheus:latest"

          port {
            container_port = 9090
          }

          args = [
            "--config.file=/etc/prometheus/prometheus.yml",
            "--storage.tsdb.path=/prometheus"
          ]

          volume_mount {
            name       = "prometheus-config"
            mount_path = "/etc/prometheus"
          }
        }

        volume {
          name = "prometheus-config"
          config_map {
            name = kubernetes_config_map.prometheus.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "prometheus" {
  metadata {
    name = "prometheus-service"
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "prometheus"
    }

    port {
      port        = 9090
      target_port = 9090
    }
  }
}