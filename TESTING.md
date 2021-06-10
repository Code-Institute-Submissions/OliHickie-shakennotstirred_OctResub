# Testing

## Functionality Testing

- Manual testing was carried out on:
    - Desktop: Apple and Dell
    - Tablets: Apple and Samsung
    - Mobile: Apple and Samsung
    - Browsers: Chrome, Safari, Edge and Internet Explorer

- During manual testing the following tests were carried out:
    - All links worked and took the user to the desired target. These links included:
        - all nav bar links (including logo)
        - carousel links (home page)
        - randomizer and other recipe links on home page
        - login button (home page)
        - all footer links including quick search tabs and email link
        - all recipe cards
        - pagination links
        - all form buttons and modals
        - login and register buttons

    - The nav bar collapsed in smaller screens and became reachable through a hamburger icon.

    - The search bar returned cocktails with keywords included. A search message confirms what the user has searched for. If no cocktail is returned, a user message is displayed. 

    ![No results found](static/images/readme/noresults.png)

    - The quick links return cocktails which have been placed into that category. 

    - All form inputs are labelled and are validated. 

    - All data is successfully stored in the database and return flash messages to confirm with user.

    - User buttons that require you to be logged in (e.g. Add Review) take the user to the login page. 

    - Recipes are displayed in alphabetical order and are paginated with twelve recipes per page. 
    
    - All reviews are displayed with the most recent first with a new rating included and updating the recipe rating. 

- The following security measures were tested:

    - If no user is logged in, any url requiring a valid username redirect user to 404 page which includes a link back to the home page. 

    ![404 page](static/images/readme/404.png)

    - Before any recipe or review can be deleted, the user must confirm deletion via a modal. 

    - All passwords are successfully scrambled when saving in the database using Werkzeug security.

## Validation

The following results were returned from validating my code. 

- **HTML** passed with one warning

![HTML Validator](static/images/readme/htmlvalid.png)

- **CSS** passed.

![CSS Validator](static/images/readme/cssvalid.png)

- [JS Hint](https://jshint.com/) and [PEP8](http://pep8online.com/) also failed to return any issues. 

## User feedback

Some changes were made to the site after receiving user feedback:

- Originally, 'Cocktails' was called 'Recipes' and 'My Recipes' had the title 'My Cocktails'. The wording Cocktails and Recipes was swapped to give the user a clearer idea of the function of these pages. 

- The recipe card had a button to click in order to take the user to the recipe page. Instad, this has been been removed and now, the card is a clickable anchor link performing the same function. Visually, this created less clutter on the page with the removal of many buttons. 

- Reviews were listed with the newest review first. 




## Compatibility Testing

## Lighthouse

## Testing User Stories