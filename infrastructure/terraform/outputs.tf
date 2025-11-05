output "postgres_service" {
  value = "postgres-service:5432"
}

output "libro_service" {
  value = "libro-service:8000"
}

output "jenkins_service" {
  value = "jenkins-service:8080"
}

output "commands" {
  value = {
    port_forward_libro   = "kubectl port-forward service/libro-service 8000:8000"
    port_forward_jenkins = "kubectl port-forward service/jenkins-service 8080:8080"
    logs_libro           = "kubectl logs -l app=libro -f"
    logs_postgres        = "kubectl logs -l app=postgres -f"
  }
}