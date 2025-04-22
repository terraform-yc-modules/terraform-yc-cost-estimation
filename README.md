# Terraform YC Cost Estimation
Resource cost estimation based on the Terraform plan for Yandex Cloud.

List of supported resources:
```
yandex_compute_instance
yandex_compute_instance_group
yandex_compute_disk
yandex_compute_filesystem
yandex_kubernetes_cluster
yandex_kubernetes_node_group
yandex_mdb_mysql_cluster
yandex_mdb_postgresql_cluster
yandex_mdb_clickhouse_cluster
yandex_mdb_greenplum_cluster
yandex_mdb_kafka_cluster
yandex_mdb_redis_cluster
yandex_mdb_opensearch_cluster
yandex_ydb_database_dedicated
yandex_vpc_address
```

> Only `ru-central` Yandex Cloud installation is currently supported. The output is in RUB currency.

# Demo

Prerequisites:
- jq
- curl
- Terraform plan

Generate JSON file from Terraform plan:
```
terraform plan -out=plan.tfplan > /dev/null && terraform show -json plan.tfplan > plan.json
```

Send the plan to get cost estimation results:
```
curl -H "Content-Type: application/json" "https://tf.kirsh.cloud" -d @plan.json | jq
```

Result should look like this:
```
{
  "current": {
    "hourly": 0,
    "monthly": 0
  },
  "planned": {
    "hourly": 514.58,
    "monthly": 382844.5
  },
  "difference": {
    "hourly": 514.58,
    "monthly": 382844.5,
    "percentage": 0
  },
  "currency": "RUB",
  "has_changes": true
}
```
You can also get the full results like this:
```
curl -H "Content-Type: application/json" "https://tf.kirsh.cloud?full=true" -d @plan.json | jq
```
Which should look like this:
```
{
  "current": {
    "hourly": 0,
    "monthly": 0
  },
  "planned": {
    "hourly": 514.58,
    "monthly": 382844.5
  },
  "difference": {
    "hourly": 514.58,
    "monthly": 382844.5,
    "percentage": 0
  },
  "currency": "RUB",
  "has_changes": true,
  "current_usage": [],
  "planned_usage": [
    {
      "sku_id": "dn27ajm6m8mnfcshbi61",
      "sku_name": "Fast network storage (SSD)",
      "amount": 10,
      "cost": 0.1654166,
      "unit": "gbyte*hour",
      "resource_name": "vm-disk-1",
      "resource_type": "yandex_compute_disk"
    }
    ...
  ]
}
```

# Deployment

## SKU

For the script to work you need to get SKU data like this:

```
cd functions
python get-sku.py $(yc iam create-token)
```
This will generate `sku.json` required for the script to work.

> You need YC CLI installed and initialized.

## Local

You can run the script locally like this:
```
cd functions
python app.py /path/plan.json
```

To display full details you can run the script like this:
```
python app.py /path/plan.json --full
```

This will print the cost estimations in table format.

> Python `tabulate` package is recommended to have installed, but the script can work without it.

## Cloud

You can deploy this code as a Cloud Function in Yandex Cloud using Terraform module provided.

- Generate `sku.json` file as described above.
- Create a service account with `editor` role in cloud folder (or with more specific roles, if needed).
- Create `key.json` file for service account authentication.
- Alternatively, use OAuth authentication in Terraform provider.
- Provide `cloud_id` and `folder_id` as required in `variables.tf`.

Deploy terraform module:
```
cd deploy
terraform init
terraform apply
```

This will create a Cloud Function and an API Gateway for access.

You can send the requests to the API Gateway FQDN, as described in the **Demo** section.
