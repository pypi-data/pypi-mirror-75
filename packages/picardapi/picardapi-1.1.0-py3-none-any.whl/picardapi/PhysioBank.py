from picardapi import SimulateSana
import requests
import datetime
from dateutil.relativedelta import relativedelta
import random
import uuid
import numpy as np
from pprint import pprint as pp
from underscore import _
import string
import numpy


# Get a Simulation client configured to connect with the marketplace stack
sim = SimulateSana('sana')
sim.api.login('admin')

sim.api.query('/admin/config', method='put', params={"key": "USER_CREATION_METHOD", "value": "user"})
sim.api.query('/admin/config', method='put', params={"key": "REQUIRE_EMAIL_VALIDATION", "value": "False"})
sim.api.query('/admin/config', method='put', params={"key": "TERMS_ENFORCE", "value": "False"})
sim.load_roles()

delete_doctypes = False
if delete_doctypes:
    sim.remove_doctypes()

create_doctypes = False
if create_doctypes:
    sim.load_doctypes()

create_coordinator = False
if create_coordinator:
    # { 'email':  'coordinator@mtsinai.org', 'name':  'coordinator', 'password': 'letmein1' }
    sim.create_coordinator()

# Set a seed and use it to obtain user data from the randomuser.me service.
# This service uses an outdated HTTP CIPHER and will fail w/o some adjustements to openSSL
# To help users avoid troubleshooting this we include the users as a pickle file
try:
    seed = uuid.uuid4().get_hex()
    users = requests.get('https://randomuser.me/api/?results=' + str(150) + '&nat=us&seed=' + seed).json()['results']
except Exception as e:
    a=1

# Set the location from which the user agent data will be simulated
myfaker = sim.get_locale_faker('en_US')

# Get IP address for clinic
clinic_ip = sim.fakeloc_toip(target='new york', supertype="city", count=1)[0][0]

# Simulate the user types
# twoWeekExcluded: patient adherence during first two weeks is less than 50%
# eightWeekExcluded: patient stops using the mask completely before the midway part of the trial
# final: patient goes all the way through the trial
user_types = ['twoWeekExcluded'] * 10 + ['eightWeekExcluded'] * 40 + ['final'] * 100
random.shuffle(user_types)
study_arms = ['A'] * 75 + ['B'] * 75
random.shuffle(study_arms)

try:
    # Here we simulate data for each of the users.
    for user_index in range(len(users)):
        user = users[user_index]
        user_type = user_types[user_index]
        study_arm = study_arms[user_index]
        # Define user keys for different data fields
        user['medications'] = []
        user['survey_surveys'] = []
        user['patientReminder'] = {}
        user['sleepVAS'] = []
        user['painVAS'] = []
        user['medicationLogs'] = []
        user['fallAsleepUsing'] = []
        user['whoqol_surveys'] = []
        user['patientProfile'] = []
        user['medicalHistory'] = []
        user['painManagementTechniques'] = []
        user['bloodPressure'] = []
        user['deviceRegistration'] = []
        user['pgic'] = []
        user['deviceUsability'] = []
        user['willingessToKeepUsing'] = {}

        # user has a start date for the trial, then a two week follow up, then a ten week follow up,
        # then a fourteen week followup.  We simulate the dates here.
        enrollmentDate = datetime.datetime.now() - relativedelta(days=random.sample(range(200, 350), 1)[0])
        twoWeekFollowUpDate = enrollmentDate + relativedelta(days=random.sample(range(12,16), 1)[0])
        tenWeekFollowUpDate = enrollmentDate + relativedelta(days=random.sample(range(66,76), 1)[0])
        fourteenWeekFollowUpDate = enrollmentDate + relativedelta(days=random.sample(range(94, 102), 1)[0])

        # get ip address for their home
        user['ip'] = sim.fakeloc_toip(target='new york', supertype="city", count=1)[0][0]

        # Create a tablet
        tablet = sim.create_tablet(clinic_ip, enrollmentDate)
        # create the patient account
        patient = sim.create_patient(user, clinic_ip, enrollmentDate)

        # Create the patientUUID document
        user['patientUUIDs'] = {"patientUUID": patient['id']}
        res = sim.api.query('/custom/document', method='post', params={"doctypename": "patientUUIDs",
                                                                       "_id": user['id']['value'],
                                                                       "document": user['patientUUIDs']},
                            fake_ip=clinic_ip, fake_time=enrollmentDate)

        if res.status_code != 201:
            a = 1

        res = sim.api.query('/custom/document', method='get', params={"doctypename": "patientUUIDs",
                                                                      "name": user['id']['value']})
        if res.json['body']['patientUUID'] != patient['id']:
            a = 1
        print(user['id']['value'] + "\t" + patient['id'])
        continue

        ########################################################
        #
        #
        # Gather data from baseline visit
        #
        #
        ########################################################

        # Now should login as patient
        sim.api.login(name=patient['name'], password=user['login']['password'],
                      fake_ip=clinic_ip, fake_time=enrollmentDate)

        sim.create_document('stages', {'patientUUID': patient['id'], 'stage': 'week0'},
                            clinic_ip, enrollmentDate)

        # Build the user profile data
        user['patientProfile'] = [{
            "phoneNumber": user['phone'],
            "enrollmentDate": enrollmentDate,
            "patientId": user['id']['value'],
            "ageAtDateOfEnrollment": user['dob']['age'],
            "gender": user['gender'],
            "consentDate": enrollmentDate
        }]

        res = sim.create_document('patientProfile', user['patientProfile'][0], clinic_ip, enrollmentDate)
        user['medicalHistory'] = [{"description": 'first medical history'}]
        sim.create_document('medicalHistory', user['medicalHistory'][0], clinic_ip, enrollmentDate)
        user['painManagementTechniques'] = [{"description": 'first pain management techniques'}]
        sim.create_document('painManagementTechniques', user['painManagementTechniques'][0], clinic_ip, enrollmentDate)
        starting_systolic = random.sample(range(120, 180), 1)[0]
        starting_diastolic = random.sample(range(80, 120), 1)[0]
        user['bloodPressure'] = [{"systolic": starting_systolic, "diastolic": starting_diastolic}]
        sim.create_document('bloodPressure', user['bloodPressure'][0], clinic_ip, enrollmentDate)

        user['medications'] = [{
            'active': 'tylenol',
            'doseForm': 'pill',
            'numberUnitsPerDosageTime': 5,
            'mgPerUnit': 234,
            'asNeeded': True
        }]
        sim.create_document('medications', user['medications'][0], clinic_ip, enrollmentDate)
        whoqol_responses = []
        for i in range(50, 95):
            whoqol_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': enrollmentDate + relativedelta(minutes=i-50)
            })

        user['whoqol_surveys'] = [{'patientUUID': patient['id'], 'responses': whoqol_responses}]
        sim.create_document('surveys', user['whoqol_surveys'][0], clinic_ip, enrollmentDate)

        # Now should login as tablet
        sim.api.login(name=tablet['name'], password='letmein1', fake_ip=clinic_ip, fake_time=enrollmentDate)

        user['deviceRegistration'] = [{
            'tabletMacId': tablet['name'],
            'patientUUID': patient['id'],
            'eventType': 'assigned'
        }]
        sim.create_document('deviceRegistration', user['deviceRegistration'][0], clinic_ip, enrollmentDate)
        survey_responses = []
        for i in range(1, 51):
            survey_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': enrollmentDate + relativedelta(minutes=i)
            })

        user['survey_surveys'] = [{
            'patientUUID': patient['id'],
            'responses': survey_responses,
            'dateTaken': enrollmentDate
        }]
        sim.create_document('surveys', user['survey_surveys'][0], clinic_ip, enrollmentDate)

        ########################################################
        #
        #
        # First two week at home portion of the trial
        #
        #
        ########################################################
        two_week_duration = twoWeekFollowUpDate - enrollmentDate
        days_adhering = random.sample(range(two_week_duration.days/2+1, two_week_duration.days), 1)[0]
        if user_type == 'twoWeekExcluded':
            days_adhering = random.sample(range(0, two_week_duration.days/2), 1)[0]

        adherence = [0] * two_week_duration.days
        for i in range(days_adhering):
            adherence[i] = 1
        random.shuffle(adherence)

        for nextDate in sim.daterange(enrollmentDate, twoWeekFollowUpDate):
            if adherence.pop(0) == 0:
                continue
            sleep_vas = {
                'sleepScore': float(random.sample(range(0, 100), 1)[0]),
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['sleepVAS'].append(sleep_vas)
            res = sim.create_document('sleepVAS', sleep_vas, user['ip'], nextDate)
            pain_vas = {
                'painScore': float(random.sample(range(0, 100), 1)[0]),
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['painVAS'].append(pain_vas)
            res = sim.create_document('painVAS', pain_vas, user['ip'], nextDate)
            medication_log = {
                'medList': [{
                    'active': 'tylenol',
                    'numberUnitsPerDosageTime': 3
                }],
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['medicationLogs'].append(medication_log)
            res = sim.create_document('medicationLogs', medication_log, user['ip'], nextDate)

        ########################################################
        #
        #
        # Week two visit
        #
        #
        ########################################################

        if user_type == 'twoWeekExcluded':
            # Login as the admin and mark the patient as excluded.
            # Then move on to next patient
            sim.api.login('admin')
            exclusion = {
                "reason": 'Patient compliance prior to deployment of Sana therapy (week 0-2)',
                "details": 'this patient did not meet the adherence criteria for the first two weeks portion'
            }
            sim.create_document('exclusionReasons', exclusion, clinic_ip, twoWeekFollowUpDate)
            continue

        # Now should login as patient
        sim.api.login(name=patient['name'], password=user['login']['password'],
                      fake_time=twoWeekFollowUpDate, fake_ip=clinic_ip)

        bp = {
            "systolic": starting_systolic+random.sample(range(0, 10), 1)[0],
            "diastolic": starting_diastolic+random.sample(range(0, 10), 1)[0]
        }
        user['bloodPressure'].append(bp)
        sim.create_document('bloodPressure', bp, clinic_ip, twoWeekFollowUpDate)

        whoqol_responses = []
        for i in range(50, 95):
            whoqol_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': twoWeekFollowUpDate + relativedelta(minutes=i-50)
            })
        user['whoqol_surveys'].append({'patientUUID': patient['id'], 'responses': whoqol_responses})
        sim.create_document('surveys', user['whoqol_surveys'][1], clinic_ip, twoWeekFollowUpDate)
        user['medicalHistory'].append({"description": 'second medical history'})
        sim.create_document('medicalHistory', user['medicalHistory'][1], clinic_ip, twoWeekFollowUpDate)
        user['painManagementTechniques'].append({"description": 'second pain management techniques'})
        sim.create_document('painManagementTechniques', user['painManagementTechniques'][1],
                            clinic_ip, twoWeekFollowUpDate)
        user['patientProfile'].append({
            "phoneNumber": user['phone'],
            "enrollmentDate": enrollmentDate,
            "patientId": user['id']['value'],
            "ageAtDateOfEnrollment": user['dob']['age'],
            "gender": user['gender'],
            "consentDate": enrollmentDate
        })
        sim.create_document('patientProfile', user['patientProfile'][1], clinic_ip, twoWeekFollowUpDate)

        # Now should login as tablet
        sim.api.login(name=tablet['name'], password='letmein1',
                      fake_ip=clinic_ip, fake_time=twoWeekFollowUpDate)

        survey_responses = []
        for i in range(1, 51):
            survey_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': twoWeekFollowUpDate + relativedelta(minutes=i)
            })

        user['survey_surveys'].append({
            'patientUUID': patient['id'],
            'responses': survey_responses,
            'dateTaken': twoWeekFollowUpDate
        })
        sim.create_document('surveys', user['survey_surveys'][-1], clinic_ip, twoWeekFollowUpDate)

        user['patientReminder'] = {
            'nextDate': twoWeekFollowUpDate + relativedelta(weeks=2),
            'name': 'form_reminder',
            'patientUUID': patient['id']
        }
        sim.create_document('patientReminder', user['patientReminder'], clinic_ip, twoWeekFollowUpDate)
        user['deviceRegistration'] = [{
            'tabletMacId': tablet['name'],
            'maskMacId': sim.random_mask(),
            'patientUUID': patient['id'],
            'eventType': 'assigned'
        }]
        sim.create_document('deviceRegistration', user['deviceRegistration'][-1], clinic_ip, twoWeekFollowUpDate)
        user['painVAS'].append({
            'painScore': float(random.sample(range(0, 100), 1)[0]),
            'dateTaken': twoWeekFollowUpDate,
            'patientUUID': patient['id']
        })
        sim.create_document('painVAS', user['painVAS'][-1], clinic_ip, twoWeekFollowUpDate)
        # Run simulation for session here
        user['mask_name'] = 'SanaMask-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        first_mask_session = sim.simulate_mask_session(patientUUID=patient['id'],
                                                       mask_name=user['mask_name'],
                                                       startDate=twoWeekFollowUpDate + relativedelta(minutes=60),
                                                       session_id=1)
        sim.create_document('maskSessions', first_mask_session, clinic_ip, twoWeekFollowUpDate)
        user['painVAS'].append({
            'painScore': float(random.sample(range(0, 100), 1)[0]),
            'dateTaken': twoWeekFollowUpDate,
            'patientUUID': patient['id']
        })
        sim.create_document('painVAS', user['painVAS'][-1], clinic_ip, twoWeekFollowUpDate)

        ########################################################
        #
        #
        # 8 week at home portion of the trial
        #
        #
        ########################################################
        eight_week_duration = tenWeekFollowUpDate - twoWeekFollowUpDate
        days_adhering = random.sample(range(int(eight_week_duration.days/1.1)+1, eight_week_duration.days), 1)[0]
        if user_type == 'eightWeekExcluded':
            days_adhering = random.sample(range(0, eight_week_duration.days/3), 1)[0]

        adherence = [0] * eight_week_duration.days
        for i in range(days_adhering):
            adherence[i] = 1
        random.shuffle(adherence)

        num_forms = 0
        session_id = 0
        for nextDate in sim.daterange(twoWeekFollowUpDate, tenWeekFollowUpDate):
            if adherence.pop(0) == 0:
                continue
            # Get the sleep score from the previous night
            sleepVAS = {
                'sleepScore': float(random.sample(range(0, 100), 1)[0]),
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['sleepVAS'].append(sleepVAS)
            sim.create_document('sleepVAS', sleepVAS, user['ip'], nextDate)

            # Determine if they fell asleep using the mask
            fallAsleepUsing = {
                'fallAsleepUsing': '0',
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['fallAsleepUsing'].append(fallAsleepUsing)
            sim.create_document('fallAsleepUsing', fallAsleepUsing, user['ip'], nextDate)

            medicationLogs = {
                'medList': {
                    'active': 'tylenol',
                    'numberUnitsPerDosageTime': 3
                },
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['medicationLogs'].append(medicationLogs)
            sim.create_document('medicationLogs', medicationLogs, user['ip'], nextDate)

            painVAS = {
                'painScore': float(random.sample(range(0, 100), 1)[0]),
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['painVAS'].append(painVAS)
            sim.create_document('painVAS', painVAS, user['ip'], nextDate)

            # Run the mask session
            session_id += 1
            mask_session = sim.simulate_mask_session(patientUUID=patient['id'],
                                                     mask_name=user['mask_name'],
                                                     startDate=nextDate,
                                                     session_id=session_id)
            sim.create_document('maskSessions', mask_session, user['ip'], nextDate)
            painVAS = {
                'painScore': float(random.sample(range(0, 100), 1)[0]),
                'dateTaken': nextDate,
                'patientUUID': patient['id']
            }
            user['painVAS'].append(painVAS)
            sim.create_document('painVAS', painVAS, user['ip'], nextDate)
            delta = nextDate - twoWeekFollowUpDate
            if (delta.days % 14) == 0 and num_forms < 3:
                num_forms += 1
                survey_responses = []
                for i in range(1, 51):
                    survey_responses.append({
                        'questionNumber': i,
                        'answer': random.sample(range(1, 6), 1)[0],
                        'answerTimestamp': nextDate + relativedelta(minutes=1)
                    })
                surveys = {
                    'patientUUID': patient['id'],
                    'responses': survey_responses,
                    'dateTaken': nextDate
                }
                user['survey_surveys'].append(surveys)
                sim.create_document('surveys', surveys, user['ip'], nextDate)

        ########################################################
        #
        #
        # 10 week checkup
        #
        #
        ########################################################

        sim.api.login(name=patient['name'], password=user['login']['password'],
                      fake_ip=clinic_ip, fake_time=tenWeekFollowUpDate)
        bp = {
            "systolic": starting_systolic+random.sample(range(0, 10), 1)[0],
            "diastolic": starting_diastolic+random.sample(range(0, 10), 1)[0]
        }
        user['bloodPressure'].append(bp)
        sim.create_document('bloodPressure', bp, clinic_ip, tenWeekFollowUpDate)
        user['painManagementTechniques'].append({"description": 'third pain management techniques'})
        sim.create_document('painManagementTechniques', user['painManagementTechniques'][-1],
                            clinic_ip, tenWeekFollowUpDate)

        whoqol_responses = []
        for i in range(50, 95):
            whoqol_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': tenWeekFollowUpDate + relativedelta(minutes=i-50)
            })
        user['whoqol_surveys'].append({'patientUUID': patient['id'], 'responses': whoqol_responses})
        sim.create_document('surveys', user['whoqol_surveys'][-1],clinic_ip, tenWeekFollowUpDate)
        user['pgic'].append({"levelOfChange": 98, 'changeDescription': 'something about my change'})
        sim.create_document('pgic', user['pgic'][-1], clinic_ip, tenWeekFollowUpDate)
        user['deviceUsability'] = {
            'easeOfUse': random.sample(range(1, 6), 1)[0],
            'easeOfUseDescription': 'something here',
            "comfortLevel": random.sample(range(1, 6), 1)[0],
            "comfortLevelDescription": 'something here',
            "isolationLevel": random.sample(range(1, 6), 1)[0],
            "isolateLevelDescription": 'something here',
            "appEaseOfUse": random.sample(range(1, 6), 1)[0],
            "appEaseOfUseDescription": 'something here',
            "continuedUse": random.sample(range(1, 6), 1)[0],
            "recommendLikelihood": 5,
            "negativeExperienceDescription": 'something here',
            "negativeExperienceImpact": random.sample([True, False], 1)[0],
            "negativeExperienceDynamics": 'something here',
            "threeWordDescription": 'something here'
        }
        sim.create_document('deviceUsability', user['deviceUsability'], clinic_ip, tenWeekFollowUpDate)

        # Now should login as tablet
        sim.api.login(name=tablet['name'], password='letmein1', fake_ip=clinic_ip, fake_time=tenWeekFollowUpDate)

        survey_responses = []
        for i in range(1, 51):
            survey_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': tenWeekFollowUpDate + relativedelta(minutes=i)
            })

        surveys = {
            'patientUUID': patient['id'],
            'responses': survey_responses,
            'dateTaken': tenWeekFollowUpDate
        }
        user['survey_surveys'].append(surveys)
        sim.create_document('surveys', surveys, clinic_ip, tenWeekFollowUpDate)

        ########################################################
        #
        #
        # 14 week checkup
        #
        #
        ########################################################
        # Now should login as patient
        sim.api.login(name=patient['name'], password=user['login']['password'],
                      fake_ip=clinic_ip, fake_time=fourteenWeekFollowUpDate)
        bp = {
            "systolic": starting_systolic+random.sample(range(0, 10), 1)[0],
            "diastolic": starting_diastolic+random.sample(range(0, 10), 1)[0]
        }
        user['bloodPressure'].append(bp)
        sim.create_document('bloodPressure', bp, clinic_ip, fourteenWeekFollowUpDate)
        user['painManagementTechniques'].append({"description": 'fourth pain management techniques'})
        sim.create_document('painManagementTechniques', user['painManagementTechniques'][-1],
                            clinic_ip, fourteenWeekFollowUpDate)

        whoqol_responses = []
        for i in range(50, 95):
            whoqol_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': fourteenWeekFollowUpDate + relativedelta(minutes=i-50)
            })
        user['whoqol_surveys'].append({'patientUUID': patient['id'], 'responses': whoqol_responses})
        sim.create_document('surveys', user['whoqol_surveys'][-1], clinic_ip, fourteenWeekFollowUpDate)
        user['pgic'].append({"levelOfChange": random.sample(range(0, 100), 1)[0],
                             'changeDescription': 'something about my change'})
        sim.create_document('pgic', user['pgic'][-1], clinic_ip, fourteenWeekFollowUpDate)
        user['willingessToKeepUsing'] = {
            'desireToContinueUsing': random.sample([True, False], 1)[0],
            'wasSanaHelpful': random.sample([True, False], 1)[0]
        }
        sim.create_document('willingessToKeepUsing', user['willingessToKeepUsing'],
                            clinic_ip, fourteenWeekFollowUpDate)

        # Now should login as tablet
        sim.api.login(name=tablet['name'], password='letmein1', fake_ip=clinic_ip, fake_time=fourteenWeekFollowUpDate)
        survey_responses = []
        for i in range(1, 51):
            survey_responses.append({
                'questionNumber': i,
                'answer': random.sample(range(1, 6), 1)[0],
                'answerTimestamp': fourteenWeekFollowUpDate + relativedelta(minutes=i)
            })
        surveys = {
            'patientUUID': patient['id'],
            'responses': survey_responses,
            'dateTaken': fourteenWeekFollowUpDate
        }
        user['survey_surveys'].append(surveys)
        sim.create_document('surveys', surveys, clinic_ip, fourteenWeekFollowUpDate)

        a=1
        import json
        from json import json_util

        with open('data.json', 'w') as outfile:
            json.dump(json.dumps(user, default=json_util.default, indent=4), outfile)

except Exception as e:
    pass

a=1
hrvs = list()
hrvs2 = list()
for i in range(900):
    hrvs.append({
        'hr_data': random.randrange(1, 100, 1),
        'sig_quality': random.randrange(1, 100, 1),
        'NoOfRRI': random.randrange(1, 3, 1),
        'RRITime': random.randrange(1, 901, 1),
        'RRIINterval': [random.randrange(1, 901, 1) for x in range(5)]
    })

battery = list()
battery2 = list()
mask_stages = list()
mask_stages2 = list()
for i in range(30):
    battery.append(
        {
            'gauge_level': random.randrange(1, 100, 1),
            'voltage_level': random.randrange(1, 100000, 1)
        })
mask_stages.append(
    {
        'num_program': random.randrange(0, 3, 1),
        'num_steps': random.randrange(0, 3, 1),
        'type_blocks': random.randrange(0, 3, 1),
        'num_blocks': random.randrange(0, 3, 1),
        'segment': random.randrange(0, 3, 1)
    }
)

import json
session = {"SANA_PACKET_HRVDATA": hrvs, "SANA_BATTERY_STATUS": battery, "SANA_MASK_STAGE": mask_stages}
session_json = json.dumps(session)
f = open("sana_session.json", "w")
f.write(session_json)
f.close()


session = {
    'SANA_PACKET_HRVDATA': [[312, 854, 374, 506, [272, 579, 479, 505, 16]],
                            [813, 58, 105, 806, [21, 50, 255, 494, 801]]], # in reality about 900 of these
    'SANA_PACKET_SANANAME': 'SanaMask-0EAF14', # sent at beginning of session
    'SANA_FIRMWARE_VERSION': 'v01.01.5', # sent at beginning of session
    'SANA_BATTERY_STATUS': [[24, 9785], [2, 2531]], # in reality about 30 of these
    'SANA_STOPPING': 0, # sent at end of session
    'SANA_VCFW_VERSION': "6754", # sent at beginning of session
    "SANA_MASK_STAGE": [[249, 686, 376, 817], [782, 630, 234, 34]], # in reality about 30 of these
    'SANA_SESSION_ID': 0, # sent at beginning of session
    'SANA_MASK_MODE': 0, # sent at beginning of session
    'SANA_LIGHT_SOUND_LEVELS': [[51, 9340], [99, 1395]] # in reality about 30 of these
}

session = {
    'SANA_SESSION_ID': 0, # sent at beginning of session,
    'SANA_MASK_MODE': 0, # sent at beginning of session,
    'SANA_VCFW_VERSION': "6754", # sent at beginning of session,
    'SANA_PACKET_SANANAME': 'SanaMask-0EAF14', # sent at beginning of session
    'SANA_FIRMWARE_VERSION': 'v01.01.5', # sent at beginning of session
    "SANA_PACKET_HRVDATA": [
        {"NoOfRRI": 2, "RRIINterval": [324, 437, 638, 422, 677], "sig_quality": 51, "RRITime": 246, "hr_data": 56},
        {"NoOfRRI": 1, "RRIINterval": [392, 431, 462, 514, 760], "sig_quality": 17, "RRITime": 708, "hr_data": 3}
    ], # in reality about 900 of these
    "SANA_MASK_STAGE": [
        {"num_program": 0, "num_blocks": 1, "segment": 0, "num_steps": 0, "type_blocks": 1},
        {"num_program": 2, "num_blocks": 0, "segment": 2, "num_steps": 2, "type_blocks": 1}
    ], # in reality about 30 of these,
    "SANA_BATTERY_STATUS": [
        {"voltage_level": 21106, "gauge_level": 34},
        {"voltage_level": 39033, "gauge_level": 46}
    ], # in reality about 30 of these,
    'SANA_LIGHT_SOUND_LEVELS': [
        {'common_light_setting': 40,'common_sound_offset': 41},
        {'common_light_setting': 0,'common_sound_offset': 11}
    ], # in reality about 30 of these,
    'SANA_STOPPING': 0, # sent at end of session,
}

# common_light_setting; # led light
# 	uint8_t common_sound_offset; # audio volume levels
a=1
# {
#     'SANA_PACKET_HRVDATA': {
# 		hr_data: integer,
# 		sig_quality: integer,
# 		NoOfRRI:   integer,
# 		RRITime:  integer,
# 		RRIINterval:  integer[5]
# 	},
#     'SANA_PACKET_SANANAME': {
#         BLE_dev_id[]: integer //SanaMask-0EAF14  // not sure what this returns
#     },
# 'SANA_FIRMWARE_VERSION': {
#     uint8_t FW_Version[];
# },
# 'SANA_BATTERY_STATUS': {
#     uint8_t gauge_level;  // 0 to 100
# 	uint8_t charger_pwr_connected_or_batterylow;
# 	uint16_t voltage_level;  // millivolts
# },
# 'SANA_STOPPING': {
#     uint8_t StopCode;
#     #define SC_UNKNOWN		0
#     #define SC_CHARGING		1
#     #define SC_BATTERYLOW	2
#     #define SC_DONE		3
#     #define SC_POWERDOWN	4
# },
# 'SANA_VCFW_VERSION': {
#     uint8_t VCFWString[16];  // not sure what this looks like
#    # Where VCFWString is a a null-terminated string indicating the Valencell firmware version, such as "6754".
# },
# 'SANA_MASK_STAGE': {
# 	uint8_t num_program;		//which program is running 0-sleep 1-Nap 2-Relax
# 	uint8_t num_steps;			//Current program Step
# 	uint8_t type_block;			//Which type of block is running 0 =7.83hz, 1:3hz, 2=1hz
# 	uint8_t num_blocks;			//how many times to run a block
# 	uint8_t segment;			//Which segment
# },
# 'SANA_SESSION_ID': {
#     uint32_t CurrentSessionID;
# },
# 'SANA_MASK_MODE': {
#     uint32_t CurrentMaskMode;
# #define	MASK_MODE_STD		0
# #define	MASK_MODE_HRV		1
# #define	MASK_MODE_SHAM		2
#
# },
# 'SANA_LIGHT_SOUND_LEVELS': {
# 	uint8_t common_light_setting; # led light
# 	uint8_t common_sound_offset; # audio volume levels
# }
# }
