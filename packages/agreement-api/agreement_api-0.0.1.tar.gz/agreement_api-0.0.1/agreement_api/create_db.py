import os
from agreement_api.app import DB, DB_FILE_NAME
from agreement_api.models.agreement import AgreementDummy

# Delete database file if it exists currently
if os.path.exists(DB_FILE_NAME):
    os.remove(DB_FILE_NAME)

# Create the database
DB.create_all()

# create data in database
AgreementDummy.generate_dummy_agreements()


print("Data Import Successful.")
