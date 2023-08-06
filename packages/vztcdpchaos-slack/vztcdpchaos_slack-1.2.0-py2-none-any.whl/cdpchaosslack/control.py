# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Activity, Configuration, Experiment, Hypothesis, \
    Journal, Run, Secrets
from logzero import logger

from . import push_to_slack_channel

__all__ = ["configure_control", "before_experiment_control",
           "after_experiment_control", "after_hypothesis_control",
           "after_method_control", "after_rollback_control",
           "after_activity_control"]

#with_logging = threading.local()

def configure_control(configuration: Configuration, secrets: Secrets):

    token = secrets.get("slack", {}).get("token", "").strip()
    if not token:
        logger.info("Missing slack token secret")
        #with_logging.__setattr__(False)
        return

    channel = secrets.get("slack", {}).get("channel", "").strip()
    if not channel:
        logger.info("Missing slack channel")
        #with_logging.__setattr__(False)
        return

    logger.debug(f'Slack logging to channel {channel} is enabled for this session')
    #with_logging.__setattr__(True)


def before_experiment_control(context: Experiment, secrets: Secrets):
    """
    Send the experiment
    """
    # if not with_logging.__getattribute__():
    #     return

    event = {
        "name": "before-experiment",
        "context": context,

    }
    #push_to_slack_channel(event=event, secrets=secrets, configuration=None)


def after_experiment_control(context: Experiment, state: Journal,
                             secrets: Secrets, configuration: Configuration):
    """
    Send the experiment's journal
    """
    # if not with_logging.enabled:
    #     return

    event = {
        "name": "after-experiment",
        "context": context,
        "state": state
    }
    push_to_slack_channel(event=event, secrets=secrets, configuration=configuration)


def after_hypothesis_control(context: Hypothesis, state: Dict[str, Any],
                             secrets: Secrets):
    """
    Send the steady-state hypothesis's result
    """
    # if not with_logging.enabled:
    #     return

    event = {
        "name": "after-hypothesis",
        "context": context,
        "state": state,
        "type": "hypothesis"
    }
    #push_to_slack_channel(event=event, secrets=secrets, configuration=None)


def after_method_control(context: Experiment, state: List[Run],
                         secrets: Secrets):
    """
    Send the method's result
    """
    # if not with_logging.enabled:
    #     return

    event = {
        "name": "after-method",
        "context": context,
        "state": state,
        "type": "method"
    }
    #push_to_slack_channel(event=event, secrets=secrets, configuration=None)


def after_rollback_control(context: Experiment, state: List[Run],
                           secrets: Secrets):
    """
    Send the rollback's result
    """
    # if not with_logging.enabled:
    #     return

    event = {
        "name": "after-rollback",
        "context": context,
        "state": state,
        "type": "rollback"
    }
    #push_to_slack_channel(event=event, secrets=secrets, configuration=None)


def after_activity_control(context: Activity, state: Run,
                           secrets: Secrets):
    """
    Send each activity's result
    """
    # if not with_logging.enabled:
    #     return

    event = {
        "name": "after-activity",
        "context": context,
        "state": state,
        "type": "activity"
    }

    #push_to_slack_channel(event=event, secrets=secrets, configuration=None)
