resource "google_bigquery_dataset" "silver" {
  dataset_id                  = "silver"
  friendly_name               = "silver"
  description                 = "Contains cleansed and conformed data"
  location                    = "us-central1"

  labels = {
    env = var.stack_env
  }
}

resource "google_bigquery_dataset" "gold" {
  dataset_id                  = "gold"
  description                 = "Contains optimized reports"
  location                    = "us-central1"

  labels = {
    env = var.stack_env
  }
}

resource "google_bigquery_dataset_iam_binding" "silver_owner" {
  dataset_id = google_bigquery_dataset.silver.dataset_id
  role       = "roles/bigquery.dataOwner"

  members = [
    "user:${var.data_owner_email}",
  ]
}

resource "google_bigquery_dataset_iam_binding" "gold_owner" {
  dataset_id = google_bigquery_dataset.silver.dataset_id
  role       = "roles/bigquery.dataOwner"

  members = [
    "user:${var.data_owner_email}",
  ]
}