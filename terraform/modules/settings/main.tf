locals {
  labels = {
    "app.kubernetes.io/managed-by" = "opentofu"
    environment                    = var.environment
  }
}

resource "kubernetes_config_map_v1" "this" {
  metadata {
    name      = var.name
    namespace = var.namespace
    labels    = local.labels
  }

  data = var.data
}

resource "kubernetes_secret_v1" "this" {
  metadata {
    name      = var.name
    namespace = var.namespace
    labels    = local.labels
  }

  data = {
    token = "placeholder-not-a-real-token"
  }
}
