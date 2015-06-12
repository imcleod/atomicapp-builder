import logging

import dock
from dock import api as dapi

logger = logging.getLogger(__name__)


class Builder(object):
    def __init__(self, build_image, df_path, image_name, tag=None,
            registry=None, registry_insecure=False):
        self.build_image = build_image
        self.df_path = df_path
        self.image_name = image_name
        self.tag = tag
        self.registry = registry
        self.registry_insecure = registry_insecure

    def build(self, wait=True, log_level=logging.INFO):
        """Build Docker image using dock.

        :param wait: currently unused
        :param log_level: log level at which error messages will be printed

        :return: dock's BuildResults object
        """
        tag = self.tag or self.image_name.to_str()
        target_registries = [self.registry] if self.registry else None

        dock.set_logging(level=log_level)
        logger.info('Building image "{0}"'.format(tag))
        response = dapi.build_image_using_hosts_docker(
            self.build_image,
            {'provider': 'path', 'uri': 'file://' + self.df_path},
            tag,
            target_registries=target_registries,
            target_registries_insecure=self.registry_insecure
        )

        # TODO: handle "wait"
        return response
