from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_iam as iam,
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

        # Define existing build project 
        # cfn_lint_project_name = "cfn-lint"  # Replace with your CodeBuild project name
        # cfn_lint_project = codebuild.Project.from_project_name(
        #     self,
        #     "MyCodeBuildProject",
        #     cfn_lint_project_name
        # )

        # Define new build

        # Define CodeBuild project with custom Docker image
        custom_image = "slickboy/cdk-nodejs:1.1"
        existing_role_arn = "arn:aws:iam::723389358939:role/service-role/codebuild-build-001-service-role"
        cfn_lint_project = codebuild.Project(
            self,
            "MyCodeBuildProject",
            project_name="cfn-lint-project",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "commands": [
                            "pip3 install cfn-lint",
                            "pip3 install -r requirements.txt",
                        ]
                    },
                    "build": {
                        "commands": [
                            "cdk synth >> template.json",
                            "cfn-lint  template.json",
                        ]
                    }
                }
            }),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.from_docker_registry(custom_image),
                privileged=None  # Set to True if you need elevated privileges
            ),

            role=iam.Role.from_role_arn(
                self,
                "ExistingCodeBuildRole",
                role_arn=existing_role_arn
            )
        )

        # Define your pipeline build stage - ADD stage to pipline
        self.build_stage = self.pipeline.add_stage(stage_name="Build")
        
        # Define action for build stage 
        self.build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildAction",
            project=cfn_lint_project,
            input=source_output,
            outputs=[build_output]
        )

        # Add defined action to Build stage
        self.build_stage.add_action(self.build_action)
  




    