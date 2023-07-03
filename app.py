#!/usr/bin/env python3
import os

import aws_cdk as cdk

from codepipeline.codepipline_stack import CodepipelineStack


app = cdk.App()
CodepipelineStack(app, "CodepipelineStack",
    )




    

app.synth()
