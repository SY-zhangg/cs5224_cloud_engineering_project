import { CognitoUserPool } from 'amazon-cognito-identity-js';

const poolData = {
  UserPoolId: 'ap-southeast-1_xvD69qdzi',
  ClientId: '5eoq60cdm86a2mq42ac92q70f7',
};

export default new CognitoUserPool(poolData);