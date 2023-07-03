from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codecommit as codecommit,
)
from constructs import Construct

class CodepipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the CodePipeline pipeline
        self.pipeline = codepipeline.Pipeline(self, "MyPipeline")
        source_output = codepipeline.Artifact("SourceOutput")
        build_output = codepipeline.Artifact("BuildOutput")
        
        #SOURCE
        # Define your pipeline source stage - ADD stage to pipline
        self.source_stage = self.pipeline.add_stage(stage_name="Source")

        # Define action for source stage (Github)
        # source_action = codepipeline_actions.GitHubSourceAction(
        #     action_name="SourceAction",
        #     owner="your-github-username",
        #     repo="your-github-repo",
        #     oauth_token=core.SecretValue.secrets_manager("github-token"),
        #     output=source_output
        # )

        # Define action for source stage (Codecommit)
        self.source_repo = codecommit.Repository.from_repository_name(
            self,
            "MyCodeCommitRepo",
            "codecommit-001"
        )
        self.source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="SourceAction",
            repository=self.source_repo,
            output=source_output
        )

        # Add defined action to source stage
        self.source_stage.add_action(self.source_action)


        #BUILD

        # Define your pipeline build stage - ADD stage to pipline
        self.build_stage = self.pipeline.add_stage(stage_name="Build")
        
        # Define action for build stage 
        self.build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildAction",
            project=your_codebuild_project,
            input=source_output,
            outputs=[build_output]
        )

        # Add defined action to Build stage
        self.build_stage.add_action(self.build_action)
  




    