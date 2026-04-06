import * as cdk from "aws-cdk-lib";
import { StatelessStack } from "../../lib/stateless/stateless-stack";
import { StatefulStack } from "../../lib/stateful/stateful-stack";
import { GlobalStack } from "../../lib/global/global-stack";

export interface EnvironmentConfig {
  Stateful: any;
  Stateless: any;
  Global: any;
}

export function setupEnvironment(
  app: cdk.App,
  envConfig: EnvironmentConfig,
): {
  statefulStack: StatefulStack;
  statelessStack: StatelessStack;
  globalStack: GlobalStack;
} {
  const statefulStack = new StatefulStack(
    app,
    `${envConfig.Stateful.stage}-StatefulStack`,
    {
      ...envConfig.Stateful,
    },
  );

  const statelessStack = new StatelessStack(
    app,
    `${envConfig.Stateless.stage}-StatelessStack`,
    {
      ...envConfig.Stateless,
      crossRegionReferences: true,
      dataBucket: statefulStack.s3Construct.dataBucket,
      userPool: statefulStack.cognitoConstruct.userPool,
      userPoolClient: statefulStack.cognitoConstruct.userPoolClient,
      corsOrigins: envConfig.Stateless.corsOrigins,
      dbUser: envConfig.Stateless.dbUser,
      dbPassword: envConfig.Stateless.dbPassword,
      dbHost: envConfig.Stateless.dbHost,
      dbPort: envConfig.Stateless.dbPort,
      dbName: envConfig.Stateless.dbName,
    },
  );

  const globalStack = new GlobalStack(
    app,
    `${envConfig.Global.stage}-GlobalStack`,
    {
      ...envConfig.Global,
      crossRegionReferences: true,
      apiEndpoint: statelessStack.apiGatewayConstruct.api.apiEndpoint,
      frontendBucket: statefulStack.s3Construct.assetsBucket, // Using assetsBucket for frontend
    },
  );

  return { statefulStack, statelessStack, globalStack };
}
