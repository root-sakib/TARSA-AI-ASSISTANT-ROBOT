# core/user_profile.py

USER_PROFILE = {
    "name": "Sakibul Islam Sakib",
    "education": [
        "BSc in Computer Science and Engineering, Daffodil International University (2020)",
        "Diploma in Computer Science, Shariatpur Polytechnic Institute (2016)",
        "SSC in Science, Mithapur L.N. High School (2011)"
    ],
    "current_study": "Masters in Intelligent Systems at Peter the Great Saint Petersburg Polytechnic University"
}


def who_is_user(lang="en") -> str:
    """
    General answer when user asks: do you know me / who am I
    """
    edu = "; ".join(USER_PROFILE["education"])

    if lang == "bn":
        return (
            f"হ্যাঁ, আমি আপনাকে চিনি। আপনি {USER_PROFILE['name']}। "
            f"আপনার শিক্ষা: {edu}। "
            f"বর্তমানে আপনি পড়ছেন {USER_PROFILE['current_study']}।"
        )

    return (
        f"Yes, I know you. You are {USER_PROFILE['name']}. "
        f"Your education: {edu}. "
        f"Currently you are studying {USER_PROFILE['current_study']}."
    )


def get_user_field(field: str):
    """
    Get specific user attribute like name, education, current_study
    """
    if field == "name":
        return USER_PROFILE.get("name")

    if field == "education":
        return "; ".join(USER_PROFILE.get("education", []))

    if field == "current_study":
        return USER_PROFILE.get("current_study")

    return None
