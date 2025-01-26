from cryptography.fernet import Fernet
import json

# Générer une clé de chiffrement (à conserver en lieu sûr)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

data = {
    "department": "Service Financier",
    "email": "cf@ihec.tn",
    "phone": "+21612345678"
}

# Chiffrer les données sensibles
data["email"] = cipher_suite.encrypt(data["email"].encode()).decode()
data["phone"] = cipher_suite.encrypt(data["phone"].encode()).decode()

# Sauvegarder les données chiffrées dans un fichier JSON
with open("datadep.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Encrypted data saved successfully!")
print(key)