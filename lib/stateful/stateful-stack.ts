import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { StatefulStackProps } from '../types';
import { S3Construct } from './constructs/s3';
import { CognitoConstruct } from './constructs/cognito';

export class StatefulStack extends cdk.Stack {
  // Public properties exposed for inter-stack references
  public s3Construct: S3Construct;
  public cognitoConstruct: CognitoConstruct;

  constructor(scope: Construct, id: string, props: StatefulStackProps) {
    super(scope, id, props);

    this.createS3Construct(props);
    this.createCognitoConstruct(props);
    this.createOutputs();
  }

  private createS3Construct(props: StatefulStackProps): void {
    this.s3Construct = new S3Construct(this, `${props.stage}-S3-Construct`, {
      stage: props.stage,
    });
  }

  private createCognitoConstruct(props: StatefulStackProps): void {
    this.cognitoConstruct = new CognitoConstruct(
      this,
      `${props.stage}-Cognito-Construct`,
      {
        stage: props.stage,
      }
    );
  }

  private createOutputs(): void {
    new cdk.CfnOutput(this, 'S3-Data-Bucket-Name', {
      value: this.s3Construct.dataBucket.bucketName,
    });

    new cdk.CfnOutput(this, 'S3-Assets-Bucket-Name', {
      value: this.s3Construct.assetsBucket.bucketName,
    });

    new cdk.CfnOutput(this, 'Cognito-UserPool-Id', {
      value: this.cognitoConstruct.userPool.userPoolId,
    });

    new cdk.CfnOutput(this, 'Cognito-UserPool-ClientId', {
      value: this.cognitoConstruct.userPoolClient.userPoolClientId,
    });
  }
}
