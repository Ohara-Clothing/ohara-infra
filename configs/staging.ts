const commons = {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  stage: "ohara-staging",
};

const Stateful = {
  ...commons,
  env: {
    ...commons.env,
    region: "ap-southeast-1",
  },
};

const Stateless = {
  ...commons,
  env: {
    ...commons.env,
  },
  corsOrigins: [
    "https://ohara.breindel.me",
    "https://www.ohara.breindel.me",
    "http://localhost:5173",
  ],
};

const Global = {
  ...commons,
  env: {
    ...commons.env,
    region: "us-east-1",
  },
};

export default {
  commons,
  Stateful,
  Stateless,
  Global,
};
