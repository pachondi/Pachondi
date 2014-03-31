

from app.profile.models import UserProfile
from app.users.models import SiteUser

def GetActionItem(action, user, content_type_id, current_level, target_level):
    if action == "Connect":
        return __connections(user, content_type_id, current_level, target_level)
    elif action == "Join Groups":
        return "Join the following groups"
    else:
        pass
    
def __connections(user, content_type_id, current_level, target_level):
    """
    1. identify target organization
    2. identify target position
    3. Identify list of ppl in target position
    3.1 Gather profile data
    3.1.1 Number of years work ex
    3.1.2 Age
    3.1.3 Highest degree
    3.2 Aggregate data
    4 return data
    """

    target_position = target_level
    target_company = 1
    shortlisted_profiles = UserProfile.objects.get_all_profiles_by(content_type_id, target_position)
    aggregated_data = __aggregate_statistics(shortlisted_profiles)
    
    user_exp = user.userprofiles.get_default_profile().total_experience()
    result=""
    if user_exp < aggregated_data.get("avg_exp"):
        result= "You need approximately " + str(aggregated_data["avg_exp"]) + " of experience."
    
    for skill, count in aggregated_data.get("skill_set").iteritems():
        result+=" Required Skill: " + skill
        
    return result
  
def __aggregate_statistics(shortlisted_profiles):
    total_exp = 0 
    for profile in shortlisted_profiles:
        total_exp += profile.total_experience()
        skill_set=dict()
        for skill in profile.skills.all():
            if skill_set.get(skill.skill.name)==None:
                skill_set[skill.skill.name]=1
            else:
                skill_set[skill.skill.name]+=1
                             
    
    avg_exp = total_exp/shortlisted_profiles.count()
    return_dict = dict(avg_exp = avg_exp, skill_set = skill_set)
    return return_dict


class ActionResult(object):
    def __init__(self, *args, **kwargs):
        self.message=None
        
    