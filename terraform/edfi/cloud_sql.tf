resource "google_sql_database_instance" "edfi_ods" {
  name             = "edfi-ods-db"
  region           = "us-central1"
  database_version = "POSTGRES_11"

  settings {
    tier = "db-custom-1-6144" # 1 cpu, 6144 MB
    backup_configuration {
      enabled    = true
      start_time = "08:00"
    }

    ip_configuration {
      require_ssl = true
    }

    database_flags {
      name  = "max_connections"
      value = "250"
    }

    location_preference {
      zone = "us-central1-c"
    }
  }
}
