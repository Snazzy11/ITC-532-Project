output "config_map_name" {
  description = "Name of the ConfigMap this module created"
  value       = kubernetes_config_map_v1.this.metadata[0].name
}

output "secret_name" {
  description = "Name of the Secret this module created"
  value       = kubernetes_secret_v1.this.metadata[0].name
}

output "setting_keys" {
  description = "Keys of the ConfigMap, in sorted order"
  value       = sort(keys(kubernetes_config_map_v1.this.data))
}
