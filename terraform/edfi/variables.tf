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

variable "stack_env" {
  type        = string
  default     = "dev"
  description = "Stack Environment"
}

variable "dev_name" {
  type        = string
  default     = "btombers"
  description = "Stack Environment"
}

variable "data_owner_email" {
  description = "The email of the BigQuery data owner"
  type        = string
}

