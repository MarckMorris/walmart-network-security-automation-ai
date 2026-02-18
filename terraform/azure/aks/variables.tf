# AKS Module Variables

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "vnet_subnet_id" {
  description = "VNet subnet ID for AKS"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
}
