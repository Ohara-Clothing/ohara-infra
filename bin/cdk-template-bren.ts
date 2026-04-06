#!/usr/bin/env node

import * as cdk from "aws-cdk-lib";
import { config } from "dotenv"; // Import dotenv
import { setupDevEnvironment } from "./environments/dev";
import { setupStagingEnvironment } from "./environments/staging";
import { setupProdEnvironment } from "./environments/prod";

config(); // Load environment variables from .env

const app = new cdk.App();

// Define environments
setupDevEnvironment(app);
setupStagingEnvironment(app);
setupProdEnvironment(app);