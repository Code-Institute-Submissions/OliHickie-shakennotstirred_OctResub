# Shaken, Not Stirred!
### An online community where users can discover, share and enjoy cocktails of all shapes and sizes!

![Image of website mock up]()

[&#x1F378;  &nbsp; **View Live Website**  &nbsp; &#x1F378;](http://shakennotstirred.herokuapp.com/)

[&#x1F379;  &nbsp; **View GitHub Repository** &nbsp; &#x1F379;](https://github.com/OliHickie/shakennotstirred)

Shaken, Not Stirred! is a website designed for users to share, discover, rate and review cocktail recipes. The website allows a user to create their own profile with which they may upload, edit and delete cocktail recipes. A user can view other user's cocktails and add a written review as well as rate the recipe. This website was created as part of my Full Stack Web Developer Diploma with Code Institute.

# Contents

1) [User Experience](#user-experience)
2) [Features](#features)
3) [Technologies](#technologies)
4) [Testing](#testing)
5) [Deployment](#deployment)
6) [Credits](#credits)

# User Experience

## User Stories

As a user of this website, I have come here to searh for new and exciting cocktails to make. I would also like to become part of a recipe sharing community where I can share some of the best recipes I used in the past. 

**As a new user (without a profile):**
I would like ot be able to:
    
- (US01) Quickly understand the purpose of the website. 
- (US02) Easily navigate around the various pages.
- (US03) Create a user profile and log in. 

**As a returning user (with a profile)**
I would like to be able to:

- (US04) Easily navigate to the login page.
- (US05) Be directed to my personal profile page.
- (US06) Search for previously visited cocktail recipes. 
- (US07) Add a cocktail recipe.
- (US08) Review other people's cocktail recipes.
- (US09) Be able to edit and delete my recipes.
- (US10) Be able to edit and delete my reviews.
- (US11) Be able to log out easily. 

**Shared user stories**
I would like to be able to:

- (US12) Experience intuitive navigation with quick and easy links to pages as well as return back to pages without needing to use the browser's back button. 
- (US13) Search for and find cocktail recipes.
- (US14) Have access to a quick search feature relying on the base spirit of the cocktail. 
- (US15) Read recipes and reviews left by users. 
- (US16) See an average rating for each recipe. 
- (US17) Discover a randomly chosen recipe when struggling for inspiration.
- (US18) Discover a popular recipe depending on the season. 
- (US19) Be able to contact the site owner with feedback or comments. 

**As the site owner**
I would like to be able to:

- (US20) Be able to edit and delete any cocktail recipe. 
- (US21) Be able to delete and edit any rating. 


## Design

The overall design was aimed at being sophisticated with a touch of fun. I wanted the site to appeal to both sexes and people of all ages. 

- Color Scheme

    The color scheme was chosen to be fairly simple as, inevitably, the use of imagery would brighten up the site. Therefore, I concentrated on three colors for the content of the pages; black, white and gold. Black and White were chosen to give a 'Black Tie' feel and that, along with splashes of gold, would give the site a clean and sophisticated look. I chose slightly off-black and off-white to soften the page and contrast. 

    ![Image of Colors Used - White, Gold and Black](static/images/readme/color-p.jpg)

- Typography

    The two main fonts used on the site are 'Yeseva One' and 'Roboto', both of which were imported from [Google Fonts](https://fonts.google.com/).

    'Yeseva One' is reserved for larger headings (h1 - h3) and is a large, heavy font with soft edges. I wanted headings to be clear but not too strong. 'Roboto' is a clear font as is used for the website content. It is easy to read but is softened by its cursive style. I find that both fonts fit the theme of being sophisticated by generally light-hearted. 

    ![Image of Yeseva One font in use](static/images/readme/yesevaone.png)
    ![Image of Roboto font in use](static/images/readme/roboto.png)

    Occassionally, a more calligraphic style font is used in some of the feature content. This is to add a welcoming feel to the home page and the logo. The fonts are not as easy to read as the main fonts, however, the added style adds a warmth and a conversational feel to the (often) subtitles in contrast to 'Yeseva One'. 

    ![Image of a calligraphhic font in use](static/images/readme/bethellen.png)

- Imagery

    Imagery is widely used on this site. The colors break up the black and white template and add a friendly and inviting feel. 
    The homepage is littered with imagery to welcome the user and help a new user understand the function of the site. There is little control over what imagery is uploaded by the user when adding a cocktail recipe. However, to ensure the image is visible, the height has been fixed and, if any inappropriate imagery is added, the admin (or site owner) is able to edit and change the image. Imagery is an important way of enticing the user into clicking a recipe. With that in mind, if no image url is added to a recipe, a default image loads instead. 

- Wireframes

    Below are my wireframes for the site, showing examples of the pages across three screen sizes. 

# Features
- **Header**
    
    The header is available on all pages and houses a website logo (which links the user to the home page) and navigation item. On smaller screens, the navigation items are located in a collapsible menu which is accessed using a hamburger icon in the top left of the screen. 

- **Nav bar items**

    The nav bar items are listed as follows:

     ![Image of navbar](static/images/readme/navbar.png)

     'My Recipes' is only visible and available to users once logged in. 'Log In' replaces 'Log Out' if no user is currently logged in and both items take the user to the log in page.

- **Footer**

    The footer appears on all pages and comprises of three main componants. 
    
    1. A repitition of the logo along with a description of the purpose of the site. 
    2. A quick search feature which, when a spirit is chosen, will take the user directly to the cocktails page and display a list of cocktails containing that base spirit.
    3. A feedback link to email the site owner in case a user has any feedback or would like to report an issue. 

    ![Image of footer](static/images/readme/footer.png)

- **Home Page**

    The home page is a welcoming page designed to give the user an outlook of the whole site as well as offer some suggestions for cocktails. As a site owner, it is also designed to encourage a new user to sign up for an account. 

    The top banner consists of a carousel with three slides; the first (upon the page loading) is a slide directing the user to log in or create an account. Two further slides are suggesting favourite cocktail recipes to try. All three slides are clickable a link the user to the desired page (whether the login page or recipe page).

    Below the carousel is a wide clickable button taking the user to all the recipes available. The button also contains a counter displaying how many cocktails are currently on the database. 

    The next section is a random cocktail picker that, on each page load, will return a random recipe from the database and display it to the user. There is also a button to quickly refresh the page and display an alternative cocktail. 

    Below that is a 'Cocktail for Every Season' section, again, designed to inspire and entice a user into clicking onto a cocktail recipe and trying it out. 

    ![Image of a seasonal cocktails](static/images/readme/seasonal-cocktails.png)

    N.B. all cocktails that appear on the home page are have been added by the site owner, so cannot be deleted or edited. 

    The final section is a brief description of what is available to a user when they sign up for the website. The three sections; create, discover and rate and review, lead to a sign up button which will take the user to a log in/register page. 

- **Cocktails Page and Cocktail Cards**

    The cocktails page is the main page of recipes. This is available to users whether they are signed in or not. Before the list of cocktails are displayed, there is a search feature and quick search tabs. The search feature uses key words and searches the cocktail names as well as ingredients. If no cocktail is found then a message is displayed informing the user of this.

    The quick search tabs are a quick way of searching for the base alcohol in the cocktail. These are the main six spirit bases that are used and will return cocktails containing those spirits. 

    ![Image of a search results](static/images/readme/searchresults.png)
    
    We then come to the recipe cards themselves. The cards are all clickable links which take the user to the specific recipe page. The cards display four pieces of information about the cocktail:
        
    - An image of the cocktail, taken from a url provided by the recipe author. If the author hasn't provided a url (which is optional), a default image will be displayed. 
    - The name of the cocktail. This is limited to 20 characters in order to prevent any overflow. 
    - The difficulty of the recipe, which is presented as dots to portray easy, medium or difficult. 
    - and the creator of the recipe. 

    The recipe cards are designed so that overflow is not possible and reduce in number per row as the screen size reduces. The recipe cards are also paginated and have a limit of twelve cards per page to prevent the page from getting too long. 

    ![Image of User's profile](static/images/readme/graceprofile.png)

- **My Recipes**

    The "My Recipes" page is similar to the "Cocktail" page, however, this page only displays cocktails contributed by the current user. From here, the user is able to progress to an edit page allowing them to edit or delete the recipe. This page also includes a link so the user can add more of their own recipes.

    The site Admin account has acces to all cocktails on this page in order to allow edit and delete functionality across all data. 

    Before adding any cocktails, a message is displayed and the "add recipe" button is more central. 

    Below is an example of a users profile page who has added three cocktails to the site. 

    ![Image of a cocktail cards](static/images/readme/cocktail-cards.png)

- **Add/Edit a Recipe **
- **Nav bar**
- **Nav bar**
- **Nav bar**
- **Flashes**


### Future Features

# Technologies
## Database Design

## Languages

## Libraries, Frameworks and other Programmes

# Testing

## Functionality Testing

- **Nav bar**

## Validation

## Compatibility Testing

## Lighthouse

## Testing User Stories

# Deployment

# Credits
