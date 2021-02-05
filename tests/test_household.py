import datetime
import json
import os
import unittest
from unittest import TestCase
import io

from api.app import create_app
from api.models import HouseHold, db
from flask import url_for

household_payload = {
    'housingType': 'HDB'
}

family_member_payload = {
    'name': 'John',
    'gender': 'Male',
    'maritalStatus': 'Married',
    'spouseName': 'Alice',
    'annualIncome': 10000,
    'occupationType': 'Employed',
    'dob': '1987-05-20',

}


class HouseholdTestCase(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_households(self):

        # test creation of household
        res = self.client.post(
            '/api/v1/households',
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(household_payload)
        )
        result = res.json
        self.assertEqual(result['msg'], 'successfully created household')
        self.assertEqual(res.status_code, 201)

        # test deletion of household
        res = self.client.delete(
            '/api/v1/households/1'
        )
        result = res.json
        self.assertEqual(result['msg'], 'successfully deleted household')
        self.assertEqual(res.status_code, 200)

    def test_family_members(self):
        self.client.post(
            '/api/v1/households',
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(household_payload)
        )

        # create a family member
        res = self.client.put(
            '/api/v1/households/1/family_members',
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(family_member_payload)
        )
        result = res.json
        self.assertEqual(result['msg'], 'successfully created family member')
        self.assertEqual(res.status_code, 201)
