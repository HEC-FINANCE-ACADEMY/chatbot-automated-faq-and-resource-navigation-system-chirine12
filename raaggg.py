import json
from cryptography.fernet import Fernet

# Assuming you have the key from the previous step
key = b'ysbpEoECgEMwOXFNn_t0MZR51BoHTF6JVioemkMnDTQ= '
cipher_suite = Fernet(key)

def get_department_contact(department_name):
    # Load the encrypted JSON data
    with open("datadep.json", "r") as json_file:
        encrypted_data = json.load(json_file)

    # Check if the department exists
    if encrypted_data.get("department").lower() == department_name.lower():
        # Decrypt the sensitive data
        decrypted_email = cipher_suite.decrypt(encrypted_data["email"].encode()).decode()
        decrypted_phone = cipher_suite.decrypt(encrypted_data["phone"].encode()).decode()

        return f"Contact for {department_name}: Email - {decrypted_email}, Phone - {decrypted_phone}"
    else:
        return "Department not found!"

# Run the function
print(get_department_contact("Service Financier"))