from dataclasses import dataclass


@dataclass
class Origin:
    origin_cloud_provider: str = ""
    origin_cloud_account_subscription_project: str = ""
    origin_cloud_resource: str = ""
    origin_cloud_resource_type: str = ""
    origin_kubernetes_namespace: str = ""
    origin_kubernetes_resource_type: str = ""
    origin_kubernetes_resource_name: str = ""
