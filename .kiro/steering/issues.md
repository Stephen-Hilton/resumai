
# "Job Card" "Subcomponent" Bugs:
## Please Fix:
- clicking on the green arrow to "Manual" "Generate" Summary correctly sets the icon to spin, but does nothing; it never returns and never generates anything, until I do a hard-reset of the browser.  I suspect the request is made, but the webpage never returns to ask for an update on progress.  Can you either make a callback when processing is complete (preferable), or have a 2 second timer that will check for updates (if materially easier).

- The "Manual" "Generate" function for "Contacts" generated... just the name, none of the contacts.
    `<section class="contact"><h1>Stephen Hilton</h1><address></address></section>`
    This is not the contact section.  The "Manual Engine" needs a dramatic fix.  

- in the Job Card top section, there was supposed to be a small "Edit" button added to the end of the 2nd row, behind "URL Added" but I don't see it, please fix



# "Job Card" "Subcomponent" Change Requests:
## Please Change:
### When clicking on the name of the Resume Section:
- ...the window to view/edit the code is only a few lines tall; please make it much taller, at least 20 lines.
- ...the window to view/edit the code should close when the Escape key is pressed, unless there are unsaved changes.


### Submitted
- minor change; please change the "Omit" icon to be a grey X (not red, it's too distracting).  Also, if "Omit" then change the text for that line to light grey with strike-thru.  



# "Settings" "Preferences" Pop-Out Bugs:
## Please Fix:
- Default Generation by Section is not saving; every browser hard-reset erases all my selectiongs.  please persist to DynamoDB per the requirements. 




## "Left Nav Pane"

### Needed / TBD:

- move the "Search Jobs" text box to the left Job Nav pane, between "Add Job" and "Phases"
- add a "Sort by" dropdown to the left Job Nav pane, between "Search Jobs" and "Phases"


