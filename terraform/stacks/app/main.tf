locals {
  # One entry per workspace. Keep default, because Task 1 runs there.
  settings = {
    default = { quota_pods = 10, limit_cpu = "200m", tier = "scratch" }
    dev     = { quota_pods = 20, limit_cpu = "200m", tier = "development" }
    staging = { quota_pods = 30, limit_cpu = "300m", tier = "pre-production" }
    prod    = { quota_pods = 50, limit_cpu = "500m", tier = "production" }
  }

  cfg = local.settings[terraform.workspace]
}

resource "kubernetes_namespace_v1" "env" {
  metadata {
    name = "project-${terraform.workspace}"
    labels = {
      "app.kubernetes.io/managed-by"       = "opentofu"
      "pod-security.kubernetes.io/enforce" = "baseline"
      environment                          = terraform.workspace
      tier                                 = local.cfg.tier
    }
  }
}

resource "kubernetes_resource_quota_v1" "env" {
  metadata {
    name      = "project-quota"
    namespace = kubernetes_namespace_v1.env.metadata[0].name
    labels = {
      "app.kubernetes.io/managed-by" = "opentofu"
      environment                    = terraform.workspace
    }
  }

  spec {
    hard = {
      pods = local.cfg.quota_pods
    }
  }
}

resource "kubernetes_limit_range_v1" "env" {
  metadata {
    name      = "project-limits"
    namespace = kubernetes_namespace_v1.env.metadata[0].name
    labels = {
      "app.kubernetes.io/managed-by" = "opentofu"
      environment                    = terraform.workspace
    }
  }

  spec {
    limit {
      type = "Container"
      default = {
        cpu    = local.cfg.limit_cpu
        memory = "256Mi"
      }
      default_request = {
        cpu    = "50m"
        memory = "64Mi"
      }
    }
  }
}

module "app_env" {
  source = "../../modules/settings"

  name        = "app-env"
  namespace   = kubernetes_namespace_v1.env.metadata[0].name
  environment = terraform.workspace
  data = {
    ENVIRONMENT = terraform.workspace
    TIER        = local.cfg.tier
  }
}

module "api_env" {
  source = "../../modules/settings"

  name        = "api-env"
  namespace   = kubernetes_namespace_v1.env.metadata[0].name
  environment = terraform.workspace
  data = {
    SERVICE = "api"
  }
}
