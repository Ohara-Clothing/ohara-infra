import * as cdk from 'aws-cdk-lib';

test('CDK App Initialization', () => {
  const app = new cdk.App();
  expect(app).toBeDefined();
});

