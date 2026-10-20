#!/usr/bin/env node

import * as path from "path";
import * as cdk from "aws-cdk-lib";
import { config } from "dotenv"; // Import dotenv
import { setupDevEnvironment } from "./environments/dev";
import { setupStagingEnvironment } from "./environments/staging";
import { setupProdEnvironment } from "./environments/prod";

config(); // Load environment variables from root .env if present
config({ path: path.join(__dirname, "../lambdas/mainAPI/.env") }); // Fallback to lambdas/mainAPI/.env

const app = new cdk.App();

// Define environments
setupDevEnvironment(app);
setupStagingEnvironment(app);
setupProdEnvironment(app);