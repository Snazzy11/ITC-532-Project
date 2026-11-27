# settings module
Creates a ConfigMap of the settings and a Secret holding a placeholder token. Both will get the same name, in an existing namespace. They are labeled `app.kubernetes.io/managed-by = opentofu` and with their environment.

The module doesnt have a `provider` so it uses the caller's Kubernetes provider.The state keeps values in plaintext so we must be careful with real credentials.

## Inputs

- `name` (string): The name of the ConfigMap and the Secret. It must be a kubernetees name meaning only lowercase letters, digits and hyphens, at most 63 characters
- `namespace` (string): Namespace both objects are created in. The caller will create it
- `environment` (string): Environment both objects belong to, as their environment label
- `data` (map(string)): Settings written into the ConfigMap

## Outputs

- `config_map_name`: Name of the ConfigMap this module created.
- `secret_name`: Name of the Secret this module created.
- `setting_keys`: Keys of the ConfigMap, in sorted order.

## Example

```hcl
module "api_env" {
  source = "../../modules/settings"

  name        = "api-env"
  namespace   = kubernetes_namespace_v1.env.metadata[0].name
  environment = terraform.workspace
  data = {
    SERVICE = "api"
  }
}
```
