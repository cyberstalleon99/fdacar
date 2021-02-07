from masterlist.models import Establishment
from .models import Record

def generate_folder(est):
    # est = Establishment.objects.get(pk=938)
    last_number = int(get_last_number(est))
    folder_number = []
    prod_type = est.product_type.name
    primary_activity = est.primary_activity.name
    specific_activities = list(est.specific_activity.all())

    if specific_activities[0].name == "Hospital Pharmacy":
        folder_number.append('HOSP-')
        folder_number.append(get_last_param(last_number))
        return "".join(folder_number)

    folder_number.append(prod_type[0])
    get_second_param(primary_activity, specific_activities, folder_number)
    get_third_param(est.plant_address.municipality_or_city.name, est.plant_address.province.name, folder_number)
    folder_number.append(get_last_param(last_number))

    return "".join(folder_number)

def get_second_param(primary_activity, specific_activities, folder_number):
    if primary_activity == 'Distributor':
        # print(specific_activities)
        temp = "/".join(list(map(get_first_char, specific_activities)))
        folder_number.append(temp)
    elif primary_activity == 'Retailer':
        print(specific_activities[0].name)
        if specific_activities[0].name == 'Drugstore' or specific_activities[0].name == 'Retail Outlet for Non-Prescription Drugs':
            folder_number.append('S')
        else:
            folder_number.append('X')

def get_third_param(city_or_muni, province, folder_number):
    if city_or_muni == "Baguio City":
        folder_number.append("BAG-")
    elif province == "Mountain Province":
        folder_number.append("MTP-")
    else:
        folder_number.append(province[:3].upper() + '-')

def get_last_param(last_number):
    return str(last_number + 1)

def get_first_char(specific_activity):
    return specific_activity.name[0]

def get_last_number(est):
    # est = Establishment.objects.get(pk=938)
    similar_ests = get_similar_establishments(est)
    folder_numbers = []
    for similar_est in similar_ests:
        folder_numbers.append(int(similar_est.folder_id.split('-')[1]))
    folder_numbers.sort()

    return folder_numbers[-1]

def get_similar_establishments(est):

    est_specific_activity = list(est.specific_activity.all())

    filters = {
        'establishment__product_type': est.product_type,
        'establishment__primary_activity': est.primary_activity,
    }

    if est.specific_activity.filter(name__in=['Hospital Pharmacy',]).exists():
        filters['establishment__specific_activity__name'] = 'Hospital Pharmacy'
    else:
        if est.plant_address.municipality_or_city.name == 'Baguio City':
            filters['establishment__plant_address__municipality_or_city'] =  est.plant_address.municipality_or_city
        else:
            filters['establishment__plant_address__province'] =  est.plant_address.province

    result = Record.objects.filter(**filters)

    if est.primary_activity == 'Distributor' and len(est_specific_activity) > 1:
        for spec in est_specific_activity:
            result = result.filter(establishment__specific_activity=spec)
        return result

    result = result.filter(establishment__specific_activity=est_specific_activity[0])
    return result
