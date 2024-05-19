from prudens.models import User,Researcher, NonResearcher
from prudens import db

class UserRepository:
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    @staticmethod    
    def delete_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    @staticmethod
    def update_fname(email, fname):
        user = User.query.filter_by(email=email).first()
        if user:
            user.fname = fname
            db.session.commit()
        return user

    @staticmethod
    def update_lname(email, lname):
        user = User.query.filter_by(email=email).first()
        if user:
            user.lname = lname
            db.session.commit()
        return user


class NonResearcherRepository:
    @staticmethod
    def create_non_researcher(fname, lname, username, email, password):
        non_researcher = NonResearcher(
            fname=fname,
            lname=lname,
            username=username,
            email=email,
            password=password
        )
        db.session.add(non_researcher)
        db.session.commit()
        return non_researcher
class ResearcherRepository:
    @staticmethod
    def create_researcher(fname, lname, username, email, password, field_of_study, linkedin_account, google_scholar_account):
        researcher = Researcher(
            fname=fname,
            lname=lname,
            username=username,
            email=email,
            password=password,
            field_of_study=field_of_study,
            linkedin_account=linkedin_account,
            google_scholar_account=google_scholar_account
        )
        db.session.add(researcher)
        db.session.commit()
        return researcher
