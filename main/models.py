from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.utils import timezone


class DemographicAffected(models.Model):
    descriptionDemo = models.CharField(max_length=1000)


class ConditionsHelped(models.Model):
    descriptionConditionHelped = models.CharField(max_length=1000)

class ConditionsHelped2(models.Model):
    descriptionConditionHelped = models.CharField(max_length=1000)


class Conditions(models.Model):
    descriptionCondition = models.CharField(max_length=1000)


class Modalities(models.Model):
    descriptionModality = models.CharField(max_length=1000)


class ModalityResource(models.Model):
    articleLink = models.CharField(max_length=1000)
    articleImage = models.CharField(max_length=1000, default="https://static.thenounproject.com/png/3255444-200.png")
    title = models.CharField(max_length=1000)
    description = models.TextField()
    publishDate = models.DateField(default=timezone.now)
    modalities = models.ManyToManyField(Modalities)
    conditions = models.ManyToManyField(Conditions)
    conditionsHelped = models.ManyToManyField(ConditionsHelped)
    demographicAffected = models.ManyToManyField(DemographicAffected)
    goal = models.CharField(max_length=1000)
    typeArticle = models.CharField(max_length=1000)
    patientReadScore = models.IntegerField()
    patientPhysicalScore = models.IntegerField()
    patientMoodScore = models.IntegerField()
    timeRequired = models.IntegerField()

class Patient(models.Model):
    userTransferID=models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ModalitiesWatched = models.ManyToManyField(ModalityResource, related_name="history+")
    ModalitiesBookmarked = models.ManyToManyField(ModalityResource, related_name="bookmarked+")
    SMOKING_CHOICES = [
        ('CURRENT', "Current Smoker"),
        ('FORMER', 'Former Smoker'),
        ('NEVER', 'Never Smoker'),
    ]

    ALCOHOL_CHOICES = [
        ('CURRENT', "Current Drinker"),
        ('FORMER', 'Former Drinker'),
        ('NEGATIVE', 'Never Drank'),
    ]
    HOUSING_CHOICES = [
        ('ALONE', "Live Alone"),
        ('GROUP', 'Live With Others'),
    ]
    MARITAL_CHOICES = [
        ('SINGLE', "Single"),
        ('MARRIED', 'Married'),
        ('OTHER', 'Other'),
    ]
    EMPLOYMENT_CHOICES = [
        ('EMPLOYED', "Employed"),
        ('UNEMPLOYED', 'Unemployed'),
    ]
    DIET_CHOICES = [
        ('VEGAN', "Vegan"),
        ('VEGETARIAN', 'Vegetarian'),
        ('REGULAR', 'Regular'),
    ]
    VETERAN_CHOICES = [
        ('NOT', 'Not A Veteran'),
        ('VETERAN', 'Veteran'),
    ]
    DISABILITIES_CHOICES = [
        ('DISABLE', 'Disabled'),
        ('ABLE', "Able"),
    ]
    GENDER_CHOICES = [
        ('FEMALE', 'Female'),
        ('MALE', "Male"),
        ('OTHER', "Other"),
        ('PREFER NOT TO DISCLOSE', "Prefer Not To Disclose"),
    ]
    GIVEN_BIRTH_CHOICES = [
        ('YES', 'Yes'),
        ('NO', "No"),
    ]
    EXERCISE_CHOICES = [
        ('YES', 'Yes'),
        ('NO', "No"),
    ]

    age = models.IntegerField(default=20,)
    height = models.IntegerField()
    weight = models.IntegerField()
    smoking = models.CharField(
        max_length=10,
        choices=SMOKING_CHOICES,
        default='NEVER',
    )
    drinking = models.CharField(
        max_length=10,
        choices=ALCOHOL_CHOICES,
        default='NEVER',
    )
    housing = models.CharField(
        max_length=10,
        choices=HOUSING_CHOICES,
        default='ALONE',
    )
    marital = models.CharField(
        max_length=10,
        choices=MARITAL_CHOICES,
        default='ALONE',
    )
    employment = models.CharField(
        max_length=10,
        choices=EMPLOYMENT_CHOICES,
        default='INSURED',
    )
    diet = models.CharField(
        max_length=10,
        choices=DIET_CHOICES,
        default='REGULAR',
    )
    veteran = models.CharField(
        max_length=10,
        choices=VETERAN_CHOICES,
        default='NOT',
    )
    disabilities = models.CharField(
        max_length=10,
        choices=DISABILITIES_CHOICES,
        default='ABLE',
    )
    dateEnrolled = models.DateField(default=timezone.now)
    firstName = models.TextField(default="John")
    lastName = models.TextField(default="Smith")
    # street = models.TextField()
    # city = models.TextField()
    # state = models.TextField()
    # zipCode = models.PositiveIntegerField()
    phoneNumber = models.IntegerField(default=1111111111)
    email = models.TextField(default="abc@email.com", help_text="Enter in correct format abc@email.com")
    dateOfBirth = models.DateField(default=timezone.now)
    ethnicity = models.TextField(default="Not Reported")
    race = models.TextField(default="Not Reported")
    gender = models.CharField(
        max_length=25,
        choices=GENDER_CHOICES,
        default='OTHER',
    )
    givenBirth = models.CharField(
        max_length=10,
        choices=GIVEN_BIRTH_CHOICES,
        default='NO',
    )
    timesBirth = models.PositiveIntegerField(default=0)
    exercise = models.CharField(
        max_length=10,
        choices=EXERCISE_CHOICES,
        default='NO',
    )
    allergies = models.TextField(default="None")
    userComment = models.CharField(max_length=1000, default="None")
    currentPos = gis_models.PointField(default=Point(0, 0))
    searchRange = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username


class CovidTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('ANTIBODY', "Antibody Testing"),
        ('ANTIGEN', 'Antigen Testing'),
    ]
    RESULT_CHOICES = [
        ('UNKNOWN', 'Unknown'),
        ('NEGATIVE', 'Negative'),
        ('POSITIVE', 'Positive'),
    ]
    HOSPITALIZATION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    VENTILATION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    INTERVENTION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    MEDICATION_CHOICES = [
        ('REMDESIVIR', "Remdesivir"),
        ('DEXAMETHASONE', 'Dexamethasone'),
        ('HYDROXYCHLOROQUINE', 'Hydroxychloroquine'),
        ('AZITHROMYCIN', 'Azithromycin'),
        ('CONVALESCENT PLASMA', 'Convalescent plasma'),
        ('ACTEMRA', "Actemra"),
        ('KALETRA', 'Kaletra'),
        ('TAMIFLU', 'Tamiflu'),
        ('AVIGAN', 'Avigan'),
        ('COLCRYS', 'Colcrys'),
        ('IVERMECTIN', 'Ivermectin'),
    ]
    STATUS_CHOICES = [
        ('CURRENTLY POSITIVE', "Currently Positive"),
        ('CURRENTLY NEGATIVE', 'Currently Negative'),
        ('CURRENTLY NEGATIVE, WAS POSITIVE', 'Currently Negative, Was Positive'),
        ('NOT TESTED', 'Not tested'),
        ('PREFER NOT TO TELL', 'Prefer not to tell'),
    ]
    OTHER_INTERVENTION_CHOICES = [
    ('BEHAVIOR', 'Behavior'),
    ('NUTRITION', 'Nutrition'),
    ('OTHERS', 'Others'),
    ]
    Date = models.DateField()
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='ANTIBODY',
    )
    results = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        default='UNKNOWN',
    )
    hospitalization = models.CharField(
        max_length=10,
        choices=HOSPITALIZATION_CHOICES,
        default='NO',
    )
    ventilation = models.CharField(
        max_length=10,
        choices=VENTILATION_CHOICES,
        default='NO',
    )
    medication = models.CharField(
        max_length=60,
        choices=MEDICATION_CHOICES,
        default='OTHERS',
    )
    covidStatus = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='NONE',
    )
    otherIntervention = models.CharField(
        max_length=10,
        choices=OTHER_INTERVENTION_CHOICES,
        default='NONE',
    )
    covidMedicineOthers = models.CharField(max_length=200)
    behaviorIntervention = models.CharField(max_length=1000)
    nutritionIntervention = models.CharField(max_length=1000)
    dateDischarge = models.DateField()
    dateLatestVisit = models.DateField(),
    dateRecovery = models.DateField()


class ScientificArticle(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)


class NewsArticle(models.Model):
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=1000)
    image = models.FileField()
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    website = models.CharField(max_length=100)


class Point(models.Model):
    name = models.CharField(max_length=100)
    point = gis_models.PointField()


class MedicalPhenotype(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    PROBLEM_CHOICES = [
        ('CARDIOVASCULAR DISEASE', "Cardiovascular Disease"),
        ('NEUROLOGICAL DISEASE', 'Neurological Disease'),
        ('CANCER', 'Cancer'),
        ('RESPIRATORY DISEASE', 'Respiratory Disease'),
        ('METABOLIC DISEASE', 'Metabolic Disease'),
        ('IMMUNOLOGICAL DISEASE', 'Immunological Disease'),
        ('HEMATOLOGICAL DISEASE', 'Hematological Disease'),
        ('MENTAL DISEASE', 'Mental Disease'),
        ('INFECTIOUS DISEASE', 'Infectious Disease'),
        ('GASTROINTESTINAL DISEASE', 'Gastrointestinal Disease'),
        ('ENDOCRINE SYSTEM DISEASE', 'Endocrine System Disease'),
        ('REPRODUCTIVE SYSTEM DISEASE', 'Reproductive System Disease'),
        ('URINARY SYSTEM DISEASE', 'Urinary System Disease'),
        ('GENETIC DISEASE', 'Genetic Disease'),
        ('SYNDROME', 'Syndrome'),
        ('OTHERS', 'Others'),
    ]
    VACCINATION_LIST_CHOICES = [
        ('INFLUENZA', "Influenza"),
        ('TD', 'Td'),
        ('HEP B', 'Hep B'),
        ('MENINGOCOCCAL MCV4P', 'Meningococcal MCV4P'),
        ('HEP A', 'Hep A'),
        ('PNEUMOCOCCAL CONJUGATE PCV 13', 'Pneumococcal conjugate PCV 13'),
        ('ZOSTER', 'Zoster'),
        ('PNEUMOCOCCAL POLYSACCHARIDE', 'Pneumococcal Polysaccharide'),
        ('VALENT', 'Valent'),
        ('HIB', 'Hib'),
        ('IPV', 'IPV'),
        ('VARICELLA', 'varicella'),
        ('MMR', 'MMR'),
        ('TDAP', 'Tdap'),
        ('HPV', 'HPV'),
        ('HEP A', 'Hep A'),
        ('DTAP', 'DTaP'),
    ]
    problem = models.CharField(
        max_length=60,
        choices=PROBLEM_CHOICES,
        default='NONE',
    )
    cardioDisease = models.CharField(max_length=1000)
    cardioMedication = models.CharField(max_length=1000)
    neurologicalInfo = models.CharField(max_length=1000)
    neurologicalMedication = models.CharField(max_length=1000)
    medicationList = models.CharField(max_length=1000)
    vaccinationList = models.CharField(
        max_length=200,
        choices=VACCINATION_LIST_CHOICES,
        default='OTHER',
    )


class Sensors(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    USING_SENSORS_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    REASON_USING_CHOICES = [
        ('SYMPTOM MANAGEMENT DOCTOR REQUIREMENT', "Symptom Management Doctor Requirement"),
        ('TREATMENT DOCTOR REQUIREMENT', 'Treatment Doctor Requirement'),
        ('SYMPTOM MANAGEMENT PERSONAL INTEREST', "Symptom Management Personal Interest"),
        ('TREATMENT PERSONAL INTEREST', 'Treatment Personal Interest'),
        ('DAILY ACTIVITY MANAGEMENT', "Daily Activity Management"),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other'),
    ]
    SHARE_DATA_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    usingSensors = models.CharField(
        max_length=10,
        choices=USING_SENSORS_CHOICES,
        default='NO',
    )
    reasonUsing = models.CharField(
        max_length=100,
        choices=REASON_USING_CHOICES,
        default='OTHER',
    )
    moreInformation = models.CharField(max_length=1000)
    brandName = models.CharField(max_length=1000)
    sharingData = models.CharField(
        max_length=10,
        choices=SHARE_DATA_CHOICES,
        default='NO',
    )

class Insurance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    INSURANCE_TYPE_CHOICES = [
        ('MEDICARE', "Medicare"),
        ('MEDICAID', 'Medicaid'),
        ('PRIVATE HEALTH PROGRAMS', 'Private Health Programs'),
        ('OTHER', 'Other'),
        ('NONE', 'None'),
    ]
    INSURANCE_PLAN_CHOICES = [
        ('HMO', "HMO"),
        ('PPO', 'PPO'),
        ('EPO', 'EPO'),
        ('POS', 'POS'),
        ('HDHP', 'HDHO'),
        ('NONE', 'None'),
    ]
    CARE_PLAN_CHOICES = [
        ('DIABETES CARE PLAN', "Diabetes care plan"),
        ('ALLERGIC DISORDER MONITORING', 'Allergic disorder monitoring'),
        ('ANTI-SUICIDE PSYCHOTHERAPY', 'Anti-suicide psychotherapy'),
        ('ASTHMA SELF MANAGEMENT', 'Asthma self management'),
        ('BURN CARE', 'Burn care'),
        ('CANCER CARE PLAN', 'Cancer care plan'),
        ('CHRONIC OBSTRUCTIVE PULMONARY DISEASE', 'Chronic obstructive pulmonary disease '),
        ('DEMENTIA MANAGEMENT', 'Dementia management'),
        ('DIABETES SELF MANAGEMENT PLAN', 'Diabetes self management plan'),
        ('DIALYSIS CARE PLAN', 'Dialysis care plan'),
        ('FRACTURE CARE', 'Fracture care'),
        ('HEAD INJURY REHABILITATION', 'Head injury rehabilitation'),
        ('HEART FAILURE SELF MANAGEMENT PLAN', 'Heart failure self management plan'),
        ('HYPERLIPIDEMIA CLINICAL MANAGEMENT PLAN', 'Hyperlipidemia clinical management plan'),
        ('INFECTIOUS DISEASE CARE PLAN', 'Infectious disease care plan'),
        ('INPATIENT CARE PLAN', 'Inpatient care plan'),
        ('LIFESTYLE EDUCATION REGARDING HYPERTENSION', 'Lifestyle education regarding hypertension'),
        ('MAJOR DEPRESSIVE DISORDER CLINICAL MANAGEMENT PLAN','Major depressive disorder clinical management plan'),
        ('MAJOR SURGERY CARE MANAGEMENT', 'Major surgery care management'),
        ('MENTAL HEALTH CARE PLAN', 'Mental health care plan'),
        ('MINOR SURGERY CARE MANAGEMENT', 'Minor surgery care management'),
        ('MUSCULOSKELETAL CARE', 'Musculoskeletal care'),
        ('OVERACTIVITY/INATTENTION BEHAVIOR MANAGEMENT', 'Overactivity/inattention behavior management'),
        ('PHYSICAL THERAPY PROCEDURE', 'Physical therapy procedure'),
        ('POSTOPERATIVE CARE', 'Postoperative care'),
        ('PSYCHIATRY CARE PLAN', 'Psychiatry care plan'),
        ('RESPIRATORY THERAPY', 'Respiratory therapy'),
        ('ROUTINE ANTENATAL CARE', 'Routine antenatal care'),
        ('SELF-CARE INTERVENTIONS', 'Self-care interventions'),
        ('SKIN CONDITION CARE', 'Skin condition care'),
        ('SPINAL CORD INJURY REHABILITATION', 'Spinal cord injury rehabilitation'),
        ('TERMINAL CARE', 'Terminal care'),
        ('URINARY TRACT INFECTION CARE', 'Urinary tract infection care'),
        ('WOUND CARE', 'Wound care'),
        ('OTHER', 'Other'),
    ]
    HEALTH_INSURANCE_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    dateEnrolled = models.DateField()
    insuranceType = models.CharField(
        max_length=100,
        choices=INSURANCE_TYPE_CHOICES,
        default='NONE',
    )
    insuranceBrand = models.TextField()
    insurancePlan = models.CharField(
        max_length=100,
        choices=INSURANCE_PLAN_CHOICES,
        default='NONE',
    )
    carePlan = models.CharField(
        max_length=200,
        choices=CARE_PLAN_CHOICES,
        default='NONE',
    )
    carePlanOther = models.TextField()
    annualMedicalBill = models.TextField()
    annualInsuranceBill = models.TextField()
    healthInsurance = models.CharField(
        max_length=10,
        choices=HEALTH_INSURANCE_CHOICES,
        default='NO',
    )
    userComment = models.CharField(max_length=1000)






class Payer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    corporationName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    applicationId = models.IntegerField()
    dateCreated = models.DateTimeField(auto_now_add=True)



    # class ClinicalTrials(models.Model):
#     What they are searching for'
#
#     location = models.geolocation()
