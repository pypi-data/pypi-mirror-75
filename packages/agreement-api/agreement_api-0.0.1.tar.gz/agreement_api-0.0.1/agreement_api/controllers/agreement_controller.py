from werkzeug.exceptions import abort

from agreement_api.app import DB
from agreement_api.models.agreement import Agreement, AgreementSchema
from agreement_api.models.user import User
from agreement_api.models.utils import get_timestamp


# Create a handler for our read (GET) agreements
def read_agreements():
    """
    This function responds to a request for /api/agreement
    with the complete lists of agreements.

    :return:        sorted list of agreements
    """
    # Create the list of people from our data
    agreements = Agreement.query.order_by(Agreement.agreement_status).all()

    # Serialize the data for the response
    agreement_schema = AgreementSchema(many=True)
    return agreement_schema.dump(agreements), 200


def agreement_form_dict(body):
    agreement_schema = AgreementSchema()
    de_serialized_agreement = agreement_schema.load(body, session=DB.session)
    return Agreement(**de_serialized_agreement)


def add_agreement(body):
    """
    This function creates a new agreement in the agreement structure
    based on the passed-in agreement data

    :param body:  agreement to create in agreement structure
    :return:        201 on success, 406 on agreement exists
    """
    agreement_already_exists = Agreement.query.filter(Agreement.user_id == body.get("user_id")).one_or_none()
    user = User.query.filter_by(id=body.get("user_id")).one_or_none()
    if not user:
        abort(400, "Specified user does't exits"),

    if agreement_already_exists:
        abort(409, f"Agreement against {body.get('user_id')} exists already")

    agreement = agreement_form_dict(body)
    DB.session.add(agreement)
    DB.session.commit()

    serialized = AgreementSchema().dump(agreement)

    return serialized, 201  # created


def get_agreement(agreement_id):
    agreement = Agreement.query.filter(Agreement.id == agreement_id).one_or_none()
    if not agreement:
        abort(404, "Invalid Agreement id.")

    agreement_schema = AgreementSchema()
    serialized_agreement = agreement_schema.dump(agreement)
    return serialized_agreement


def accept_agreement(uuid):
    """
    This function only marks an existing agreement as accepted.

    :param uuid:  uuid of target agreement.
    :return:        201 on success, 404 if agreement does't exists
    """

    agreement = Agreement.query.filter_by(uuid=uuid).first()

    if not agreement:
        abort(404, f"Invalid agreement uuid.")

    agreement.agreement_status = True
    agreement.agreed_on = get_timestamp()
    # DB.session.add(agreement) # not required in case of update.
    DB.session.commit()

    return AgreementSchema().dump(agreement), 200


def create_new(body):
    email = body.get("email")
    user_created = False
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        user_created = True
        user = User(email=email)
        DB.session.add(user)
        DB.session.commit()

    agreement = Agreement(user_id=user.id)
    DB.session.add(agreement)
    DB.session.commit()

    response = {
        "activation_link": agreement.get_activation_link(),
        "user_created": user_created
    }
    return response, 200
