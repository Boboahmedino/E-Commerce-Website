# E-Commerce Website
# Overview
This web-based eCommerce platform, built with HTML, CSS, JavaScript, and Django, provides a seamless shopping experience for users. It allows browsing products, adding items to a shopping cart, making secure payments, and tracking orders through an intuitive interface. The site also supports product management for admins, providing features to add, update, and delete products.

# Features
+ **User Authentication:** The app includes robust user authentication to ensure secure logins and protect sensitive user data, allowing customers to create accounts, log in, and make purchases safely.
+ **Product Management:** Admin users can easily manage product listings, including adding new products, editing product details (e.g., name, description, price, image), and removing outdated items.
+ **Shopping Cart:** Users can add products to a cart, view their cart contents, and proceed to checkout with a clear summary of their orders and total price.
+ **Order Management:** After completing a purchase, users can view order details, track the status, and manage their orders directly from their account page.
+ **PayPal Payment Gateway Integration:** The platform supports secure payments through PayPal, enabling customers to make transactions via PayPal accounts or credit/debit cards, ensuring secure and smooth payment processing.
+ **Responsive Design:** The website features a responsive design, ensuring optimal usability across all devices, from desktops to mobile phones.

# Installation
To run this application, you need to install the required libraries listed in the requirements.txt file. Follow the steps below to install the dependencies:

+ Ensure you have Python installed on your system.
+ Open your terminal or command prompt and navigate to the project directory.
+ Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

This command will automatically install all the necessary libraries, including Django and other dependencies, ensuring your project is ready to run.

# Additional Notes
+ **Database Configuration:** This application is designed to work seamlessly with PostgreSQL as the default database. Ensure you have a PostgreSQL server running locally with the required database (e.g., "EcommerceDB") and user credentials configured as specified in the project settings. Alternatively, the application can also be configured to work with MySQL by updating the database settings in the settings.py file.
+ **Static and Media Files:** Make sure to place all necessary static files, such as images (e.g., product images, logo), in the appropriate directories as defined in the Django project settings. Update file paths if needed to ensure they align with your setup.
+ **PayPal Payment Gateway Configuration:** To enable PayPal payments, you need to configure the PayPal API keys and credentials in the settings. Ensure your PayPal developer account is set up, and update the integration settings accordingly in your project.
+ **Customizability:** This platform provides a flexible foundation for an eCommerce website. It can be further extended with additional features like product reviews, customer support chat, inventory management, or multi-language support.
+ **Environment Setup:** It is recommended to use a virtual environment to manage your dependencies and ensure a clean project setup. This helps to isolate the project’s libraries and avoid conflicts with other Python projects.

---

## Author
Olaneye Ahmed Oladapo
