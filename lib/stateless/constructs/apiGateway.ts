import * as api from "aws-cdk-lib/aws-apigatewayv2";
import * as integrations from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { HttpUserPoolAuthorizer } from "aws-cdk-lib/aws-apigatewayv2-authorizers";
import * as cognito from "aws-cdk-lib/aws-cognito";
import { Construct } from "constructs";
import { BaseConstructProps } from "../../types";

export interface ApiGatewayConstructProps extends BaseConstructProps {
  userPool: cognito.IUserPool;
  userPoolClient: cognito.IUserPoolClient;
  corsOrigins?: string[];
  mainLambdaIntegration: integrations.HttpLambdaIntegration;
}

export class ApiGatewayConstruct extends Construct {
  public api: api.HttpApi;
  private authorizer: HttpUserPoolAuthorizer;

  constructor(scope: Construct, id: string, props: ApiGatewayConstructProps) {
    super(scope, id);

    this.authorizer = new HttpUserPoolAuthorizer(
      `${props.stage}-Cognito-HttpApi-Authorizer`,
      props.userPool,
      {
        userPoolClients: [props.userPoolClient],
      },
    );

    this.createApiGateway(props);
    this.createApiRoutes(props);
  }

  private createApiGateway(props: ApiGatewayConstructProps): void {
    this.api = new api.HttpApi(this, `${props.stage}-ApiGateway-HttpApi`, {
      apiName: `${props.stage}-ApiGateway-HttpApi`,
      corsPreflight: {
        allowOrigins: props.corsOrigins ?? ["*"],
        allowMethods: [
          api.CorsHttpMethod.GET,
          api.CorsHttpMethod.POST,
          api.CorsHttpMethod.PUT,
          api.CorsHttpMethod.PATCH,
          api.CorsHttpMethod.DELETE,
          api.CorsHttpMethod.OPTIONS,
        ],
        allowHeaders: ["Content-Type", "Authorization", "X-Api-Key"],
      },
    });
  }

  private createApiRoutes(props: ApiGatewayConstructProps): void {
    this.api.addRoutes({
      path: "/",
      methods: [api.HttpMethod.GET],
      integration: props.mainLambdaIntegration,
    });

    // USER ROUTES ==================================
    this.api.addRoutes({
      path: "/getUsers",
      methods: [api.HttpMethod.GET],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/createUser",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/confirmUser",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/login",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/logout",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/refreshToken",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/deleteUser",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
      authorizer: this.authorizer,
    });

    this.api.addRoutes({
      path: "/forgetPass",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/forgetPassConfirm",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    // CLOTHES ROUTES ===============================
    this.api.addRoutes({
      path: "/clothes",
      methods: [api.HttpMethod.GET],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/clothes",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/clothes/{clothes_id}",
      methods: [api.HttpMethod.PATCH],
      integration: props.mainLambdaIntegration,
      authorizer: this.authorizer,
    });

    this.api.addRoutes({
      path: "/clothes/{clothes_id}",
      methods: [api.HttpMethod.DELETE],
      integration: props.mainLambdaIntegration,
      authorizer: this.authorizer,
    });

    // FITS ROUTES ===============================
    this.api.addRoutes({
      path: "/fits",
      methods: [api.HttpMethod.GET],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/fits",
      methods: [api.HttpMethod.POST],
      integration: props.mainLambdaIntegration,
    });

    this.api.addRoutes({
      path: "/fits/{fits_id}",
      methods: [api.HttpMethod.PATCH],
      integration: props.mainLambdaIntegration,
      authorizer: this.authorizer,
    });

    this.api.addRoutes({
      path: "/fits/{fits_id}",
      methods: [api.HttpMethod.DELETE],
      integration: props.mainLambdaIntegration,
      authorizer: this.authorizer,
    });
  }
}
