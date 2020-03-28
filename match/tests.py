from django.test import TestCase
from django.utils import timezone
import datetime
import pytz
from match.models import Person, Mentor, Skill


class PersonModelTests(TestCase):

    # TODO: set up Person with Skills associated
    # @classmethod
    # def setUpTestData(cls):
    #     cls.skill_design = Skill(type='Design', form_value='7')
    #     cls.skill_backend = Skill(type='Back-end', form_value='2')
    #     cls.skill_design.save()
    #     cls.skill_backend.save()
    #     cls.no_time_p = Person(name='Caden McKenzie', email="caden@codingnomads.co", info="Let's DO this!!",
    #                    skills=Skill.objects.all(), timezone=6, daytime='evening', # start_time, end_time ???
    #                    )
    #     cls.no_time_p.save()
    #     # TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use skills.set() instead.

    @classmethod
    def setUpTestData(cls):
        cls.no_date_p = Person(name='Caden McKenzie', email="caden@codingnomads.co", info="Let's DO this!!",
                               timezone=6, daytime='evening', # skills, start_date, end_date ???
                               )
        cls.date_p = Person(name='Mr X', email="x@codingnomads.co", info="Secrecy!",
                            timezone=6, daytime='evening',
                            start_date=datetime.datetime(2019, 9, 16, 0, 0, tzinfo=pytz.UTC),
                            end_date=datetime.datetime(2020, 1, 1, 0, 0, tzinfo=pytz.UTC), # skills,  ???
                            )
        cls.active_p = Person(name='Mr X', email="x@codingnomads.co", info="Secrecy!",
                            timezone=6, daytime='evening',
                            start_date=datetime.datetime(2019, 9, 16, 0, 0, tzinfo=pytz.UTC),
                            end_date=timezone.now() + datetime.timedelta(days=10), # skills,  ???
                            )

    def test_empty_end_date_returns_false(self):
        self.assertFalse(self.no_date_p.is_active())

    def test_end_date_in_past_returns_false(self):
        self.assertFalse(self.date_p.is_active())

    def test_person_within_enrollment_returns_true(self):
        self.assertTrue(self.active_p.is_active())
