# Walmart Network Security Automation - Main Terraform Configuration
# Phase 1: Azure Infrastructure

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
  
  backend "azurerm" {
    # Configure after Azure subscription is ready
    # resource_group_name  = "walmart-terraform-state"
    # storage_account_name = "walmartterraformstate"
    # container_name       = "tfstate"
    # key                  = "network-security-automation.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Resource naming
locals {
  project_name = "walmart-netsec"
  environment  = var.environment
  location     = var.location
  
  tags = {
    Project     = "Walmart Network Security Automation"
    Environment = var.environment
    ManagedBy   = "Terraform"
    CostCenter  = "IT-Security"
    Owner       = "Network Security Team"
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.project_name}-${local.environment}-rg"
  location = local.location
  tags     = local.tags
}

# Virtual Network
module "networking" {
  source = "./azure/networking"
  
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  environment         = local.environment
  project_name        = local.project_name
  tags                = local.tags
}

# Azure Kubernetes Service
module "aks" {
  source = "./azure/aks"
  
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  environment         = local.environment
  project_name        = local.project_name
  vnet_subnet_id      = module.networking.aks_subnet_id
  tags                = local.tags
}

# Azure Database for PostgreSQL
module "database" {
  source = "./azure/database"
  
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  environment         = local.environment
  project_name        = local.project_name
  subnet_id           = module.networking.database_subnet_id
  tags                = local.tags
}

# Azure Key Vault
resource "azurerm_key_vault" "main" {
  name                = "${local.project_name}-${local.environment}-kv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
  
  enabled_for_deployment          = true
  enabled_for_disk_encryption     = true
  enabled_for_template_deployment = true
  purge_protection_enabled        = false
  
  tags = local.tags
}

data "azurerm_client_config" "current" {}

# Storage Account for logs and data
resource "azurerm_storage_account" "main" {
  name                     = "${replace(local.project_name, "-", "")}${local.environment}sa"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  
  tags = local.tags
}

resource "azurerm_storage_container" "ml_models" {
  name                  = "ml-models"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "logs" {
  name                  = "logs"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}
