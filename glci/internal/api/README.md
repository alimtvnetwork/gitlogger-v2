# API contract

`openapi.yaml` here is a **mirror** of `git-logs-plugin/openapi.yaml`.

The plugin file is the source of truth. This copy lets `glci` developers (and future code generators) work without the plugin checked out.

When the plugin's openapi changes, refresh this copy:

```bash
cp ../../git-logs-plugin/openapi.yaml ./openapi.yaml
```

P8 will add a CI check that fails if the two files drift.
