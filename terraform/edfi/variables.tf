variable "region" {
  type        = string
  default     = "us-central1"
  description = "Default region for GCP configuration"
}

variable "project_id" {
  type        = string
  default     = "edfi-training"
  description = "GCP Project ID"
}
