"""Column name → human-readable description mapping for the GMP (Global Mind Project) dataset.

Grouped by topic for easy browsing and documentation generation.
"""

# =============================================================================
# Meta & timestamps
# =============================================================================
META = {
    "language": "Survey language (问卷语言)",
    "start_date_utc": "Assessment start time in UTC (评估开始时间 UTC)",
    "day": "Day of assessment (评估日期 日)",
    "month": "Month of assessment (评估日期 月)",
    "year": "Year of assessment (评估日期 年)",
    "submit_data_utc": "Submission time in UTC (提交时间 UTC)",
    "time_to_complete": "Time taken to complete the assessment (完成耗时)",
}

# =============================================================================
# MHQ aggregate scores (7)
# =============================================================================
MHQ_SCORES = {
    "overall_mhq_score": "Overall MHQ score (MHQ 总得分)",
    "cognition_score": "Cognition score (认知能力得分)",
    "adapt_resilience_score": "Adaptation & resilience score (适应与韧性得分)",
    "drive_motivation_score": "Drive & motivation score (驱动力与动机得分)",
    "mood_outlook_score": "Mood & outlook score (情绪与展望得分)",
    "social_self_score": "Social self score (社交自我得分)",
    "mind_body_score": "Mind-body connection score (身心连接得分)",
}

# =============================================================================
# MHQ 47 individual assessment items
# =============================================================================
MHQ_ITEMS = {
    # --- Cognition ---
    "understanding": "Understanding (理解能力)",
    "ability_learn": "Ability to learn (学习能力)",
    "memory": "Memory (记忆力)",
    "creativity_problem_solving": "Creativity & problem solving (创造力与解决问题)",
    "planning_organization": "Planning & organization (计划与组织)",
    "selective_attention": "Selective attention (选择性注意力)",
    "focus_concentration": "Focus & concentration (专注力)",
    "speech_language": "Speech & language (言语与语言)",
    "confusion": "Confusion (困惑感)",

    # --- Mood & emotion ---
    "stability_calmness": "Stability & calmness (情绪稳定与冷静)",
    "emotional_resilience": "Emotional resilience (情绪韧性)",
    "emotional_control": "Emotional control (情绪控制)",
    "mood_swings": "Mood swings (情绪波动)",
    "sad_hopeless": "Sadness & hopelessness (悲伤/绝望)",
    "outlook_optimism": "Outlook & optimism (乐观展望)",
    "fear_anxiety": "Fear & anxiety (恐惧/焦虑)",
    "anger": "Anger (愤怒)",
    "guilt_blame": "Guilt & self-blame (内疚/自责)",
    "guilt_blame_type": "Guilt/blame trigger type (内疚/自责触发类型)",

    # --- Self ---
    "self_worth_confidence": "Self-worth & confidence (自我价值/自信)",
    "self_image": "Self-image (自我形象)",
    "drive_motivation": "Drive & motivation (驱动力与动机)",
    "curiosity_enthusiasm": "Curiosity & enthusiasm (好奇心与热情)",
    "energy": "Energy level (精力水平)",
    "adapt_to_change": "Adaptability to change (适应变化能力)",
    "decision_risk": "Decision-making & risk assessment (决策与风险评估)",

    # --- Social ---
    "relationships": "Relationship quality (人际关系质量)",
    "social_cooperation": "Social cooperation (社交合作能力)",
    "empathy": "Empathy (同理心)",
    "coordination": "Coordination (协调能力)",
    "physical_intimacy": "Physical intimacy (身体亲密)",
    "aggression": "Aggression (攻击性)",
    "avoidance": "Social avoidance (社交回避)",

    # --- Mind-body ---
    "sleep_quality": "Sleep quality (睡眠质量)",
    "appetite_regulation": "Appetite regulation (食欲调节)",
    "physical_health": "Physical health perception (身体健康感受)",
    "self_control_impulsivity": "Self-control & impulsivity (自控力/冲动控制)",
    "sensory_sensitivity": "Sensory sensitivity (感官敏感度)",
    "pain": "Physical pain (身体疼痛)",

    # --- Clinical ---
    "restless_hyperactive": "Restlessness & hyperactivity (烦躁/多动)",
    "obsessive_thoughts": "Obsessive thoughts (强迫思维)",
    "obsessive_thoughts_type": "Obsessive thought type (强迫思维类型)",
    "detached_reality": "Detached reality (现实感脱离)",
    "nightmares": "Nightmares (噩梦)",
    "hallucinations": "Hallucinations (幻觉)",
    "flashblacks": "Flashbacks (闪回)",
    "repetitive_actions": "Repetitive actions (重复行为)",
    "addictions": "Addictive behaviors (成瘾行为)",
    "infections": "Infections (感染)",
    "suicidal_thoughts": "Suicidal thoughts (自杀念头)",
}

# =============================================================================
# Core demographics
# =============================================================================
DEMOGRAPHICS_CORE = {
    "age": "Age group (年龄段)",
    "biological_sex": "Biological sex (生理性别)",
    "gender_diff": "Gender identity vs. biological sex difference (性别认同与生理性别差异)",
    "gender_identity": "Gender identity (性别认同)",
    "gender": "Gender (性别)",
    "ethnicity": "Ethnicity (种族/民族)",
    "country": "Country (国家)",
    "state": "State / province / region (州/省/地区)",
    "rural_urban": "Rural vs. urban classification (城乡分类)",
    "city": "City (城市)",
    "education": "Education level (教育程度)",
    "employment": "Employment status (就业状态)",
}

# =============================================================================
# Work & employment
# =============================================================================
WORK = {
    "employment_sector": "Employment sector (就业行业)",
    "job_role": "Job role / position (职位/角色)",
    "income_household": "Household income level (家庭收入水平)",
    "veteran_status_US": "US veteran status (美国退伍军人身份)",
    "productivity_absent": "Days absent from work — past 4 weeks (缺勤天数 过去4周)",
    "productivity_unproductive": "Unproductive work days — past 4 weeks (低效工作天数 过去4周)",
    "team_situation": "Team working arrangement (团队工作模式)",
    "job_features": "Job features description (工作特征描述)",
    "work_situation": "Work mode — remote / on-site / hybrid (工作模式 远程/现场/混合)",
    "organization_size": "Organization size (组织规模)",
    "job_duration": "Time in current role (在当前岗位时长)",
    "work_control_time": "Control over work schedule (对工作时间安排的控制)",
    "work_control_job": "Autonomy over how work is done (对工作方式的自主权)",
    "work_amount": "Workload pressure (工作量压力)",
    "work_purpose": "Sense of purpose & meaning at work (工作目标感/意义感)",
    "work_learning": "Learning opportunities at work (工作中学习机会)",
    "work_colleagues": "Relationship with colleagues (与同事关系)",
    "work_manager": "Relationship with manager/supervisor (与上司关系)",
    "work_informed": "Being kept informed at work (工作信息知情度)",
    "work_recognition": "Recognition at work (工作认可度)",
    "work_factors": "Work stress factors — multi-select (工作压力因素 多选)",
    "job_sector": "Industry sector (所属行业)",
    "work_activity": "Type of work activity (工作活动类型)",
}

# =============================================================================
# Lifestyle — diet, exercise, sleep, socialising
# =============================================================================
LIFESTYLE = {
    "cantril": "Cantril ladder — overall life evaluation 1-9 (Cantril 阶梯 总体生活评价 1-9)",
    "sleep_freq": "Frequency of getting enough sleep (充足睡眠频率)",
    "sleep_problem_type": "Sleep problem type — multi-select (睡眠问题类型 多选)",
    "exercise_freq": "Exercise frequency — ≥30 min/session (运动频率 ≥30分钟/次)",
    "UPF_freq": "Ultra-processed food consumption frequency (超加工食品摄入频率)",
    "fruit_veg_freq": "Fresh fruit & vegetable intake frequency (新鲜蔬果摄入频率)",
    "organic_fruit_veg_freq": "Organic fruit & vegetable consumption (有机蔬果食用频率)",
    "sugary_food_freq": "Sweet/sugary food or dessert frequency (甜食/含糖食物频率)",
    "meat_diet": "Meat consumption habits (肉类摄入习惯)",
    "fish_diet": "Fish/shellfish consumption habits (鱼类/贝类摄入习惯)",
    "plastic_food": "Food/drinks from plastic containers (塑料容器装食物/饮品频率)",
    "plastic_hot_food": "Hot food from plastic containers (塑料容器装热食频率)",
    "plastic_hot_drink": "Hot drinks in paper cups (纸杯热饮频率)",
    "social_freq": "In-person socializing frequency (线下社交频率)",
}

# =============================================================================
# Substance use, medical conditions & treatment
# =============================================================================
SUBSTANCE_AND_MEDICAL = {
    "substance_use": "Substance use — multi-select (物质使用 多选)",
    "medical_condition_presence": "Whether diagnosed with a medical condition (是否有确诊疾病)",
    "medical_condition_type": "Medical condition type — multi-select (疾病类型 多选)",
    "treatment_status": "Whether currently receiving treatment (是否正在接受治疗)",
    "help_seeking": "Whether sought help (是否寻求过帮助)",
    "treatment_type_new": "Treatment type — new version, multi-select (治疗类型 新版 多选)",
    "treatment_type": "Treatment type — old version, multi-select (治疗类型 旧版 多选)",
    "therapy_efficacy": "Perceived effectiveness of psychological therapy (心理治疗有效性评价)",
    "medication_efficacy": "Perceived effectiveness of medication (药物治疗有效性评价)",
    "brain_stim_efficacy": "Perceived effectiveness of brain stimulation (脑刺激治疗效果)",
    "neurofeedback_efficacy": "Perceived effectiveness of neurofeedback (神经反馈治疗效果)",
    "mental_health_disorder": "Mental health disorder diagnosis (心理健康障碍诊断)",
}

# =============================================================================
# Trauma & adversity
# =============================================================================
TRAUMA = {
    "trauma_childhood": "Childhood trauma experiences — before age 18, multi-select (童年创伤经历 18岁前 多选)",
    "trauma_adulthood": "Adult trauma experiences — after age 18, multi-select (成年创伤经历 18岁后 多选)",
    "trauma_life_old": "Life trauma — archived old version (人生创伤经历 旧版 已归档)",
}

# =============================================================================
# Family, friendship & community
# =============================================================================
FAMILY_AND_FRIENDS = {
    "family_situation": "Current family situation (当前家庭状况)",
    "children_num": "Number of children (子女数量)",
    "household_size": "Number of people sharing household (共同居住人数)",
    "siblings_num": "Number of siblings growing up — archived (成长中兄弟姐妹数 已归档)",
    "friends_num": "Number of close friends — archived (密友数量 已归档)",
    "friends_childhood": "Friends known since childhood — archived (童年至今朋友数量 已归档)",
    "friends_proximity": "Close friends live nearby — archived (密友是否住附近 已归档)",
    "friendship_type": "Mode of interaction with friends — archived (与朋友的互动方式 已归档)",
    "friends_help_out": "Whether friends would help out when in need (是否有朋友能帮忙)",
    "friends_confide_in": "Whether has friends to confide in — archived (是否有朋友可倾诉 已归档)",
    "household_nature": "Nature of household growing up — conflict/stable, archived (成长家庭冲突/稳定性 已归档)",
    "household_description": "Household growing up — warm/distant, archived (成长家庭温暖/疏离程度 已归档)",
    "parental_support": "Type of parental/caregiver support — archived (父母/照顾者支持类型 已归档)",
    "family_proximity": "Adult family living nearby — archived (成年家人是否住附近 已归档)",
    "family_relationships": "Quality of relationships with adult family (与成年家人关系质量)",
}

# =============================================================================
# Faith & religion
# =============================================================================
FAITH = {
    "spirituality_connection": "Spiritual/transcendent connection — archived (灵性/超越连接感 已归档)",
    "love_feelings": "Extent of loving feelings towards others (对他人的关爱程度)",
    "religious_identity": "Religious identity — archived (宗教身份认同 已归档)",
    "religious_practice": "Whether actively practices religion — archived (是否践行宗教活动 已归档)",
    "individual_collective": "Individualism vs. collectivism orientation — archived (个人主义 vs 集体主义倾向 已归档)",
}

# =============================================================================
# Technology — smartphones, social media, AI, VR, gaming, nature
# =============================================================================
TECHNOLOGY = {
    # Smartphone & tablet
    "smartphone_own_old": "Owns a smartphone — old version, archived (是否拥有手机 旧版 已归档)",
    "smartphone_age_access": "Age first obtained a smartphone (首次获得手机年龄)",
    "smartphone_school_old": "Smartphone use at school — old version, archived (学校使用手机情况 旧版 已归档)",
    "smartphone_class_old": "Smartphone use in class — old version, archived (课堂上使用手机 旧版 已归档)",
    "smartphone_ownership _age": "Age of smartphone ownership (拥有手机年龄)",
    "smartphone_friends": "Number of friends with smartphones (手机朋友数量)",
    "smartphone_school_age": "Age school provided a smartphone (学校提供手机年龄)",
    "smartphone_class": "Smartphone use in class — new version (课堂使用手机 新版)",
    "smartphone_recess": "Smartphone use during recess (课间使用手机)",
    "tablet_ownership_age": "Age obtained a tablet (获得平板电脑年龄)",
    "smartphone_tablet_age": "Age obtained a smartphone/tablet (获得手机/平板年龄)",
    "laptop_school_age": "Age school provided a laptop (学校提供笔记本年龄)",
    "laptop_class": "Laptop use in class (课堂使用笔记本)",
    "internet_restrictions": "Internet access restrictions (上网限制)",

    # Social media
    "social_media_age": "Age started using social media (开始使用社交媒体年龄)",
    "social_media_freq": "Social media use frequency (社交媒体使用频率)",
    "sm_freq_new": "Social media use frequency — new version (社交媒体使用频率 新版)",
    "sm_impact": "Social media impact on life — multi-select (社交媒体对生活的影响 多选)",

    # AI
    "ai_freq": "AI tool usage frequency (AI 工具使用频率)",
    "ai_use_general": "AI general use cases — multi-select (AI 通用用途 多选)",
    "ai_use_social": "AI social/emotional use cases — multi-select (AI 社交/情感用途 多选)",
    "ai_impact_personal": "AI impact on personal life — multi-select (AI 对个人的影响 多选)",
    "ai_impact_work": "AI impact on work — multi-select (AI 对工作的影响 多选)",

    # VR, gaming & nature
    "vr_freq": "VR headset usage frequency (VR 头显使用频率)",
    "gaming_freq": "Video gaming frequency (电子游戏频率)",
    "time_nature": "Time spent in natural environments (在自然环境中时长)",
    "live_close_nature": "Whether lives close to nature (是否居住在自然附近)",
    "immersion_nature": "Most-frequented natural environment types — multi-select (最常接触的自然环境类型 多选)",
}

# =============================================================================
# Benchmarking scales — PHQ-9, GAD-7, life satisfaction
# =============================================================================
BENCHMARKING = {
    # PHQ-9 (depression screening)
    "PHQ9_interest": "PHQ-9: Little interest or pleasure in doing things (做事缺乏兴趣或乐趣)",
    "PHQ9_depressed": "PHQ-9: Feeling down, depressed, or hopeless (感到沮丧、抑郁或绝望)",
    "PHQ9_sleep": "PHQ-9: Trouble falling/staying asleep or sleeping too much (入睡困难、易醒或嗜睡)",
    "PHQ9_energy": "PHQ-9: Feeling tired or having little energy (感到疲倦或缺乏精力)",
    "PHQ9_failure": "PHQ-9: Feeling bad about yourself — failure, letting family down (自我否定/觉得自己失败)",
    "PHQ9_appetite": "PHQ-9: Poor appetite or overeating (食欲不振或暴饮暴食)",
    "PHQ9_concentration": "PHQ-9: Trouble concentrating on things (注意力难以集中)",
    "PHQ9_movement": "PHQ-9: Moving/speaking slowly or being fidgety/restless (动作迟缓或焦躁不安)",
    "PHQ9_self_harm": "PHQ-9: Thoughts of self-harm or being better off dead (自伤或自杀念头)",
    # GAD-7 (anxiety screening)
    "GAD7_nervous": "GAD-7: Feeling nervous, anxious, or on edge (感到紧张、焦虑)",
    "GAD7_worry": "GAD-7: Not being able to stop or control worrying (无法停止或控制担忧)",
    "GAD7_self_control": "GAD-7: Worrying too much about different things (对很多事情过度担忧)",
    "GAD7_relax": "GAD-7: Trouble relaxing (难以放松)",
    "GAD7_restless": "GAD-7: Being so restless that it is hard to sit still (坐立不安)",
    "GAD7_irritable": "GAD-7: Becoming easily annoyed or irritable (容易烦躁或易怒)",
    "GAD7_afraid": "GAD-7: Feeling afraid as if something awful might happen (感到害怕)",
    "GAD7_impact": "GAD-7: How difficult these problems made daily life (上述问题对生活的影响程度)",
    # Life satisfaction
    "life_satisfaction": "Overall life satisfaction 1-9 (总体生活满意度 1-9)",
}

# =============================================================================
# Momentary assessments — archived
# =============================================================================
MOMENTARY = {
    "time_day": "Time of day when assessment taken — archived (评估时间段 已归档)",
    "mood_current": "Current mood at assessment time — archived (当前情绪 已归档)",
    "alertness_current": "Current alertness level — archived (当前清醒程度 已归档)",
    "sleep_prevous_night": "Hours slept the previous night — archived (前一晚睡眠时长 已归档)",
    "time_last_meal": "Time since last meal — archived (距上次进食时间 已归档)",
    "physical_complaints": "Physical complaints at assessment time — archived (当前身体不适症状 已归档)",
    "pregnancy": "Whether currently pregnant — archived (是否怀孕 已归档)",
}

# =============================================================================
# COVID-19 impact — archived
# =============================================================================
COVID = {
    "covid_health": "COVID-19: health & social impact — archived (新冠疫情 健康与社交影响 已归档)",
    "covid_finance": "COVID-19: financial impact — archived (新冠疫情 财务影响 已归档)",
}

# =============================================================================
# Repeat respondent identifiers (anonymous, derived from email)
# =============================================================================
DEDUP = {
    "Repeat identifier": "Repeat respondent identifier — anonymous, derived from email (重复受访者标识符, 由邮箱匿名化生成)",
    "Repeat identifier 2": "Repeat respondent identifier — backup (重复受访者标识符 备用)",
}

# =============================================================================
# Flat aggregated dict for direct column-name lookup
# =============================================================================
COLUMN_DESCRIPTIONS: dict[str, str] = {}
for _group in [
    META,
    MHQ_SCORES,
    MHQ_ITEMS,
    DEMOGRAPHICS_CORE,
    WORK,
    LIFESTYLE,
    SUBSTANCE_AND_MEDICAL,
    TRAUMA,
    FAMILY_AND_FRIENDS,
    FAITH,
    TECHNOLOGY,
    BENCHMARKING,
    MOMENTARY,
    COVID,
    DEDUP,
]:
    COLUMN_DESCRIPTIONS.update(_group)


def describe_column(name: str) -> str:
    """Return the human-readable description for a column, or the column name itself if not found."""
    return COLUMN_DESCRIPTIONS.get(name, name)
