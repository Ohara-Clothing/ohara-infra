import * as cdk from 'aws-cdk-lib';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';
import { BaseConstructProps } from '../../types';

export interface CognitoConstructProps extends BaseConstructProps {}

export class CognitoConstruct extends Construct {
  public userPool: cognito.UserPool;
  public userPoolClient: cognito.UserPoolClient;

  constructor(scope: Construct, id: string, props: CognitoConstructProps) {
    super(scope, id);

    this.createUserPool(props);
    this.createUserPoolClient(props);
  }

  private createUserPool(props: CognitoConstructProps): void {
    this.userPool = new cognito.UserPool(this, `${props.stage}-UserPool`, {
      userPoolName: `${props.stage}-ohara-users`,
      selfSignUpEnabled: true,
      signInAliases: {
        email: true,
        username: true,
      },
      autoVerify: {
        email: true,
      },
      standardAttributes: {
        email: {
          required: true,
          mutable: true,
        },
      },
      passwordPolicy: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
      },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
      removalPolicy:
        props.stage === 'dev'
          ? cdk.RemovalPolicy.DESTROY
          : cdk.RemovalPolicy.RETAIN,
    });
  }

  private createUserPoolClient(props: CognitoConstructProps): void {
    this.userPoolClient = new cognito.UserPoolClient(
      this,
      `${props.stage}-UserPoolClient`,
      {
        userPool: this.userPool,
        userPoolClientName: `${props.stage}-ohara-client`,
        generateSecret: false,
        authFlows: {
          userPassword: true,
          userSrp: true,
        },
      }
    );
  }
}
