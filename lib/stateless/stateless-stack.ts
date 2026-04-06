import * as cdk from "aws-cdk-lib";

import { Construct } from "constructs";
import { MainLambdaConstruct } from "./constructs/mainLambda";
import { ApiGatewayConstruct } from "./constructs/apiGateway";
import { StatelessStackProps } from "../types";

export class StatelessStack extends cdk.Stack {
  public apiGatewayConstruct: ApiGatewayConstruct;

  private lambdaConstruct: MainLambdaConstruct;

  constructor(scope: Construct, id: string, props: StatelessStackProps) {
    super(scope, id, props);

    this.createLambdaConstruct(props);
    this.createApiGatewayConstruct(props);
    // this.createCloudWatchConstruct(props);
    // this.createSqsConstruct(props);
    // this.createSnsConstruct(props);
  }

  private createLambdaConstruct(props: StatelessStackProps): void {
    this.lambdaConstruct = new MainLambdaConstruct(
      this,
      `${props.stage}-Lambda-Construct`,
      {
        stage: props.stage,
        dataBucket: props.dataBucket,
        userPool: props.userPool,
        userPoolClient: props.userPoolClient,
      },
    );
  }

  private createApiGatewayConstruct(props: StatelessStackProps): void {
    this.apiGatewayConstruct = new ApiGatewayConstruct(
      this,
      `${props.stage}-ApiGateway-Construct`,
      {
        stage: props.stage,
        userPool: props.userPool,
        userPoolClient: props.userPoolClient,
        corsOrigins: props.corsOrigins,
        mainLambdaIntegration: this.lambdaConstruct.mainLambdaIntegration,
      },
    );
  }

  // private createSqsConstruct(props: StatelessStackProps): void {
  //   this.sqsConstruct = new SqsConstruct(this, `${props.stage}-SQS-Construct`, {
  //     stage: props.stage,
  //   });
  // }
  //
  // private createSnsConstruct(props: StatelessStackProps) {
  //   this.snsConstruct = new SnsConstruct(this, `${props.stage}-SNS-Construct`, {
  //     stage: props.stage,
  //   });
  // }
  //
  // private createCloudWatchConstruct(props: StatelessStackProps): void {
  //   this.cloudWatchConstruct = new CloudwatchConstruct(
  //     this,
  //     `${props.stage}-CloudWatch-Construct`,
  //     {
  //       stage: props.stage,
  //       sampleDlq: this.sqsConstruct.sampleDlq,
  //       errorAlertTopic: this.snsConstruct.errorAlertTopic,
  //     },
  //   );
  // }
}
