# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Factory class that automatically selects the appropriate cache store."""
import logging
from typing import Optional

from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore

from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.file_cache_store import FileCacheStore, _CacheConstants
from azureml.automl.runtime.shared.memory_cache_store import MemoryCacheStore
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl.runtime._azurefilecachestore import AzureFileCacheStore
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import ArgumentException


logger = logging.getLogger(__name__)


class CacheStoreFactory:

    # TODO: simplify this
    @staticmethod
    def get_cache_store(temp_location: str,
                        run_target: str,
                        run_id: str,
                        data_store: Optional[AbstractAzureStorageDatastore] = None,
                        task_timeout: int = _CacheConstants.DEFAULT_TASK_TIMEOUT_SECONDS) -> CacheStore:
        """Get the cache store based on run type."""
        try:
            if run_id is None:
                return MemoryCacheStore()

            if data_store is not None and run_target is not "local":
                return AzureFileCacheStore(
                    path=run_id,
                    account_key=data_store.account_key,
                    account_name=data_store.account_name,
                    endpoint_suffix=data_store.endpoint,
                    temp_location=temp_location,
                    task_timeout=task_timeout)

            return FileCacheStore(
                path=temp_location,
                task_timeout=task_timeout)
        except Exception as e:
            logging_utilities.log_traceback(e, logger, is_critical=False)
            logger.warning("Failed to get store, fallback to memorystore {}".format(run_id))

        return MemoryCacheStore()
