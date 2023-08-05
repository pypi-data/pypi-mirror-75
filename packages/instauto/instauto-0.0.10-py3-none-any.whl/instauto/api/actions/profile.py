from requests import Session, Response
from typing import Callable, Union

from ..structs import IGProfile, State, DeviceProfile, Method
from .structs.profile import ProfileSetGender, ProfileSetBiography, ProfileUpdate


class ProfileMixin:
    """Handles everything related to updating an Instagram profile."""
    _session: Session
    ig_profile: IGProfile
    state: State
    device_profile: DeviceProfile
    _request: Callable
    _gen_uuid: Callable
    _generate_user_breadcrumb: Callable

    def _profile_act(self, obj: Union[ProfileUpdate, ProfileSetBiography, ProfileSetGender]) -> Response:
        obj._csrftoken = self._session.cookies['csrftoken']
        obj._uid = self.state.user_id
        obj._uuid = self.state.uuid
        obj.device_id = self.state.device_id

        # retrieve the existing data for all profile data fields
        current_data = self._request('accounts/current_user/', Method.GET, query={'edit': 'true'}).json()

        # ensure we don't overwrite existing data to nothing
        if obj.phone_number is None: obj.phone_number = current_data['user']['phone_number']
        if obj.first_name is None: obj.first_name = current_data['user']['full_name']
        if obj.external_url is None: obj.external_url = current_data['user']['external_url']
        if obj.email is None: obj.email = current_data['user']['email']
        if obj.biography is None: obj.biography = current_data['user']['biography']
        if obj.username is None: obj.username = current_data['user']['trusted_username']

        endpoint = f'accounts/edit_profile/'
        return self._request(endpoint, Method.POST, data=obj.__dict__, signed=True)

    def profile_set_biography(self, obj: ProfileSetBiography) -> Response:
        """Sets the biography of the currently logged in user"""
        obj._csrftoken = self._session.cookies['csrftoken']
        obj._uuid = self.state.uuid
        obj._uid = self.state.user_id

        return self._request('accounts/set_biography/', Method.POST, data=obj.__dict__)

    def profile_set_gender(self, obj: ProfileSetGender) -> Response:
        """Sets the gender of the currently logged in user"""
        obj._csrftoken = self._session.cookies['csrftoken']
        obj._uuid = self.state.uuid

        return self._request('accounts/set_gender/', Method.POST, data=obj.__dict__, signed=False)

    def profile_update(self, obj: ProfileUpdate):
        """Updates the name, username, email, phone number and url for the currently logged in user."""
        self._profile_act(obj)
