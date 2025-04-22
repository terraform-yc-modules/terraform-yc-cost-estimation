# Various
data "archive_file" "function" {
  type        = "zip"
  source_dir  = "${path.module}/../functions"
  output_path = "${path.module}/functions.zip"
}

resource "random_string" "suffix" {
  length  = 4
  upper   = false
  lower   = true
  numeric = true
  special = false
}

# Cloud Function
resource "yandex_function" "main" {
  folder_id          = var.folder_id
  name               = "tfcost-${random_string.suffix.result}"
  runtime            = "python312"
  entrypoint         = "main.handler"
  memory             = "128"
  execution_timeout  = "60"

  user_hash = data.archive_file.function.output_base64sha256
  content {
    zip_filename = data.archive_file.function.output_path
  }
}

resource "yandex_iam_service_account" "invoker" {
  folder_id       = var.folder_id
  name            = "tfcost-invoker-${random_string.suffix.result}"
  description     = "tfcost-invoker-${random_string.suffix.result}"
}

resource "yandex_resourcemanager_folder_iam_member" "invoker" {
  folder_id       = var.folder_id
  member          = "serviceAccount:${yandex_iam_service_account.invoker.id}"
  role            = "functions.functionInvoker"
}

# API gateway
resource "yandex_api_gateway" "gw" {
  name = "tfcost-${random_string.suffix.result}"
  spec = <<-EOT
    openapi: 3.0.0
    info:
      title: Terraform Cost Estimation API
      version: 1.0.0

    paths:
      /:
        post:
          x-yc-apigateway-integration:
            payload_format_version: '1.0'
            function_id: ${yandex_function.main.id}
            tag: $latest
            type: cloud_functions
            service_account_id: ${yandex_iam_service_account.invoker.id}
  EOT
}