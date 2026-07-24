from typing import Any

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="agent_traces")
def agent_traces_source(base_url: str = dlt.config.value) -> Any:
    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
        },
        "resources": [
            {
                "name": "logs",
                "endpoint": {
                    "path": "logs",
                    "data_selector": "logs",
                    "params": {
                        "limit": 1000,
                    },
                    "paginator": {
                        "type": "offset",
                        "limit": 1000,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": "total",
                    },
                },
                "primary_key": "index",
                "write_disposition": "replace",
            },
        ],
    }

    yield from rest_api_resources(config)


def load_agent_traces() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces_pipeline",
        destination="duckdb",
        dataset_name="agent_traces",
    )

    # 20 pages x 1000 rows/page = 20,000 records
    load_info = pipeline.run(agent_traces_source().add_limit(20))
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_agent_traces()
