## Task 04

The key ideas are:
- FluxCD is used to deploy resources
- Make sure tenant label `toolkit.fluxcd.io/tenant` is set on k8s resources of each tenant
  - Use commonMetadata field on the [tenant repository sync](../task02/admin-repo/tenants/base/common/sync.yaml)
  - Optional: create ClusterPolicy to prevent creation of resources without specifying tenant label
- Create a resource attribute for the tenant ID in the OTEL config
- Use the tenant-id resource attribute in `X-Scope-OrgID` header to provide tenant isolation in Grafana stack
