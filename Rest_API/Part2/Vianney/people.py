"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
# Personal modules
from config import db
from models import Person, PersonSchema

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))



def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()

    # Serialize the data for the response
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)


def read_one(person_id):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   ID of person to find
    :return:            person matching ID
    """
    # Get the person requested
    person = Person.query \
        .filter(Person.person_id == person_id) \
        .one_or_none()

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        return person_schema.dump(person)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, 'Person not found for Id: {person_id}'.format(person_id=person_id))


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get("lname")
    fname = person.get("fname")

    # Does the person exist already?
    existing_person = Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()

    # Can we insert this person?
    if existing_person is None:

        # Create a person instance using the schema and the passed-in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        return schema.dump(new_person), 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f'Person {fname} {lname} exists already')


def update(person_id, person_new):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """

    # Get the person requested
    person_old = Person.query \
        .filter(Person.person_id == person_id) \
        .one_or_none()

    # Does the person exist in people?
    if person_old is not None:
        person_old.fname = person_new.fname
        person_old.lname = person_new.lname
        db.session.commit()

    # otherwise, nope, that's an error
    else:
        abort(404, 'Person not found for Id: {person_id}'.format(person_id=person_id))




def delete(person_id):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Person.query \
        .filter(Person.person_id == person_id) \
        .one_or_none()
    if person is not None:
        person.delete()
    # Otherwise, nope, person to delete not found
    else:
        abort(404, 'Person not found for Id: {person_id}'.format(person_id=person_id))