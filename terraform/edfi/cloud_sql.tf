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

resource "google_sql_database" "edfi_admin_database" {
  name     = "EdFi_Admin"
  instance = google_sql_database_instance.edfi_ods.name
}

resource "google_sql_database" "edfi_security_database" {
  name     = "EdFi_Security"
  instance = google_sql_database_instance.edfi_ods.name
}

resource "google_sql_database" "edfi_ods_2023" {
  name     = "EdFi_Ods_2023"
  instance = google_sql_database_instance.edfi_ods.name
}
