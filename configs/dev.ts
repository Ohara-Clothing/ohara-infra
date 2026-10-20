const commons = {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  stage: "ohara-dev",
};

const Stateful = {
  ...commons,
  env: {
    ...commons.env,
    region: "ap-southeast-1",
  },
};

const devCorsOrigins = [
  "https://ohara.breindel.me",
  "https://www.ohara.breindel.me",
  "https://d1nttlz1cdwr0b.cloudfront.net",
  "http://localhost:5173",
  ...(process.env.ADDITIONAL_CORS_ORIGINS
    ? process.env.ADDITIONAL_CORS_ORIGINS.split(",").map((s) => s.trim())
    : []),
];

const Stateless = {
  ...commons,
  env: {
    ...commons.env,
  },
  corsOrigins: devCorsOrigins,
  dbUser: process.env.DB_USER || process.env.user,
  dbPassword: process.env.DB_PASSWORD || process.env.password,
  dbHost: process.env.DB_HOST || process.env.host,
  dbPort: process.env.DB_PORT || process.env.port,
  dbName: process.env.DB_NAME || process.env.dbname,
  databaseUrl: process.env.DATABASE_URL,
};

const Global = {
  ...commons,
  env: {
    ...commons.env,
    region: "us-east-1", // Keep us-east-1 for global resources like CloudFront certificates
  },
  apiDomainName: process.env.API_DOMAIN_NAME || (process.env.API_CERTIFICATE_ARN ? "api.ohara.breindel.me" : undefined),
  cdnDomainName: process.env.CDN_DOMAIN_NAME || (process.env.API_CERTIFICATE_ARN ? "cdn.ohara.breindel.me" : undefined),
  certificateArn: process.env.API_CERTIFICATE_ARN,
};

export default {
  commons,
  Stateful,
  Stateless,
  Global,
};
