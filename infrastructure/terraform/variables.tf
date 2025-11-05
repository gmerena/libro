variable "postgres_password" {
  description = "Adatbázis jelszó"
  type        = string
  default     = "mysecret"
}

variable "postgres_db" {
  description = "Adatbázis név"
  type        = string
  default     = "libro"
}
  
variable "app_image" {
  description = "Libro app Docker image"
  type        = string
  default     = "libro:latest"
}

variable "jenkins_image" {
  description = "Jenkins Docker image"
  type        = string
  default     = "custom-jenkins:latest"
}