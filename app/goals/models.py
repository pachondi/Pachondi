from django.db import models
from app.users.models import SiteUser
from Pachondi.core.modelbase.models import BaseModel
from app.goals.utils import GetActionItem

class Goal(BaseModel):
    GOALS=((1, _('I want to get promoted.')), (2,_('Looking for a job change.')), (3,_('Looking for a profile change.')))
    content_type_id = models.IntegerField()
    current_level=models.IntegerField()
    target_level=models.IntegerField() 
    
    def TargetFor(self, user):
        actions = list()
        for action_item in self.actionitems.all():
            actions.append(action_item.FindFor(user, self.content_type_id, self.current_level, self.target_level))
        return actions
    
class Action(BaseModel):
    name = models.CharField(max_length=100)
    
    def Analyze(self, user, content_type_id, current_level, target_level):
        return GetActionItem(self.name, user, content_type_id, current_level, target_level)
    
class GoalAction(BaseModel):
    goal = models.ForeignKey(Goal, related_name='actionitems')
    action = models.ForeignKey(Action)
    
    def FindFor(self, user, content_type_id, current_level, target_level):
        return self.action.Analyze(user, content_type_id, current_level, target_level)
    
class UserGoal(BaseModel):
    user = models.ForeignKey(SiteUser, related_name = 'goals')
    goal = models.ForeignKey(Goal)
    is_completed = models.BooleanField(bool)
    start_dt = models.DateField()
    end_dt = models.DateField()
    
class UserActionItem(BaseModel):
    usergoal = models.ForeignKey(UserGoal)
    action = models.ForeignKey(Action)
    is_completed = models.BooleanField(bool)
    

        
        