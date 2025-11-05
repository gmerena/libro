resource "kubernetes_persistent_volume_claim" "jenkins" {
  metadata {
    name = "jenkins-pvc"
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    
    resources {
      requests = {
        storage = "4Gi"
      }
    }
    
    storage_class_name = "standard"
  }
}

resource "kubernetes_deployment" "jenkins" {
  metadata {
    name = "jenkins"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "jenkins"
      }
    }

    template {
      metadata {
        labels = {
          app = "jenkins"
        }
      }

      spec {
        container {
          name  = "jenkins"
          image = var.jenkins_image
          
          image_pull_policy = "IfNotPresent"

          port {
            container_port = 8080
          }

          port {
            container_port = 50000
          }

          volume_mount {
            name       = "jenkins-data"
            mount_path = "/var/jenkins_home"
          }
        }

        volume {
          name = "jenkins-data"
          
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.jenkins.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "jenkins" {
  metadata {
    name = "jenkins-service"
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "jenkins"
    }

    port {
      port        = 8080
      target_port = 8080
    }
  }
}