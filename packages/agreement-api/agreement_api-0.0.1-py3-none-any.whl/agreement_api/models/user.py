from agreement_api.app import DB, MA


class UserDummy:
    @staticmethod
    def get_dummy_data():
        users_instances = [User(email=email) for email in ["user@one.com", "user@two.com", "user@three.com"]]
        [DB.session.add(user) for user in users_instances]
        DB.session.commit()
        return [user.id for user in users_instances]


class User(DB.Model):
    __tablename__ = "user"  # noqa

    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String, unique=True, nullable=False)
    # agreement = DB.relationship("Agreement",
    #                             backref=DB.backref('user', lazy='joined'),
    #                             uselist=False)  # use_list=False to make one-to-one


class UserSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = DB.session  # noqa
        # include_relationships = False
        # include_fk = True
