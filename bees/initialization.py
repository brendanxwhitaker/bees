import os
import json
import pickle
import shutil
import argparse
import datetime
from typing import TextIO, Tuple, Any, Dict
from bees.utils import get_token, validate_args, DEBUG
from bees.config import Config


class Setup:
    def __init__(self, args: argparse.Namespace) -> None:
        validate_args(args)

        trainer_state: Dict[str, Any] = {}
        trainer_state_path: str = ""
        env_state_path: str = ""

        # TODO: Convert everything to abspaths.
        # Resume from previous run.
        if args.load_from:

            # Construct new codename.
            # NOTE: we were going to have the basename be just the token, but this seems
            # ill-advised since you'd have to go into each folder to determine which is
            # newest.
            codename = os.path.basename(os.path.abspath(args.load_from))
            token = codename.split("_")[0]

            # Construct paths.
            env_filename = codename + "_env.pkl"
            trainer_filename = codename + "_trainer.pkl"
            settings_filename = codename + "_settings.json"
            env_state_path = os.path.join(args.load_from, env_filename)
            trainer_state_path = os.path.join(args.load_from, trainer_filename)
            settings_path = os.path.join(args.load_from, settings_filename)

            # Load trainer state.
            with open(trainer_state_path, "rb") as trainer_file:
                trainer_state = pickle.load(trainer_file)

        # New training run.
        elif args.settings:
            token = get_token(args.save_root)
            date = str(datetime.datetime.now())
            date = date.replace(" ", "_")
            codename = "%s_%s" % (token, date)
            settings_path = args.settings

        else:
            raise ValueError("You must pass a value for ``--settings``.")

        # Load settings dict into Config object.
        with open(settings_path, "r") as settings_file:
            settings = json.load(settings_file)
        config = Config(settings)

        # Construct a new ``save_dir`` in either case.
        save_dir = os.path.join(args.save_root, codename)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        # Construct log paths.
        env_log_filename = codename + "_env_log.txt"
        visual_log_filename = codename + "_visual_log.txt"
        env_log_path = os.path.join(save_dir, env_log_filename)
        visual_log_path = os.path.join(save_dir, visual_log_filename)

        # If ``save_dir`` is not the same as ``load_from`` we must copy the existing logs
        # into the new save directory, then contine to append to them.
        if args.load_from and os.path.abspath(save_dir) not in os.path.abspath(
            env_log_path
        ):
            new_env_log_filename = codename + "_env_log.txt"
            new_visual_log_filename = codename + "_visual_log.txt"
            new_env_log_path = os.path.join(save_dir, new_env_log_filename)
            new_visual_log_path = os.path.join(save_dir, new_visual_log_filename)
            shutil.copyfile(env_log_path, new_env_log_path)
            shutil.copyfile(visual_log_path, new_visual_log_path)
            env_log_path = new_env_log_path
            visual_log_path = new_visual_log_path

        # Open logs.
        env_log = open(env_log_path, "a+")
        visual_log = open(visual_log_path, "a+")

        # Load setup state.
        self.config: Config = config
        self.trainer_state: Dict[str, Any] = trainer_state
        self.env_log: TextIO = env_log
        self.visual_log: TextIO = visual_log
        self.save_dir: str = save_dir
        self.settings_path: str = settings_path
        self.trainer_state_path: str = trainer_state_path
        self.env_state_path: str = env_state_path
        self.codename: str = codename


def train_setup(
    args: argparse.Namespace,
) -> Tuple[Config, Dict[str, Any], TextIO, TextIO, str, str, str, str, str]:
    """ Setup for ``trainer.train()``. """
    validate_args(args)

    trainer_state: Dict[str, Any] = {}
    trainer_state_path: str = ""
    env_state_path: str = ""

    # TODO: Convert everything to abspaths.
    # Resume from previous run.
    if args.load_from:

        # Construct new codename.
        # NOTE: we were going to have the basename be just the token, but this seems
        # ill-advised since you'd have to go into each folder to determine which is
        # newest.
        codename = os.path.basename(os.path.abspath(args.load_from))
        token = codename.split("_")[0]

        # Construct paths.
        env_filename = codename + "_env.pkl"
        trainer_filename = codename + "_trainer.pkl"
        settings_filename = codename + "_settings.json"
        env_state_path = os.path.join(args.load_from, env_filename)
        trainer_state_path = os.path.join(args.load_from, trainer_filename)
        settings_path = os.path.join(args.load_from, settings_filename)

        # Load trainer state.
        with open(trainer_state_path, "rb") as trainer_file:
            trainer_state = pickle.load(trainer_file)

    # New training run.
    elif args.settings:
        token = get_token(args.save_root)
        date = str(datetime.datetime.now())
        date = date.replace(" ", "_")
        codename = "%s_%s" % (token, date)
        settings_path = args.settings

    else:
        raise ValueError("You must pass a value for ``--settings``.")

    # Load settings dict into Config object.
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
    config = Config(settings)

    # Construct a new ``save_dir`` in either case.
    save_dir = os.path.join(args.save_root, codename)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Construct log paths.
    env_log_filename = codename + "_env_log.txt"
    visual_log_filename = codename + "_visual_log.txt"
    env_log_path = os.path.join(save_dir, env_log_filename)
    visual_log_path = os.path.join(save_dir, visual_log_filename)

    # If ``save_dir`` is not the same as ``load_from`` we must copy the existing logs
    # into the new save directory, then contine to append to them.
    if args.load_from and os.path.abspath(save_dir) not in os.path.abspath(
        env_log_path
    ):
        new_env_log_filename = codename + "_env_log.txt"
        new_visual_log_filename = codename + "_visual_log.txt"
        new_env_log_path = os.path.join(save_dir, new_env_log_filename)
        new_visual_log_path = os.path.join(save_dir, new_visual_log_filename)
        shutil.copyfile(env_log_path, new_env_log_path)
        shutil.copyfile(visual_log_path, new_visual_log_path)
        env_log_path = new_env_log_path
        visual_log_path = new_visual_log_path

    # Open logs.
    env_log = open(env_log_path, "a+")
    visual_log = open(visual_log_path, "a+")

    return (
        config,
        trainer_state,
        env_log,
        visual_log,
        save_dir,
        settings_path,
        trainer_state_path,
        env_state_path,
        codename,
    )