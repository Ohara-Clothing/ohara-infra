import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { GlobalStackProps } from '../types';
import { CloudFrontConstruct } from './constructs/cloudfront';

export class GlobalStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: GlobalStackProps) {
    super(scope, id, props);

    const cloudfront = new CloudFrontConstruct(this, 'CloudFront', {
      stage: props.stage,
      apiEndpoint: props.apiEndpoint,
      dataBucket: props.dataBucket,
      assetsBucket: props.assetsBucket,
    });

    new cdk.CfnOutput(this, 'API-CloudFront-Distribution-DomainName', {
      value: cloudfront.apiDistribution!.domainName,
    });

    new cdk.CfnOutput(this, 'API-Endpoint-Output', {
      value: props.apiEndpoint,
    });

    if (cloudfront.assetsDistribution) {
      new cdk.CfnOutput(this, 'Assets-CloudFront-Distribution-DomainName', {
        value: cloudfront.assetsDistribution.attrDomainName,
      });
    }

    if (cloudfront.dataDistribution) {
      new cdk.CfnOutput(this, 'Data-CloudFront-Distribution-DomainName', {
                 value: cloudfront.dataDistribution.attrDomainName,      });
    }
  }
}
