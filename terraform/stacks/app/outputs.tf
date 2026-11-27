output "namespace" {
  description = "Namespace this workspace created"
  value       = kubernetes_namespace_v1.env.metadata[0].name
}

output "settings_config_maps" {
  description = "ConfigMaps the settings module created"
  value       = [module.app_env.config_map_name, module.api_env.config_map_name]
}
