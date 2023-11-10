resource "google_bigquery_dataset" "silver" {
  dataset_id                  = "silver"
  friendly_name               = "silver"
  description                 = "Contains cleansed and conformed data"
  location                    = "us-central1"

  labels = {
    env = var.stack_env
  }

  access {
    role   = "READER"
    domain = "hashicorp.com"
  }
}

resource "google_bigquery_dataset" "gold" {
  dataset_id                  = "gold"
  description                 = "Contains optimized reports"
  location                    = "us-central1"

  labels = {
    env = var.stack_env
  }

  access {
    role   = "READER"
    domain = "hashicorp.com"
  }
}