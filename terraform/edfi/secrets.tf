resource "google_secret_manager_secret" "ods_password" {
  secret_id = "ods-password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "admin_app_encryption_key" {
  secret_id = "admin-app-encryption-key"

  replication {
    auto {}
  }
}
