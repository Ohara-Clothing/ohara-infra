import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { GlobalStackProps } from '../types';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class GlobalStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: GlobalStackProps) {
    super(scope, id, props);

    // CloudFront for frontend assets
    const distribution = new cloudfront.Distribution(
      this,
      `${props.stage}-CloudFront-Distribution`,
      {
        defaultBehavior: {
          origin: new origins.S3Origin(props.frontendBucket as s3.Bucket), // Cast to s3.Bucket as it's IBucket
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        },
        defaultRootObject: 'index.html',
        errorResponses: [
          {
            httpStatus: 403,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
          },
          {
            httpStatus: 404,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
          },
        ],
      }
    );

    new cdk.CfnOutput(this, 'CloudFront-Distribution-DomainName', {
      value: distribution.distributionDomainName,
    });

    new cdk.CfnOutput(this, 'API-Endpoint-Output', {
      value: props.apiEndpoint,
    });
  }
}
