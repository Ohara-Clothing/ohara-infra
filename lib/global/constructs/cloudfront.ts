import * as s3 from "aws-cdk-lib/aws-s3";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
import { Construct } from "constructs";
import { Fn } from "aws-cdk-lib";
import { IBucketAttributes } from "../../types"; // Import the new interface

interface CloudFrontConstructProps {
  stage: string;
  websiteBucket?: s3.IBucket;
  dataBucket?: IBucketAttributes; // Use new interface
  assetsBucket?: IBucketAttributes; // Use new interface
  apiEndpoint?: string;
}

export class CloudFrontConstruct extends Construct {
  public webDistribution?: cloudfront.Distribution;
  public apiDistribution?: cloudfront.Distribution;
  public dataDistribution?: cloudfront.CfnDistribution; // Temporarily removed for debugging
  public assetsDistribution?: cloudfront.CfnDistribution;
  public dataOacArn?: string;
  public assetsOacArn?: string;

  private dataOac?: cloudfront.CfnOriginAccessControl;
  private assetsOac?: cloudfront.CfnOriginAccessControl;
  private webOac?: cloudfront.CfnOriginAccessControl; // New public property

  constructor(scope: Construct, id: string, props: CloudFrontConstructProps) {
    super(scope, id);

    if (props.websiteBucket) {
      this.webOac = new cloudfront.CfnOriginAccessControl(this, `${props.stage}-WebBucket-OAC`, {
        originAccessControlConfig: {
          name: `${props.stage}-WebBucket-OAC`,
          originAccessControlOriginType: 's3',
          signingBehavior: 'always',
          signingProtocol: 'sigv4',
        },
      });
      this.createWebDistribution(props);
    }

    if (props.apiEndpoint) {
      this.createApiDistribution(props);
    }

        if (props.dataBucket) {
          this.createDataDistribution(props);
          this.dataOacArn = this.dataOac!.ref;
        }

        if (props.assetsBucket) {
          this.createAssetsDistribution(props);
          this.assetsOacArn = this.assetsOac!.ref;
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
    const dataBucket = s3.Bucket.fromBucketAttributes(this, `${props.stage}-DataBucket-Ref`, {
      bucketName: props.dataBucket.bucketName,
      bucketArn: props.dataBucket.bucketArn,
      region: props.dataBucket.bucketRegion,
    });

    this.dataOac = new cloudfront.CfnOriginAccessControl(this, `${props.stage}-DataBucket-OAC`, {
      originAccessControlConfig: {
        name: `${props.stage}-DataBucket-OAC`,
        originAccessControlOriginType: 's3',
        signingBehavior: 'always',
        signingProtocol: 'sigv4',
      },
    });

    this.dataDistribution = new cloudfront.CfnDistribution(
      this,
      `${props.stage}-Data-Cloudfront-Distribution`,
      {
        distributionConfig: {
          defaultCacheBehavior: {
            cachePolicyId: cloudfront.CachePolicy.CACHING_OPTIMIZED.cachePolicyId,
            compress: true,
            targetOriginId: `${props.stage}-DataBucketOrigin`,
            viewerProtocolPolicy: 'redirect-to-https',
          },
          enabled: true,
          httpVersion: 'http2',
          ipv6Enabled: true,
                                                    origins: [
                                                      {
                                                        domainName: `${dataBucket.bucketName}.s3.${props.dataBucket.bucketRegion}.amazonaws.com`,
                                                        id: `${props.stage}-DataBucketOrigin`,
                                                        s3OriginConfig: {}, // Explicitly define as S3 origin
                                                        originAccessControlId: this.dataOac!.ref,
                                                      },
                                                    ],        },
      },
    );
  }

  private createAssetsDistribution(props: CloudFrontConstructProps): void {
    if (!props.assetsBucket) {
      return;
    }
    const assetsBucket = s3.Bucket.fromBucketAttributes(this, `${props.stage}-AssetsBucket-Ref`, {
      bucketName: props.assetsBucket.bucketName,
      bucketArn: props.assetsBucket.bucketArn,
      region: props.assetsBucket.bucketRegion,
    });

    this.assetsOac = new cloudfront.CfnOriginAccessControl(this, `${props.stage}-AssetsBucket-OAC`, {
      originAccessControlConfig: {
        name: `${props.stage}-AssetsBucket-OAC`,
        originAccessControlOriginType: 's3',
        signingBehavior: 'always',
        signingProtocol: 'sigv4',
      },
    });

    this.assetsDistribution = new cloudfront.CfnDistribution(
      this,
      `${props.stage}-Assets-Cloudfront-Distribution`,
      {
        distributionConfig: {
          defaultCacheBehavior: {
            cachePolicyId: cloudfront.CachePolicy.CACHING_OPTIMIZED.cachePolicyId,
            compress: true,
            targetOriginId: `${props.stage}-AssetsBucketOrigin`,
            viewerProtocolPolicy: 'redirect-to-https',
          },
          enabled: true,
          httpVersion: 'http2',
          ipv6Enabled: true,
                                                    origins: [
                                                      {
                                                        domainName: `${assetsBucket.bucketName}.s3.${props.assetsBucket.bucketRegion}.amazonaws.com`,
                                                        id: `${props.stage}-AssetsBucketOrigin`,
                                                        s3OriginConfig: {}, // Explicitly define as S3 origin
                                                        originAccessControlId: this.assetsOac!.ref,
                                                      },
                                                    ],        },
      },
    );

  }
}
