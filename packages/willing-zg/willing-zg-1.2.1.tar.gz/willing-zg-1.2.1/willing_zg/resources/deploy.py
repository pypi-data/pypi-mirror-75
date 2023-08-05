#!/usr/bin/env python

import argparse
from zygoat.utils.files import repository_root, use_dir
from zygoat.utils.shell import run
from zygoat.constants import Projects
from zygoat.utils.printing import log
from zygoat.config import Config

ECR_REPO_PREFIX = "818831340115.dkr.ecr.us-east-1.amazonaws.com"


def main(args):
    config = Config()
    with repository_root():
        with use_dir(Projects.BACKEND):
            log.info(f"Updating {args.environment} backend")
            run(["zappa", "update", args.environment])

            log.info(f"Running migrations for {args.environment}")
            run(["zappa", "manage", args.environment, "migrate"])

        with use_dir(Projects.FRONTEND):
            log.info("Building frontend")
            image_name = f"{config.name}-frontend"
            latest = f"{image_name}:latest"
            run(["docker", "build", "-t", f"{image_name}", "."])
            run(
                [
                    "docker",
                    "tag",
                    f"{config.name}-frontend:latest",
                    f"{ECR_REPO_PREFIX}/{latest}",
                ]
            )
            run(["docker", "push", f"{ECR_REPO_PREFIX}/{latest}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("environment")
    main(parser.parse_args())
