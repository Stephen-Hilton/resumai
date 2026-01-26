# Learnings:
Whenever you resolve an issue that may recurr in the fututre, update this steering document with concise but helpful information for future debugging / enhancements. 


## Adding New User Preferences
When adding new preferences to the UI (`webapp/src/components/PreferencesModal.tsx`), you must also update the Lambda handlers:

1. **`infrastructure/lambdas/user/prefs_update.py`**:
   - Add the preference name to `VALID_BOOLEAN_PREFS` (for true/false) or `VALID_INTEGER_PREFS` (for numbers)
   - Boolean values are stored as strings ('true'/'false') in DynamoDB
   - Integer values are stored as strings and converted back on retrieval

2. **`infrastructure/lambdas/user/prefs_get.py`**:
   - Add logic to retrieve and convert the preference value back to its proper type
   - Boolean prefs: `stored_prefs.get('pref_name', 'false') == 'true'`
   - Integer prefs: `int(stored_prefs.get('pref_name'))` with None handling

3. **Redeploy both Lambdas** after changes using AWS CLI (CDK has cyclic dependency issues):
   ```bash
   # Create zip with user/ and shared/ folders at root
   zip -r /tmp/userprefs.zip user/ shared/
   aws lambda update-function-code --function-name skillsnap-userprefsupdate --zip-file fileb:///tmp/userprefs.zip
   aws lambda update-function-code --function-name skillsnap-userprefsget --zip-file fileb:///tmp/userprefs.zip
   ```
