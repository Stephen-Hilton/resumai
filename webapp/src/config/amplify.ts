/**
 * AWS Amplify Configuration
 * Requirements: 1.4, 1.7, 3.2
 */

export const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || 'us-west-2_PLACEHOLDER',
      userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID || 'PLACEHOLDER',
      loginWith: {
        oauth: {
          domain: import.meta.env.VITE_COGNITO_DOMAIN || 'skillsnap-auth.auth.us-west-2.amazoncognito.com',
          scopes: ['email', 'openid', 'profile'],
          redirectSignIn: [
            import.meta.env.VITE_REDIRECT_SIGN_IN || 'http://localhost:5173/callback'
          ],
          redirectSignOut: [
            import.meta.env.VITE_REDIRECT_SIGN_OUT || 'http://localhost:5173'
          ],
          responseType: 'code' as const,
        },
      },
    },
  },
};

export const apiConfig = {
  baseUrl: import.meta.env.VITE_API_URL || 'https://r29f280jj8.execute-api.us-west-2.amazonaws.com/v1',
};
