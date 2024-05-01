#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from # type: ignore

def get_states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State).values()
    list_states = [state.to_dict() for state in all_states]
    return jsonify(list_states)


def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


def delete_state(state_id):
    """ Deletes a State Object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


def post_state():
    """ Creates a State """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


def put_state(state_id):
    """ Updates a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states_wrapper():
    """ Wrapper function for get_states """
    return get_states()


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state_wrapper(state_id):
    """ Wrapper function for get_state """
    return get_state(state_id)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state_wrapper(state_id):
    """ Wrapper function for delete_state """
    return delete_state(state_id)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state_wrapper():
    """ Wrapper function for post_state """
    return post_state()


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_state_wrapper(state_id):
    """ Wrapper function for put_state """
    return put_state(state_id)
