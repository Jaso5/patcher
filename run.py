from common import *
import sys
import shutil


if __name__ == "__main__":
    actions = ("setup", "makePatches", "applyPatches")

    if len(sys.argv) <= 1 or sys.argv[1] not in actions:
        print("Usage: python run.py [{}]".format("|".join(actions)))
        sys.exit(1)

    action = sys.argv[1]
    pre_init()

    if action == "setup":
        if Constants.PROJECT_DIR.is_dir():
            print("Project directory already exists. Please delete the folder and run setup again.")
            sys.exit(1)

        # remove previous work dir
        shutil.rmtree(Constants.WORK_DIR, ignore_errors=True)
        Constants.ensure_dirs()

        # download and decompile
        jar_path = Constants.DOWNLOADS_DIR / "minigui.jar"
        download_server_jar(jar_path)

        decompile(jar_path, Constants.DECOMPILE_DIR)

        # TODO: apply patches after setup

        # initialize project directory
        Constants.PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        src = Constants.PROJECT_DIR / "src"
        shutil.copytree(Constants.DECOMPILE_DIR, src)
