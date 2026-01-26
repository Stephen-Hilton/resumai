import { Amplify } from 'aws-amplify';
import { Authenticator, useAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { amplifyConfig } from './config/amplify';
import { Dashboard } from './pages/Dashboard';
import { AuthProvider } from './hooks/useAuth';

// Configure Amplify
Amplify.configure(amplifyConfig);

// Custom form fields that allow paste
const formFields = {
  signUp: {
    email: {
      order: 1,
      isRequired: true,
      label: 'Email',
      placeholder: 'Enter your email',
    },
    password: {
      order: 2,
      isRequired: true,
      label: 'Password',
      placeholder: 'Enter your password',
      autocomplete: 'new-password',
    },
    confirm_password: {
      order: 3,
      isRequired: true,
      label: 'Confirm Password',
      placeholder: 'Confirm your password',
      autocomplete: 'new-password',
    },
  },
  signIn: {
    username: {
      order: 1,
      isRequired: true,
      label: 'Email',
      placeholder: 'Enter your email',
    },
    password: {
      order: 2,
      isRequired: true,
      label: 'Password',
      placeholder: 'Enter your password',
      autocomplete: 'current-password',
    },
  },
};

function App() {
  return (
    <Authenticator 
      formFields={formFields}
      components={{
        SignUp: {
          FormFields() {
            const { validationErrors } = useAuthenticator();
            return (
              <>
                <Authenticator.SignUp.FormFields />
                {/* Re-enable paste via inline script */}
                <script dangerouslySetInnerHTML={{
                  __html: `
                    document.querySelectorAll('input').forEach(input => {
                      input.removeAttribute('onpaste');
                      input.onpaste = null;
                    });
                  `
                }} />
              </>
            );
          },
        },
      }}
    >
      {({ signOut, user }) => (
        <AuthProvider>
          <Dashboard />
        </AuthProvider>
      )}
    </Authenticator>
  );
}

export default App;
