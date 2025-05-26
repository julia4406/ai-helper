from src.services.interview.tool_definitions_interview import SaveAnswerRate
from src.services.profile.tool_definitions_user_profile import SaveUserProfile

tools_mapper = {
    "SaveUserProfile": SaveUserProfile,
    "SaveAnswerRate": SaveAnswerRate
}
