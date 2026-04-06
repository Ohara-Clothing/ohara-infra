import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as path from 'path';
import { BaseConstructProps } from '../../types';
import * as integrations from "aws-cdk-lib/aws-apigatewayv2-integrations";

import * as dotenv from "dotenv";
dotenv.config();

export interface MainLambdaConstructProps extends BaseConstructProps {
  dataBucket: s3.Bucket;
  userPool: cognito.IUserPool;
  userPoolClient: cognito.IUserPoolClient;
  corsOrigins?: string[];
}

export class MainLambdaConstruct extends Construct {
  public lambdaFunction: lambda.Function;

  public mainLambdaIntegration: integrations.HttpLambdaIntegration;

  constructor(scope: Construct, id: string, props: MainLambdaConstructProps) {
    super(scope, id);

    const lambdaPath = path.join(__dirname, '../../../lambdas/mainAPI');

    this.lambdaFunction = new lambda.Function(
      this,
      `${props.stage}-MainApiLambda`,
      {
        functionName: `${props.stage}-ohara-main-api`,
        runtime: lambda.Runtime.PYTHON_3_12,
        handler: 'main.handler', // The handler function in main.py
        architecture: lambda.Architecture.X86_64,
        memorySize: 1024,
        timeout: cdk.Duration.seconds(30),
        code: lambda.Code.fromAsset(lambdaPath, {
          exclude: [
            '**/__pycache__',
            '.venv',
            '.pytest_cache',
            '.git',
            'node_modules',
            '.env',
            '*.pyc',
          ],
          bundling: {
            image: lambda.Runtime.PYTHON_3_12.bundlingImage,
            command: [
              'bash', '-c',
              'cp -au . /asset-output && ' +
              'pip install --no-cache-dir -r requirements.txt -t /asset-output && ' +
              'rm -rf /asset-output/.venv /asset-output/venv /asset-output/__pycache__'
            ],
          },
        }),

        environment: {
          STAGE: props.stage,
          USER_POOL_ID: props.userPool.userPoolId,
          USER_POOL_CLIENT_ID: props.userPoolClient.userPoolClientId,
          DATA_BUCKET_NAME: props.dataBucket.bucketName,
          CORS_ORIGINS: props.corsOrigins ? props.corsOrigins.join(',') : '',
          DATABASE_URL: process.env.DATABASE_URL || '',
        },
      }
    );

    this.mainLambdaIntegration = new integrations.HttpLambdaIntegration(
      `${props.stage}-MainLambdaIntegration`,
      this.lambdaFunction,
    );

    // Grant necessary permissions to the Lambda function
    props.dataBucket.grantReadWrite(this.lambdaFunction);
    props.userPool.grant(this.lambdaFunction, 'cognito-idp:ListUsers'); // Example, adjust permissions as needed
  }
}
