# **Findr - A Minimalistic Product Marketplace**

Findr is a simple web application that allows users to upload, like, comment on, and purchase products. Users can sign up, log in, browse products, and manage their shopping cart. It's built using Flask for the backend and MySQL for the database.

---

## **Features**

- **User Registration and Authentication**: 
  - Sign up with a username, email, and password.
  - Log in using email and password (hashed with SHA-256).
  - Logout functionality.
  
- **Product Management**: 
  - Users can upload products (with captions, images, and price).
  - Each product has its own dedicated product page.
  - Products can be liked, commented on, and added to the cart.

- **Shopping Cart**: 
  - Users can add products to their cart.
  - The cart displays all products with their total price.
  - Users can proceed to checkout or remove items from the cart.

- **Request Handling**: 
  - Users can send requests to purchase items.
  - Sellers can view and manage purchase requests, updating the status (e.g., Accepted, Declined, Pending).

- **User Profile**: 
  - Users can edit their profile information.
  - Profile includes a count of posts and products uploaded.

- **Like and Comment**: 
  - Products can be liked and unliked by logged-in users.
  - Users can comment on products.

---

## **Technologies Used**

- **Backend**: 
  - Flask (Python)
  
- **Frontend**: 
  - HTML
  - CSS
  
- **Database**: 
  - MySQL
  
- **Other Libraries**: 
  - `mysql-connector-python` for database connection
  - `pickle` for cart serialization
  - `hashlib` for password hashing (SHA-256)
  - `base64` for handling product images

---

## **Installation Instructions (Windows)**

Follow these steps to get Findr up and running locally on **Windows**:

### 1. **Clone the repository**:

Download and Extract the zip file

### 3. **Install dependencies**:

Open a terminal in the project directory and run the following: 
```bash
pip install -r requirements.txt
```

### 4. **Set up MySQL database**:

In the same window, run:
```bash
python setup.py
```

### 6. **Run the Flask app**:

Once everything is set up, run the following command to start the application:

```bash
python app.py
```

### 7. **Open your browser**:

Go to `http://127.0.0.1:5000/` to access the app.

