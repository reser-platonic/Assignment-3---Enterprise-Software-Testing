from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from helper import BASE_URL, REGISTER_URL, LOGIN_URL, load_account, save_account, unique_email, unique_password

def wait(context, seconds=15):
    return WebDriverWait(context.driver, seconds)

def fill_id(context, field, value):
    field_id = "input-" + field
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(value)

def submit_registration(context, email, password, confirm_password, first_name="UTSTest", accept_privacy=True):

    fill_id(context, "firstname", first_name)
    fill_id(context, "lastname", "Student")
    fill_id(context, "email", email)
    fill_id(context, "telephone", "0400000000")
    fill_id(context, "password", password)
    fill_id(context, "confirm", confirm_password)

    consent = context.driver.find_element(
        By.CSS_SELECTOR, 'input[name="agree"]'
    )
    if accept_privacy:
        if not consent.is_selected():
            consent.click()
    else:
        if consent.is_selected():
            consent.click()
    button = wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[type="submit"][value="Continue"]')
        )
    )
    button.click()

def registration_successful(driver):
    correct_url = "route=account/success" in driver.current_url
    success_message = "Your Account Has Been Created" in driver.page_source

    return correct_url or success_message

def alert_text(context):
    return wait(context).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))).text.strip()

def validation_present(driver):
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        ".text-danger, .invalid-feedback, .alert-danger"
    )
    for element in elements:
        message = element.text.lower()
        contains_confirm = "confirm" in message
        contains_match = "match" in message
        if contains_confirm or contains_match:
            return True
    return False

def submit_login(context, email, password):
    fill_id(context, "email", email)
    fill_id(context, "password", password)
    wait(context).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"][value="Login"]'))).click()

def account_page_loaded(driver):
    correct_url = "route=account/account" in driver.current_url
    account_message = "My Account" in driver.page_source
    return correct_url and account_message


# F2 REGISTRATION
@given("I open the OpenCart registration page")
def step_open_registration(context):
    context.driver.get(REGISTER_URL)
    wait(context).until(EC.visibility_of_element_located((By.ID, "input-firstname")))

@when("I submit valid registration details with a unique email")
def step_register_valid(context):
    context.new_email = unique_email()
    context.new_password = unique_password()
    submit_registration(context, context.new_email, context.new_password, context.new_password)

@then("the new customer account should be created")
def step_registration_success(context):
    wait(context).until(registration_successful)
    assert registration_successful(context.driver)
    save_account(context.new_email, context.new_password)

@when("I submit registration details using the previously registered email")
def step_register_duplicate(context):
    account = load_account()
    password = unique_password()
    submit_registration(context, account["email"], password, password)

@then("I should see a duplicate email registration warning")
def step_duplicate_warning(context):
    warning = alert_text(context)
    warning = warning.lower()

    email_already_exists = "already" in warning or "registered" in warning # Returns true if the warning has either "already" or "registered" within it
    registration_rejected = "route=account/success" not in context.driver.current_url # Returns true if the browser is not on the registration success page

    assert email_already_exists, "Expected duplicate email warning was not displayed"
    assert registration_rejected, "Duplicate account was incorrectly accepted"

@when("I submit registration details with mismatched passwords")
def step_register_mismatch(context):
    password = unique_password()
    submit_registration(context, unique_email(), password, password + "X")

@then("I should see a password confirmation validation error")
def step_mismatch_warning(context):
    wait(context).until(validation_present)
    current_url = context.driver.current_url
    registration_rejected = "route=account/success" not in current_url
    assert registration_rejected, "Mismatched passwords were incorrectly accepted"

@when("I submit registration details without a first name")
def step_missing_firstname(context):
    email = unique_email()
    password = unique_password()
    submit_registration(context, email, password, password, first_name="")


def first_name_validation(driver):
    errors = driver.find_elements(
        By.CSS_SELECTOR,
        ".text-danger"
    )
    for error in errors:
        message = error.text.lower()
        if "first name" in message:
            return True
    return False

@then("I should see a first name validation error")
def step_firstname_warning(context):

    wait(context).until(first_name_validation)

    current_url = context.driver.current_url
    registration_rejected = "route=account/success" not in current_url

    assert registration_rejected, "Registration incorrectly accepted an empty first name"

@when("I submit valid registration details without accepting the privacy policy")
def step_no_privacy(context):
    email = unique_email()
    password = unique_password()
    submit_registration(context, email, password, password, accept_privacy=False)

@then("I should see a privacy policy warning")
def step_privacy_warning(context):
    warning = alert_text(context).lower()
    privacy_warning = "privacy" in warning or "agree" in warning
    current_url = context.driver.current_url
    registration_rejected = "route=account/success" not in current_url
    assert privacy_warning, "Privacy policy warning was not displayed"
    assert registration_rejected, "Registration was accepted without privacy consent"


#F1 LOGIN
@given("I have a customer account from the registration test")
def step_known_account(context):
    context.account = load_account()

@given("I open the OpenCart login page")
def step_open_login(context):
    context.driver.get(LOGIN_URL)
    wait(context).until(EC.visibility_of_element_located((By.ID, "input-email")))

@when("I log in using the correct password")
def step_login_valid(context):
    submit_login(context, context.account["email"], context.account["password"])

@when("I log in using an incorrect password")
def step_login_wrong_password(context):
    submit_login(context, context.account["email"], "WrongPassword")

@when("I log in using an unregistered email")
def step_login_unknown_email(context):
    submit_login(context, unique_email(), "WrongPassword")

@then("I should reach my customer account page")
def step_login_success(context):
    wait(context).until(account_page_loaded)
    assert account_page_loaded(context.driver), "Login did not reach the account page"

@when("I log in without entering a password")
def step_login_empty_password(context):

    email = context.account["email"]
    password = ""

    submit_login(context, email, password)

@then("I should see an authentication failure warning")
def step_login_rejected(context):
    warning = alert_text(context).lower()

    # Check if a warning is displayed
    contains_warning = "warning" in warning
    contains_no_match = "no match" in warning
    contains_attempt = "attempt" in warning

    warning_displayed = contains_warning or contains_no_match or contains_attempt

    # The user was not redirected to the account page, indicating that the login attempt was rejected
    current_url = context.driver.current_url
    login_rejected = "route=account/account" not in current_url

    assert warning_displayed, "Authentication failure warning was not displayed"
    assert login_rejected, "Invalid credentials were accepted"




# F3 NAVIGATION
@given("I open the OpenCart home page")
def step_home(context):
    context.driver.get(BASE_URL)
    wait(context).until(EC.visibility_of_element_located((By.ID, "menu")))


def hover_desktops(context):
    menu = context.driver.find_element(By.ID, "menu")

    # Find the Desktops link
    desktops = menu.find_element(By.LINK_TEXT, "Desktops")

    mouse = ActionChains(context.driver)
    mouse.move_to_element(desktops)
    mouse.perform()

@when("I use the top menu to open the Desktops parent category")
def step_desktops(context):
    hover_desktops(context)

    # Find the "Show All Desktops" link
    link = wait(context).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Show All Desktops")
        )
    )
    link.click()

@when("I use the top menu to open the Mac subcategory")
def step_mac(context):
    hover_desktops(context)
    link = wait(context).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "Mac") #It's a partial link text because the number of Mac elements may change over time.
        )
    )
    link.click()

@when("I use the top menu to open the Tablets category")
def step_tablets(context):
    link = wait(context).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Tablets")
        )
    )
    link.click()

@then('the category heading should be "{expected_heading}" with path "{expected_path}"')
def step_category_correct(context, expected_heading, expected_path):

    heading = wait(context).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#content h2"))
    ).text.strip()

    current_url = context.driver.current_url

    # Extract the URL parameters
    parameters = current_url.split("?")[-1].split("&")

    # Verify the expected results
    assert heading == expected_heading, "Incorrect category heading"
    assert "route=product/category" in parameters, "Incorrect destination route"
    assert "path=" + expected_path in parameters, "Incorrect category path"

def hover_components(context):

    menu = context.driver.find_element(By.ID, "menu")

    components = menu.find_element(
        By.LINK_TEXT,
        "Components"
    )

    mouse = ActionChains(context.driver)
    mouse.move_to_element(components)
    mouse.perform()

@when("I switch from Mac to Monitors using the top menu")
def step_switch_categories(context):

    wait(context).until(
        EC.url_contains("path=20_27")
    )
    heading = context.driver.find_element(
        By.CSS_SELECTOR, "#content h2"
    ).text.strip()

    assert heading == "Mac", "Mac category was not displayed"

    hover_components(context) #Open "Components" dropdown menu

    link = wait(context).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "Monitors")
        )
    )

    link.click()

@then("the category should display at least one product")
def step_verify_products(context):

    # Find the product cards
    products = context.driver.find_elements(
        By.CSS_SELECTOR, "#content .product-thumb"
    )

    number_of_products = len(products) # Count products 
    
    # At least one product should be displayed
    assert number_of_products > 0, "No products were displayed"