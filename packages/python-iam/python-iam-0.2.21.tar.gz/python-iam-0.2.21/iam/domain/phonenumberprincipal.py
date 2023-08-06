#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of python-iam.
#
# python-iam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# python-iam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-iam.  If not, see <https://www.gnu.org/licenses/>.
"""Declares :class:`~PhonenumberPrincipal`."""
import phonenumbers
from phonenumbers import NumberParseException

from .principal import Principal


class PhonenumberPrincipal(Principal):
    """A :term:`Principal` that identifies a :term:`Subject` using an
    value address.
    """
    resource_class = 'PhonenumberPrincipal'
    pattern = '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'

    @classmethod
    def iscapable(cls, value):
        if not super().iscapable(value):
            return False
        try:
            p = phonenumbers.parse(value, None)
        except NumberParseException:
            return False
        return phonenumbers.is_possible_number(p)

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value or ''
