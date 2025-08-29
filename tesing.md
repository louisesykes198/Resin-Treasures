# Resin-Treasures

![image](doc/reponsive-image.png)

[View the live project here.](https://resin-treasures-2025-f7167892b201.herokuapp.com/)

## Testing

### Testing User Stories 

### Authentication & User Profiles
- As a new user, I want to register for an account so I can make purchases and access my profile.

![image](doc/registration-page.png)

- As a returning user, I want to log in and out securely to protect my account.

![image](doc/login-page.png)

- As a user, I want to view and edit my profile so I can keep my information up to date.

![image](doc/account-settings.png)

- As a user, I want to delete my account to remove all my data.

### Shopping & Checkout
- As a user, I want to browse products by category so I can easily find what I’m looking for.

![image](doc/cat-dropdown.png)

- As a user, I want to search for products using a search bar so I can quickly find specific items.

![image](doc/desktop-nav.png)

- As a user, I want to view detailed product information before buying.

![image](doc/view-product-page.png)

- As a user, I want to add products to my basket and update quantities.
- As a user, I want to remove items from my basket.

![image](doc/basket-page.png)

- As a user, I want to proceed to checkout and make a payment securely.

![image](doc/checkout-page.png) 

![image](doc/complete-order.png)

- As a user, I want to receive confirmation after placing an order.

![image](doc/payment-complete.png)

### Wishlist
- As a user, I want to add items to my wishlist to save them for later.

![image](doc/wishlist-button.png) 

![image](doc/wishlist.png) 

- As a user, I want to view and manage my wishlist from my profile.
- As a user, I want to remove items I no longer want from my wishlist.

![image](doc/wishlist-with-items.png) 

### Newsletter

- As a visitor, I want to enter my email address and subscribe to the newsletter, so that I can receive updates about new products and offers.

![image](doc/sub.png) 

- As a visitor, I want to receive a confirmation email when I subscribe, so that I know my subscription was successful.

![image](doc/confirm-email.png) 

- As a visitor, I want to see a success message on the site after subscribing, so that I know my action was completed.

![image](doc/confirm-news.png) 

- As a visitor, I want to be notified if my email is already subscribed, so that I don’t accidentally subscribe multiple times.

 ![image](doc/new-already.png) 

- As a site admin, I want to view a list of all subscribed emails, so that I can understand my audience and target communications.

![image](doc/admin-user.png) 

![image](doc/admin-change-user.png) 

### Admin & Store Management
- As the site owner, I want to add, update, or delete product listings to manage my store inventory.

![image](doc/admin-add-item.png) 

- As the site owner, I want to create and manage product categories to keep the store organized.

![image](doc/admin-cat.png) 
 
- As the site owner, I want to view and fulfill customer orders.

![image](doc/admin-order.png) 
 
### Static Pages & Contact

- As a user, I want to visit the About page to learn about the store and its owner.

![image](doc/about-page.png) 

- As a user, I want to use a Contact form to ask questions or request custom orders.

![image](doc/contact-page.png) 

## 🚀 Lighthouse Performance Report

The site was tested using Chrome's Lighthouse tool to measure key performance metrics, including accessibility, best practices, and SEO.

<details>
<summary>Login Page - Desktop</summary>
<img src="doc/login-lighthouse.png" alt="Login Page">
</details>

<details>
<summary>Registration Page - Desktop</summary>
<img src="doc/reg-lighthouse.pngg" alt="Registration Page">
</details>

<details>
<summary>Home Page - Desktop</summary>
<img src="doc/lh-desktop-home.png" alt="Home Page">
</details>

<details>
<summary>About Page - Desktop</summary>
<img src="doc/about-lighthouse.png" alt="About Page">
</details>

<details>
<summary>Category Page - Desktop</summary>
<img src="doc/product-lighthouse.png" alt="Category Page">
</details>

<details>
<summary>Basket Page - Desktop</summary>
<img src="doc/basket-lighthouse.png" alt="Basket Page">
</details>

<details>
<summary>Profile Page - Desktop</summary>
<img src="doc/account-settings-lighthouse.png" alt="Profile Page">
</details>

<details>
<summary>Checkout Page - Desktop</summary>
<img src="doc/checkout-lighthouse.png" alt="Checkout Page">
</details>

<details>
<summary>Complete Page - Desktop</summary>
<img src="doc/complete-lighthouse.png" alt="Complete Page">
</details>

### 🖥️ Desktop View

✅ The layout scales correctly  
✅ Navigation works as expected  
✅ All buttons and forms are accessible  

#### 📸 Screenshots

 ### Landing Page  
  ![image](docs/landing-page.png)

 ### Navigation Bar  
  ![image](docs/navbar.png)

 ### Add New Project  
  ![image](docs/add-page.png)

 ### Edit Project  
  ![image](docs/edit-page.png)

  ![image](docs/denied_edit.png)

 ### View Project Page  
  ![image](docs/project-page.png)

 ### Delete Project
  ![image](docs/delete-page.png)

  ![image](docs/delete-message.png)

  ![image](docs/delete-page.png)

 No Comments State  
  ![image](docs/no-comment.png)

---

### 📱 Mobile View

✅ Navigation collapses correctly  
✅ Forms are readable and scrollable  
✅ Cards and buttons scale appropriately  

#### 📸 Screenshots

 ### Home View  
  ![image](docs/mobile-home-view.png)

 ### Navigation Menu  
  ![image](docs/mob-nav.png)

 ### Add New Project  
  ![image](docs/mob-new-pat.png)

 ### Edit Project  
  ![image](docs/mob-edit.png)

  ![image](docs/denied_edit_mob.png)

 ### View Project  
  ![image](docs/mob-view.png)

 ### Comment Section  
  ![image](docs/mob-com.png)

 ### Delete Project

 ![image](docs/delete-message-mob.png)

 ![image](docs/delete-page-mob.png)

 ![image](docs/denied-mob.png)

## 🧪 Manual Test Cases

The following features were manually tested across desktop and mobile devices:

| Feature                   | Test Case Description                                  | Status   |
|---------------------------|--------------------------------------------------------|----------|
| 🔐 User Registration      | Sign up with valid and invalid credentials             | ✅ Pass   |
| 🔓 User Login/Logout      | Login/logout flow works as expected                    | ✅ Pass   |
| ➕ Add Project             | Form validates input and displays project on submit    | ✅ Pass   |
| ✏️ Edit Project           | Changes are saved and reflected on the detail page     | ✅ Pass   |
| ❌ Delete Project         | Project is removed and no longer accessible            | ✅ Pass   |
| 💬 Comment on Project     | Adds comment and displays it beneath project           | ✅ Pass   |
| ❤️ Like Project           | Like counter updates and toggles properly              | ✅ Pass   |
| 📱 Mobile Responsiveness  | Pages adapt correctly to smaller screen sizes          | ✅ Pass   |
| 🧭 Navbar Functionality   | All links and dropdowns navigate correctly             | ✅ Pass   |

## Debug Off

The project uses an option called DEBUG to help keep the site safe when it is live. This is disabled in production so that sensitive data is not displayed if an issue occurs. Additional security options are enabled when DEBUG is turned off, such as mandating HTTPS and protecting cookies. These help to keep user data protected. When working locally on your PC (DEBUG enabled), these options are disabled to make testing and development easier.

![image](docs/debug-two.png) ![image](docs/debug-one.png)

# 🧰 Validators

The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

[W3C Markup Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)

## HTML Validation Checks

The following pages were checked with an HTML validator, and no errors were found:

| **Page**               | **Checked with HTML Validator with no errors** |
|------------------------|------------------------------------------------|
| base.html              | ✅ Yes                                        |
| home.html              | ✅ Yes                                        |
| add_comment.html       | ✅ Yes                                        |
| register.html          | ✅ Yes                                        |
| login.html             | ✅ Yes                                        |
| add_project.html       | ✅ Yes                                        |
| category_view.html     | ✅ Yes                                        |
| delete_project.html    | ✅ Yes                                        |


![image](docs/base-html-vali.png)

[W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)

![image](docs/css-vail.png)

## Python Validators

[CI Python Linter Validator](https://pep8ci.herokuapp.com/)

### Admion.py

![image](docs/admin.png)

### Apps.py

![image](docs/apps.png)

### Forms.py

![image](docs/forms.png)

### Models.py

![image](docs/models.png)

### Urls.py

![image](docs/urls.png)

### Views.py

![image](docs/views.png)

### Test.py

![image](docs/test-all-vali.png)

## Further Testing

To ensure cross-browser compatibility, the website was tested across multiple web browsers, including **Google Chrome**, **Microsoft Edge**, and **Safari**. It was also viewed on a range of devices, such as desktop and laptop computers, as well as mobile devices including the **Samsung Galaxy A12**, **Samsung Galaxy S22**, and **iPhone SE**. Additionally, friends and family members were invited to review the website and its documentation to identify potential bugs or user experience issues.

# Unit Testing


## 🧪 Testing
Unit tests were written using Django’s built-in TestCase class to ensure key functionality works correctly across the application. All tests were run using the command python manage.py test.

### ✅ Tests Overview

**Model Test** – ProjectModelTest
Verifies that a Project instance can be created successfully and that the name field is stored and retrieved correctly.

**Form Test** – CommentFormTest
Checks that the CommentForm accepts valid input and passes form validation, ensuring the comment field works as intended.

**Authentication Test** – UserAuthTest
Confirms that a test user can log in using the login view. It performs a POST request and follows the redirect to ensure a 200 OK status code is returned, indicating a successful login.

**Security Test** – SecurityTest
Verifies that DEBUG is set to False in a production environment. While DEBUG is currently True during local development, conditional logic is in place to enable important security features in production:

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    ...
else:
    # Local development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
This setup ensures HTTPS and secure cookie settings are applied when the project is deployed.

### ✅ Test Results
All tests passed successfully:

Found 3 test(s).
Creating test database for alias 'default'...
...
Ran 3 tests in 0.002s

OK
Destroying test database for alias 'default'...

![image](docs/test-all.png)




