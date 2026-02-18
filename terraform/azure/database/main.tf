# Azure Database for PostgreSQL Module

variable "resource_group_name" {}
variable "location" {}
variable "environment" {}
variable "project_name" {}
variable "subnet_id" {}
variable "tags" {}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.project_name}-${var.environment}-postgres"
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "15"
  administrator_login    = "postgres_admin"
  administrator_password = random_password.postgres.result
  
  storage_mb            = 32768
  sku_name              = "GP_Standard_D4s_v3"
  backup_retention_days = 7
  geo_redundant_backup_enabled = true
  
  high_availability {
    mode = "ZoneRedundant"
  }
  
  tags = var.tags
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "network_security_automation"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# TimescaleDB extension
resource "azurerm_postgresql_flexible_server_configuration" "timescaledb" {
  name      = "shared_preload_libraries"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "timescaledb"
}

resource "random_password" "postgres" {
  length  = 32
  special = true
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "postgres_username" {
  value     = azurerm_postgresql_flexible_server.main.administrator_login
  sensitive = true
}

output "postgres_password" {
  value     = random_password.postgres.result
  sensitive = true
}
