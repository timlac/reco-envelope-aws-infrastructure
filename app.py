#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.envelope_stack import EnvelopeStack

app = cdk.App()

env = app.node.try_get_context("env")
env = env if env else 'dev'

EnvelopeStack(app, f"EnvelopeStack-{env}", env=env)

app.synth()
