resource "kubernetes_config_map" "prometheus" {
  metadata {
    name = "prometheus-config"
  }

  data = {
    "prometheus.yml" = <<-EOT
      global:
        scrape_interval: 15s
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
        }
      }
    }
  }
}