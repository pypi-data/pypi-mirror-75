import uuid
from datetime import datetime
from flask import request

from agreement_api.app import DB, MA
from agreement_api.models.utils import get_timestamp


class AgreementDummy:

    @staticmethod
    def generate_dummy_agreements():
        """ Populates Users + Agreements in database """

        from agreement_api.models import UserDummy
        _ite = zip(UserDummy.get_dummy_data(), [True, False, True])
        agreements = [{
            "user_id": user,
            "agreement_status": status,
            "agreed_on": get_timestamp() if status else status,
        } for user, status in list(_ite)]

        [DB.session.add(Agreement(**agreement)) for agreement in agreements]

        # commit session changes to database
        DB.session.commit()


class Agreement(DB.Model):
    __tablename__ = "agreement"  # noqa

    id = DB.Column(DB.Integer, primary_key=True)
    uuid = DB.Column('uuid', DB.Text(length=36), default=lambda: str(uuid.uuid4()))
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))
    # user = DB.relationship("User", back_populates="agreement", lazy=True)
    agreement_status = DB.Column(DB.Boolean, default=False)
    agreed_on = DB.Column(DB.Integer, default=datetime.utcnow().timestamp, onupdate=datetime.utcnow().timestamp)

    def get_activation_link(self):
        host_url = request.host_url
        base_url = host_url if not host_url.endswith('/') else host_url.rstrip("/")
        api_path = request.blueprint.lstrip('/')
        activation_url = f"{base_url}/{api_path}/agreement/accept/{self.uuid}"
        return activation_url


class AgreementSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = Agreement
        sqla_session = DB.session  # noqa
        include_fk = True
        # include_relationships = True
        exclude = ("id",)

