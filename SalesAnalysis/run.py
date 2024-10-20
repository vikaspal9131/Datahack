# Apache Software License 2.0
#
# Copyright (c) ZenML GmbH 2024. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Optional
import click
from main import sales_analysis_pipeline
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)

@click.command(
    help="""
ZenML Sales Analysis Pipeline.

Run the sales analysis pipeline.

Examples:

  \b
  # Run the sales analysis pipeline
    python run.py
"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
def main(no_cache: bool = False):
    """Main entry point for the sales analysis pipeline execution.

    This entry point is where everything comes together:
      * launching the sales analysis pipeline

    Args:
        no_cache: If `True`, caching will be disabled.
    """
    client = Client()


    logger.info("Starting the sales analysis pipeline.")

    # Run the sales analysis pipeline
    sales_analysis_pipeline()  # Call the pipeline directly

if __name__ == "__main__":
    main()