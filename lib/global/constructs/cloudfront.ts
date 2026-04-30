import * as s3 from "aws-cdk-lib/aws-s3";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
import { Construct } from "constructs";
import { Fn } from "aws-cdk-lib";

interface CloudFrontConstructProps {
  stage: string;
  websiteBucket?: s3.Bucket;
  dataBucket?: s3.Bucket;
  apiEndpoint?: string;
}

export class CloudFrontConstruct extends Construct {
  public webDistribution?: cloudfront.Distribution;
  public apiDistribution?: cloudfront.Distribution;
  public dataDistribution?: cloudfront.Distribution;

  constructor(scope: Construct, id: string, props: CloudFrontConstructProps) {
    super(scope, id);

    if (props.websiteBucket) {
      this.createWebDistribution(props);
    }

    if (props.apiEndpoint) {
      this.createApiDistribution(props);
    }

    if (props.dataBucket) {
      this.createDataDistribution(props);
    }
  }

  private createWebDistribution(props: CloudFrontConstructProps) {
    if (!props.websiteBucket) {
      return;
    }

    this.webDistribution = new cloudfront.Distribution(
      this,
      `${props.stage}-Web-Cloudfront-Distribution`,
      {
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(props.websiteBucket),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        },
        defaultRootObject: "index.html",
        errorResponses: [
          {
            httpStatus: 403,
            responsePagePath: "/index.html",
            responseHttpStatus: 200,
          },
          {
            httpStatus: 404,
            responsePagePath: "/index.html",
            responseHttpStatus: 200,
          },
        ],
      },
    );
  }

  private createApiDistribution(props: CloudFrontConstructProps): void {
    if (!props.apiEndpoint) {
      return;
    }

    const urlParts = Fn.split("://", props.apiEndpoint);
    const domainAndPath = Fn.select(1, urlParts);
    const domain = Fn.select(0, Fn.split("/", domainAndPath));

    this.apiDistribution = new cloudfront.Distribution(
      this,
      `${props.stage}-Api-Cloudfront-Distribution`,
      {
        defaultBehavior: {
          origin: new origins.HttpOrigin(domain),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
        },
      },
    );
  }

  private createDataDistribution(props: CloudFrontConstructProps): void {
    if (!props.dataBucket) {
      return;
    }

    this.dataDistribution = new cloudfront.Distribution(
      this,
      `${props.stage}-Data-Cloudfront-Distribution`,
      {
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(props.dataBucket),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
      },
    );
  }
}
