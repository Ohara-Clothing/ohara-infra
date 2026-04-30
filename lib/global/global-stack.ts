import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { GlobalStackProps } from '../types';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { CloudFrontConstruct } from './constructs/cloudfront';

export class GlobalStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: GlobalStackProps) {
    super(scope, id, props);

    const cloudfront = new CloudFrontConstruct(this, 'CloudFront', {
      stage: props.stage,
      websiteBucket: props.frontendBucket as s3.Bucket,
      dataBucket: props.dataBucket as s3.Bucket,
      apiEndpoint: props.apiEndpoint,
    });

    new cdk.CfnOutput(this, 'Web-CloudFront-Distribution-DomainName', {
      value: cloudfront.webDistribution.distributionDomainName,
    });

    new cdk.CfnOutput(this, 'API-CloudFront-Distribution-DomainName', {
      value: cloudfront.apiDistribution.distributionDomainName,
    });

    new cdk.CfnOutput(this, 'Data-CloudFront-Distribution-DomainName', {
      value: cloudfront.dataDistribution.distributionDomainName,
    });

    new cdk.CfnOutput(this, 'API-Endpoint-Output', {
      value: props.apiEndpoint,
    });
  }
}
