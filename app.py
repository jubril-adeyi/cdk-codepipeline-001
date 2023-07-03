#!/usr/bin/env python3
import os

import aws_cdk as cdk

from codepipline.codepipline_stack import CodepiplineStack


app = cdk.App()
CodepiplineStack(app, "CodepiplineStack",
    )




    

app.synth()
