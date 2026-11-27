variable "name" {
  description = "Name of the ConfigMap and the Secret"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", var.name)) && length(var.name) <= 63
    error_message = "name must be a lowercase Kubernetes name: letters, digits and hyphens, starting and ending with a letter or digit, at most 63 characters."
  }
}

variable "namespace" {
  description = "Namespace both objects are created in. The caller creates it"
  type        = string
}

variable "environment" {
  description = "Environment both objects belong to, written as their environment label"
  type        = string
}

variable "data" {
  description = "Settings written into the ConfigMap, as keys and values"
  type        = map(string)
}
