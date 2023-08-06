# Docoseco

**Do**cker-**co**mpose **se**crets and **co**nfigs.

Automatize management of docker confgs and secrets.

## Usage

```
docoseco [CONFIG_ROOT_DIR] < docker-compose.template.yaml > docker-compose.yaml

  CONFIG_ROOT_DIR  Root directory for file search (default: .)
```

It reads docker-compose yaml from stdin, updates all config and secret names with corresponding file content hashsums and writes result to stdout.

## Rationale

Docker-compose configs and secrets are immutable by design. So, when config or secret is created from file via
`docker stack deploy`, it's impossible to update the file and deploy in the same way again. For example:

```yaml
# docker-compose.yaml
version: "3.8"
services:
  redis:
    image: redis:latest
    configs:
      - source: my_config
        target: /redis_config
configs:
  my_config:
    file: ./my_config.txt
```

If, after the initial deployment, `my_config.txt` is changed, the next deployment attempt will fail.

The common workaround is creating a new config, when a source file changes.
This is done by changing config name:

```yaml
# docker-compose.yaml
...
configs:
  my_config:
    name: my_config-2     # Changing name creates new docker config
    file: ./my_config.txt # This file was changed
```

To avoid manual management of config names, numerical suffix might be replaced by a file content hashsum, which can be automatically calculated.

```yaml
# docker-compose.yaml
...
configs:
  my_config:
    name: my_config-bee414b86ee02806b17104813d44eea4 # Auto-generated config name
    file: ./my_config.txt # This file was changed
```

