import shutil

import pyderman


def get_chromedriver() -> str:
    executable_path = shutil.which("chromedriver")
    if executable_path is None:
        installed_executable_path = pyderman.install(
            verbose=False, browser=pyderman.chrome
        )

        if not isinstance(installed_executable_path, str):
            raise ValueError("Executable path is not str somehow.")

        executable_path = installed_executable_path

    return executable_path
