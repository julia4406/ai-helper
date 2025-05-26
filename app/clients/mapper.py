from app.services.interview.tool_definitions_interview import SaveAnswerRate
from app.services.profile.tool_definitions_user_profile import SaveUserProfile

tools_mapper = {
    "SaveUserProfile": SaveUserProfile,
    "SaveAnswerRate": SaveAnswerRate
}
