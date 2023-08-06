# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import os
import os.path
import platform
from typing import Any, Dict
import json
from chaoslib.types import Configuration, EventPayload, Secrets, Journal
from logzero import logger
import requests
import slack
import json


__all__ = [ "push_to_slack_channel"]



def push_to_slack_channel(event: EventPayload, secrets: Secrets, configuration: Configuration):
    """
    Send the event payload to Slack
    The `secrets` must contain `token` and `channel` properties.
    If any of those two properties are missing, the function logs a message
    and immediately returns.
    """

    #journal_path=os.getcwd()+'journal.json'
    #with io.open(journal_path, "w") as r:
    #    json.dump(
    #        journal, r, indent=2, ensure_ascii=False, default=encoder)


    #if journal_path is None:
    #    journal_path = "journal.json"
    #logger.debug(f'Reading journal.josn file from path**: {journal_path}')
    #with open(journal_path, 'r') as f:
    #    event = json.load(f)

    #event = journal
    #secrets = journal.get('experiment').get('secrets')



    #slack_secrets = secrets.get('slack')
    token = secrets['token']
    channel = secrets['channel']


    if not token:
        logger.info("Slack notifier requires a token")
        return

    if not channel:
        logger.info("Slack notifier requires a channel")
        return

    token = token.strip()
    channel = "#{c}".format(c=channel.lstrip("#").strip())

    sc = slack.WebClient(token=token)

    phase = event.get("phase")

    color = "#439FE0"
    icon = None

    attachments = []
    fields = []
    steady_states_fields = []
    rollbacks_fields = []
    failed_activities_fields = []
    successful_activities_fields = []
    configuration_fields = []


    main_attachement = {
        "fields": fields,
        "color": color,

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }
    attachments.append(main_attachement)

    configuration_attachment = {
        "text": "Configuration",
        "fields": configuration_fields,
        "color": color,

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }

    steady_states_attachment = {
        "text": "Steady State",
        "fields": steady_states_fields,
        "color": color,

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }

    successful_activities_attachment = {
        "text": "Experiment activities",
        "fields": successful_activities_fields,
        "color": color,

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }

    failed_activities_attachment = {
        "text": "Experiment activities",
        "fields": failed_activities_fields,
        "color": "danger",

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }

    rollbacks_attachment = {
        "text": "Rollbacks",
        "fields": rollbacks_fields,
        "color": "danger",

        "footer_icon": icon,
        "footer": "vzt-cdp-chaos"
    }

    fields.append({
        "title": "Source",
        "value": phase,
        "short": True
    })

    payload = event.get("state")
    print(json.dumps(payload))
    if payload and isinstance(payload, dict):
        print(json.dumps(payload.get("experiment")))
        title = payload.get("title")
        if not title:

            title = payload.get("experiment", {}).get("title") + "\n Started at : " + payload.get("start").strip() + "\n Ended at : " + payload.get("end").strip() + "\n Status : " + payload.get("status").strip()
        if title:
            fields.append({
                "title": "Experiment Details",
                "value": title,
                "short": False
            })

        hypo = payload.get("steady-state-hypothesis")
        if not hypo:
            hypo = payload.get("experiment", {}).get("steady-state-hypothesis")
        title = hypo.get("title") if hypo else "N/A"
        steady_states_fields.append({
            "title": "Hypothesis",
            "value": title,
            "short": False
        })

        steady_states = payload.get("steady_states")

        if steady_states and steady_states["before"] is not None and steady_states["after"] is not None:
            before = steady_states["before"]
            met = before["steady_state_met"]
            msg = "Hypothesis successful" if met else "Hypothesis failed"

            steady_states_fields.append({
                "title": "Steady state before the experiment",
                "value": msg,
                "short": False
            })

            if not met:
                steady_states_attachment["color"] = "warning"
                probe = before["probes"][-1]
                msg = probe.get("output")
                if not msg and probe.get("exception"):
                    msg = probe.get("exception")[-1].strip()
                steady_states_fields.append({
                    "title": "Tolerance Output",
                    "value": "```{}```".format(msg),
                    "short": False
                })

            after = steady_states.get("after")
            if after:
                met = after["steady_state_met"]
                msg = "Hypothesis successful" if met else "Hypothesis failed"

                steady_states_fields.append({
                    "title": "Steady state after the experiment",
                    "value": msg,
                    "short": False
                })

                if not met:
                    steady_states_attachment["color"] = "danger"
                    probe = after["probes"][-1]
                    msg = probe.get("output")
                    if not msg and probe.get("exception"):
                        msg = probe.get("exception")[-1].strip()
                    steady_states_fields.append({
                        "title": "Tolerance Output",
                        "value": "```{}```".format(msg),
                        "short": False
                    })
        else:
            steady_states_fields.append({
                "title": "Steady state before the experiment",
                "value": "No Steady State fields defined",
                "short": False
            })


        runs = payload.get("run")
        if runs:
            for run in runs:
                if run["status"] == "failed":
                    failed_activities_attachment["color"] = "danger"
                    msg = run.get("output")
                    if not msg and run.get("exception"):
                        msg = run.get("exception")[-1].strip()
                    failed_activities_fields.append({
                        "title": run.get("activity").get("name"),
                        "value": "```{}```".format(msg),
                        "short": False
                    })
                else:
                    output = run.get("output")
                    if output and isinstance(output, dict):
                        output = run.get("output")
                        if output.get("stdout"):
                            msg = output.get("stdout")
                        else:
                            msg = output
                        successful_activities_fields.append({
                            "title": run.get("activity").get("name"),
                            "value": "```{}```".format(msg),
                            "short": False
                        })
                    elif output:
                        output = run.get("output")
                        successful_activities_fields.append({
                            "title": run.get("activity").get("name"),
                            "value": "```{}```".format(output),
                            "short": False
                        })


        rollbacks = payload.get("rollbacks")
        if rollbacks:
            for rollback in rollbacks:
                if rollback.get("status") == "failed":
                    msg = rollback.get("output")
                    if not msg and rollback.get("exception"):
                        msg = rollback.get("exception")[-1].strip()
                    rollbacks_fields.append({
                        "title": rollback.get("activity").get("name"),
                        "value": "```{}```".format(msg),
                        "short": False
                    })

        configs = payload.get("experiment").get("configuration")
        config_msg = "Platform : " + payload.get("platform").strip() + "\nNode : " + payload.get("node").strip() + "\nEnvironment : " + configs.get("aws_profile_name") + "\nAWS Region : " + configs.get("aws_region") + "\nAWS Cluster : " + configs.get("cluster")

        configuration_fields.append({
            "title": "Host Details",
            "value" : "```{}```".format(config_msg),
            "short": False
            })

        configs = payload.get("experiment").get("configuration")
        config_msg = configs.get("splunk_dashboard")

        configuration_fields.append({
            "title": "Splunk Dashboard",
            "value" : "```{}```".format(config_msg),
            "short": False
            })

    # let's not clutter the view
    if steady_states_fields:
        main_attachement.pop("ts", None)
        main_attachement.pop("footer", None)
        main_attachement.pop("footer_icon", None)
        attachments.append(configuration_attachment)
        attachments.append(steady_states_attachment)


    if successful_activities_fields or failed_activities_fields:
        steady_states_attachment.pop("ts", None)
        steady_states_attachment.pop("footer", None)
        steady_states_attachment.pop("footer_icon", None)
        attachments.append(successful_activities_attachment)
        attachments.append(failed_activities_attachment)



    if rollbacks_fields:
        steady_states_attachment.pop("ts", None)
        steady_states_attachment.pop("footer", None)
        steady_states_attachment.pop("footer_icon", None)
        activities_attachment.pop("ts", None)
        activities_attachment.pop("footer", None)
        activities_attachment.pop("footer_icon", None)
        attachments.append(rollbacks_attachment)

    result = sc.chat_postMessage(channel=channel,
                                 text="Resiliency Experiment",
                                 attachments=attachments)


    if result.get("ok", False) is False:
        logger.error("Slack client call failed")

    # logger.debug(
    #     "Slack client return call: {}".format(json.dumps(result, indent=2)))
