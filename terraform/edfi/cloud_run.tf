resource "google_cloud_run_v2_service" "edfi_api" {
  name     = "edfi-api"
  location = "us-central1"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

    service_account = google_service_account.edfi_cloud_run.email

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.edfi_ods.connection_name]
      }
    }

    containers {
      image = "gcr.io/${var.project_id}/edfi-api"
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
      ports {
        container_port = 80
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name = "DB_PASS"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.ods_password.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}
