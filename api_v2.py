import json
import falcon


class PersonBase:
    def get_json_database(self):
        with open('persons.json', 'r') as persons:
            return json.load(persons)

    def set_json_database(self, data):
        with open('persons.json', 'w') as persons:
            persons.write(json.dumps(data, indent=4))

    def get_persons(self):
        return self.get_json_database()

    def get_person(self, id):
        persons = self.get_persons()

        for person in persons:
            if person['id'] == int(id):
                return person

        return None

    def update_json(self, data, value):
        for item in data:
            if item['id'] == value['id']:
                item.update(value)
                break

        self.set_json_database(data)

    def validate_not_found(self, value):
        if not value:
            raise falcon.HTTPNotFound()

    def validate_bad_request(self, value):
        if not all(value):
            raise falcon.HTTPBadRequest

    def person_structure(self, person_id, name):
        return {
            'id': int(person_id),
            'name': name,
        }

class PersonResource(PersonBase):
    def on_get(self, request, response):
        persons = self.get_persons()
        response.body = json.dumps(persons)

    def on_post(self, request, response):
        persons = self.get_json_database()
        body = json.loads(request.stream.read())
        self.validate_bad_request([body.get('id'), body.get('name')])
        person = self.person_structure(body.get('id'), body.get('name'))

        persons.append(person)
        self.set_json_database(persons)
        response.body = json.dumps(person)


class PersonDetailResource(PersonBase):
    def on_get(self, request, response, person_id):
        person = self.get_person(person_id)
        
        self.validate_not_found(person)

        response.body = json.dumps(person)

    def on_put(self, request, response, person_id):
        persons = self.get_persons()
        person = self.get_person(person_id)
        body = json.loads(request.stream.read())

        self.validate_not_found(person)
        self.validate_bad_request([person_id, body.get('name')])

        person_data = self.person_structure(person_id, body.get('name'))

        self.update_json(persons, person_data)

        response.body = json.dumps(person_data)

    def on_delete(self, request, response, person_id):
        person = self.get_person(person_id)
        persons = self.get_persons()

        self.validate_not_found(person)
        self.validate_bad_request(person.get('hobbies'))

        persons.remove(person)
        self.set_json_database(persons)
        

class PersonHobbiesResource(PersonBase):
    def hobbies_structure(self, hobbies):
        return {'hobbies': hobbies}

    def on_get(self, request, response, person_id):
        person = self.get_person(person_id)

        self.validate_not_found(person)
        self.validate_bad_request([person.get('hobbies')])

        response.body = json.dumps(self.hobbies_structure(person['hobbies']))

    def on_delete(self, request, response, person_id):
        persons = self.get_persons()
        person = self.get_person(person_id)
        body = json.loads(request.stream.read())

        self.validate_not_found(person)
        self.validate_not_found(body['hobby'] in person['hobbies'])
        self.validate_bad_request([body.get('hobby')])

        person['hobbies'].remove(body['hobby'])
        
        self.update_json(persons, person)

        response.body = json.dumps(self.hobbies_structure(person['hobbies']))

    def on_post(self, request, response, person_id):
        persons = self.get_persons()
        person = self.get_person(person_id)
        body = json.loads(request.stream.read())

        self.validate_not_found(person)
        self.validate_bad_request([body.get('hobby')])
        
        try:
            person['hobbies'].append(body['hobby'])
        except KeyError:
            person['hobbies'] = [body['hobby']]
        
        self.update_json(persons, person)

        response.body = json.dumps(person['hobbies'])



api = falcon.API()
api.add_route('/persons', PersonResource())
api.add_route('/persons/{person_id}', PersonDetailResource())
api.add_route('/persons/{person_id}/hobbies', PersonHobbiesResource())