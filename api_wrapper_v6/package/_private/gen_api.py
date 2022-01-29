from package._private.api.manager import api_manager


def _generate_api():
    for factory in api_manager.factories:
        for version in factory.api_versions:
            api = factory.get_api_cls(version)
            print(api)


if __name__ == '__main__':
    _generate_api()
