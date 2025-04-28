## Task 02
Based on the official example: https://github.com/fluxcd/flux2-multi-tenancy/

The key ideas are:
- Tenant isolation
  - Enable tenant isolation features, configured in [flux-system/kustomization.yaml](clusters/production/flux-system/kustomization.yaml)
    - Disable cross namespace references
    - Disallow Kustomize remote bases
  - Make sure default service account, without any privileges, is used as fallback by controllers
- Notifications
  - Per tenant, each team receives notifications about their environment
  - Create Providers and Alerts for each tenant
    - Create [Provider](tenants/base/common/pagerduty-provider.yaml) and [Alert](tenants/base/common/pagerduty-alert.yaml) for Pagerduty
    - Create [Provider](tenants/base/common/rocketchat-provider.yaml) and [Alert](tenants/base/common/rocketchat-alert.yaml) for Rocketchat

The templates also contain some code for Task-04 to add tenant labels to all resources created/owned by the tenant.


## Enforce tenant isolation

To enforce tenant isolation, cluster admins must configure Flux to reconcile 
the `Kustomization` and `HelmRelease` kinds by impersonating a service account
from the namespace where these objects are created. 

Flux has built-in [multi-tenancy lockdown] features which enables tenant isolation 
at Control Plane level without the need of external admission controllers (e.g. Kyverno). The
recommended patch:

- Enforce controllers to block cross namespace references.
  Meaning that a tenant can’t use another tenant’s sources or subscribe to their events.
- Deny accesses to Kustomize remote bases, thus ensuring all resources refer to local files. 
  Meaning that only approved Flux Sources can affect the cluster-state.
- Sets a default service account via `--default-service-account` to `kustomize-controller` and `helm-controller`.
  Meaning that, if a tenant does not specify a service account in a Flux `Kustomization` or 
  `HelmRelease`, it would automatically default to said account. 

> **NOTE:** It is recommended that the default service account has no privileges.
> And each named service account used observes the least privilege model.

This repository applies this patch automatically via
[kustomization.yaml](clusters/production/flux-system/kustomization.yaml) in both clusters.
