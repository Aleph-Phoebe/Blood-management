import click
from database import engine, Base, get_db
from sqlalchemy.orm import sessionmaker
from users import create_user, authenticate_user
from models import User
from inventory import add_blood_inventory, get_blood_inventory
from donors import add_donor, get_donors
from reports import generate_inventory_report, generate_donor_report
from datetime import datetime

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# In-memory session to store the currently logged-in user
session = {"user": None}

Base.metadata.create_all(bind=engine)

@click.group()
def cli():
    """Blood Management System CLI"""
    pass

def require_login(func):
    """Decorator to ensure a user is logged in before using certain commands."""
    def wrapper(*args, **kwargs):
        if session["user"] is None:
            click.echo("You must be logged in to perform this action.")
        else:
            return func(*args, **kwargs)
    return wrapper

def display_menu():
    """Function to display the main menu"""
    click.echo("\n--- Main Menu ---")
    click.echo("1. Login")
    click.echo("2. Register")
    click.echo("3. Add Blood Inventory (Staff Only)")
    click.echo("4. View Blood Inventory")
    click.echo("5. Add Donor (Staff Only)")
    click.echo("6. View Donors")
    click.echo("7. Generate Reports (Staff Only)")
    click.echo("8. Logout")
    click.echo("9. Exit\n")

@cli.command()
def main_menu():
    """Main menu for selecting options."""
    while True:
        display_menu()
        choice = click.prompt("Select an option", type=int)

        # Call functions based on user's choice
        if choice == 1:
            login()  # Login function is called
        elif choice == 2:
            register()  # Registration function is called
        elif choice == 3:
            if session["user"] and session["user"].is_staff:
                add_inventory()  # Add inventory if user is staff
            else:
                click.echo("Only staff can add inventory.")
        elif choice == 4:
            view_inventory()  # View inventory for both staff and donors
        elif choice == 5:
            if session["user"] and session["user"].is_staff:
                add_donor()  # Add donor if user is staff
            else:
                click.echo("Only staff can add donors.")
        elif choice == 6:
            view_donors()  # View donors
        elif choice == 7:
            if session["user"] and session["user"].is_staff:
                generate_report()  # Generate report if user is staff
            else:
                click.echo("Only staff can generate reports.")
        elif choice == 8:
            logout()  # Logout function is called
        elif choice == 9:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice, please try again.")

@cli.command()
def register():
    """Register a new user (staff or donor)"""
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str, hide_input=True)
    is_staff = click.confirm('Is this a staff account?', default=False)

    db = next(get_db())
    user = create_user(db, username, password, is_staff)
    if user:
        click.echo("User registered successfully.")
    else:
        click.echo("Registration failed.")

@cli.command()
def login():
    """Login to the system"""
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str, hide_input=True)

    db = next(get_db())
    user = authenticate_user(db, username, password)
    if user:
        session["user"] = user
        role = "staff" if user.is_staff else "donor"
        click.echo(f"Login successful! Logged in as {role}.")
    else:
        click.echo("Invalid username or password.")

@cli.command()
@require_login
def add_inventory():
    """Add new blood inventory (Staff Only)"""
    blood_type = click.prompt('Blood Type', type=str)
    quantity = click.prompt('Quantity', type=int)
    expiry = click.prompt('Expiry Date (YYYY-MM-DD)', type=str)
    expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()

    db = next(get_db())
    add_blood_inventory(db, blood_type, quantity, expiry_date)
    click.echo("Blood inventory added.")

@cli.command()
@require_login
def view_inventory():
    """View blood inventory (Accessible by both staff and donors)"""
    db = next(get_db())
    inventory = get_blood_inventory(db)
    for item in inventory:
        click.echo(f'{item.blood_type}: {item.quantity} units (Expiry: {item.expiry_date})')

@cli.command()
@require_login
def add_donor():
    """Add new donor (Staff Only)"""
    name = click.prompt('Name', type=str)
    blood_type = click.prompt('Blood Type', type=str)
    contact_info = click.prompt('Contact Info', type=str)
    last_donation_date = click.prompt('Last Donation Date (YYYY-MM-DD)', type=str)
    last_donation_date = datetime.strptime(last_donation_date, '%Y-%m-%d').date()

    db = next(get_db())
    add_donor(db, name, blood_type, contact_info, last_donation_date)
    click.echo("Donor added.")

@cli.command()
@require_login
def view_donors():
    """View donors (Accessible by both staff and donors)"""
    db = next(get_db())
    donors = get_donors(db)
    for donor in donors:
        click.echo(f'{donor.name}: {donor.blood_type} (Last Donation: {donor.last_donation_date})')

@cli.command()
@require_login
def generate_report():
    """Generate reports (Staff Only)"""
    db = next(get_db())
    inventory_report = generate_inventory_report(db)
    donor_report = generate_donor_report(db)

    click.echo("Inventory Report:")
    for item in inventory_report:
        click.echo(f"{item['Blood Type']}: {item['Quantity']} units (Expiry: {item['Expiry Date']})")
    
    click.echo("\nDonor Report:")
    for item in donor_report:
        click.echo(f"{item['Name']}: {item['Blood Type']} (Last Donation: {item['Last Donation Date']})")

@cli.command()
def logout():
    """Logout from the system"""
    if session["user"] is not None:
        session["user"] = None
        click.echo("You have successfully logged out.")
    else:
        click.echo("You are not logged in.")

if __name__ == "__main__":
    cli()
