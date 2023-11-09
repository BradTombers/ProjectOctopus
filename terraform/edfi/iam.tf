resource "google_service_account" "edfi_cloud_run" {
  account_id   = "edfi-cloud-run"
  display_name = "EDFI Cloud Run Service Account"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.edfi_cloud_run.email}"
}

# Grant service account access to ods_password
resource "google_secret_manager_secret_iam_member" "ods_password_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.ods_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.edfi_cloud_run.email}"
}

# Grant service account access to admin_app_encryption_key
resource "google_secret_manager_secret_iam_member" "admin_app_encryption_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.admin_app_encryption_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.edfi_cloud_run.email}"
}
