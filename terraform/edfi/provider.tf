terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.5.0"
    }
  }
}

provider "google" {
  project = "edfi-training"
  region  = var.region
  credentials = file("/Users/bradtombers/.creds/gcp-terraform-service-account-key.json")
}

terraform {
  backend "gcs" {
    bucket = "bt-training-tf-state"
    prefix = "terraform/state"
  }
}
